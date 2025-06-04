from pyspark.sql.functions import col, udf, lit, concat_ws
from pyspark.sql.types import StringType
from datetime import datetime
import uuid

# conversao de integer para strings legiveis do dynamodb
def map_status(status_id):
    return {
        1: "todo",
        2: "done",
        3: "cancelled"
    }.get(status_id, "unknown")

# aqui a gente registra como uma UDF (User Defined Function) para usar no PySpark com WithColumn
map_status_udf = udf(map_status, StringType())

def transform_dataframe(df):
    #UUID unico pra cada item, ai e armazenado na coluna item_id
    df = df.withColumn("item_id", udf(lambda: str(uuid.uuid4()), StringType())())

    #gera a data hora atual no formato ISO, UTCNOW esta em depreciacao, estudar como substituir
    now_iso = datetime.utcnow().isoformat()
    #lit no pyspark insere um valor constante/fixo
    df = df.withColumn("createdAt", lit(now_iso))

    df = df.withColumn("date", col("Data de Conclusão").cast("timestamp"))
    df = df.withColumn("date", col("date").cast("date").cast(StringType()))

    #criacao pk e sk
    df = df.withColumn("PK", concat_ws("", lit("USER#"), col("ID do Usuário")))
    df = df.withColumn("SK", concat_ws("", lit("LIST#"), col("date"), lit("#ITEM#"), col("item_id")))

    #ajuste dos nomes existentes na tabela de amostragem
    df = df.withColumnRenamed("Nome da Tarefa", "name")
    df = df.withColumnRenamed("Tipo da Tarefa", "tipo_tarefa")
    df = df.withColumnRenamed("Tipo da Tarefa ID", "tipo_tarefa_id")
    df = df.withColumnRenamed("Status", "status_id")  

    #aqui a gente chama a funcao do map_status para a conversao do integer em texto
    df = df.withColumn("status", map_status_udf(col("status_id")))  

    # e aqui a gente filtra com os campos desejados no dataframe
    df = df.select(
        "PK", "SK", "item_id", "name", "status", "createdAt", "date",
        "tipo_tarefa", "tipo_tarefa_id", "status_id"
    )

    return df