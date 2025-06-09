import uuid

from pyspark.sql.functions import (col, concat_ws, date_format, lit,
                                   to_timestamp, udf)
from pyspark.sql.types import StringType


def map_status(status_id):
    return {1: "todo", 2: "done", 3: "cancelled"}.get(status_id, "unknown")


map_status_udf = udf(map_status, StringType())


def _filter_valid_rows(df):
    return df.filter(
        (col("ID do Usuário") != "f9a533f2c78e4a09f87c9e68e442d3fe")
        & (col("Status") != 3)
    )


def _normalize_dates(df):
    df = df.withColumn(
        "createdAt", to_timestamp(col("Data de criação"), "dd/MM/yyyy HH:mm:ss")
    )
    df = df.withColumn(
        "createdAt", date_format(col("createdAt"), "yyyy-MM-dd'T'HH:mm:ss")
    )
    df = df.withColumn("date", col("Data de Conclusão").cast("timestamp"))
    return df.withColumn("date", date_format(col("date"), "yyyy-MM-dd"))


def generate_uuid():
    return str(uuid.uuid4())


generate_uuid_udf = udf(generate_uuid, StringType())


def map_task_type(tipo):
    return {"Tarefa a Ser Feita": "Task", "Item de Compra": "Shopping_Item"}.get(
        tipo, "Unknown"
    )


map_task_type_udf = udf(map_task_type, StringType())


def transform_dataframe(df):
    new_user_sub = "73acaa5a-1071-704c-aa8e-fdcee0e21b64"
    df = _filter_valid_rows(df)
    df = df.withColumn("ID do Usuário", lit(new_user_sub))
    df = df.withColumn("item_id", generate_uuid_udf())
    df = _normalize_dates(df)
    df = df.withColumn(
        "PK", concat_ws("", lit("USER#"), col("ID do Usuário"))
    ).withColumn(
        "SK",
        concat_ws("", lit("LIST#"), col("createdAt"), lit("#ITEM#"), col("item_id")),
    )
    df = (
        df.withColumnRenamed("Nome da Tarefa", "name")
        .withColumnRenamed("Tipo da Tarefa", "tipo_tarefa")
        .withColumnRenamed("Status", "status_id")
    )
    df = df.withColumn("status", map_status_udf(col("status_id"))).withColumn(
        "task_type", map_task_type_udf(col("tipo_tarefa"))
    )
    return df.select(
        "PK", "SK", "item_id", "name", "status", "createdAt", "date", "task_type"
    )
