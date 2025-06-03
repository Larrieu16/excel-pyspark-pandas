import pandas as pd
from pyspark.sql import SparkSession

csv_path = "C:\\Users\\Larri\\Downloads\\amostragem.csv"

spark = SparkSession.builder.appName("ImportExcelToDynamoDB").getOrCreate()

# header significa que a primeira linha eh o cabecalho,  inferSchema tenta identificar quais tipos de dados
# estao entrando. existem varios outros metodos uteis como o path, que futuramente vou aplicar pra achar
# o arquivo ao inves de fazer isso numa linha... (linha 4, csv_path)
df_read_excel = spark.read.csv(csv_path, header=True, inferSchema=True)

df_read_excel.show(truncate=False) #truncate significa truncar strings longas, ou nao
df_read_excel.printSchema()
