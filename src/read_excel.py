from pyspark.sql import SparkSession


def read_excel_file(csv_path):
    spark = SparkSession.builder.appName("ImportExcelToDynamoDB").getOrCreate()
    return spark.read.csv(csv_path, header=True, inferSchema=True, sep=";")
