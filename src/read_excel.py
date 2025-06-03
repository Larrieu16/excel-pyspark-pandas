import pandas as pd
from pyspark.sql import SparkSession

csv_path = "C:\\Users\\Larri\\Downloads\\amostragem.csv"

spark = SparkSession.builder.appName("ImportExcelToDynamoDB").getOrCreate()

df_read_excel = spark.read.csv(csv_path, header=True, inferSchema=True)

df_read_excel.show(truncate=False)
df_read_excel.printSchema()
