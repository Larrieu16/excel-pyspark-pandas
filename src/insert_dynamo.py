import boto3
import json
import os
from pyspark.sql import SparkSession

# caminho do json
json_path = "C:\\Users\\Larri\\Downloads\\itens_dynamo.json"

# aqui eu defini uma tabela teste que foi criada via aws
dynamodb_table_name = "todo-list-dev"

# le o dicionario json
with open(json_path, "r", encoding="utf-8") as f:
    items = json.load(f)

# inicio sessao spark
spark = SparkSession.builder.appName("DynamoDBInsert").getOrCreate()

# aqui eu fiz uma conversao basica pra spark pra poder visualizar no terminal
df = spark.read.json(json_path)
df.show(truncate=False)

# chamamos o dynamodb com o boto3 (accesskey e secret setadas via terminal)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamodb_table_name)

# aqui enviamos os itens de 25 em 25, limite do dynamo...considerar o free tier
def batch_write(items_batch):
    with table.batch_writer() as batch:
        for item in items_batch:
            batch.put_item(Item=item)

# divide a lista em 25 itens
def chunk_items(items, chunk_size=25):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

# e aqui realizamos a insercao
for i, batch in enumerate(chunk_items(items, chunk_size=25)):
    batch_write(batch)
    print(f"Lote {i + 1} inserido com {len(batch)} itens.")

print(f"\nTotal de itens inseridos: {len(items)}")
