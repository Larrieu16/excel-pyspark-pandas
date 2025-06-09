import logging

import boto3
from boto3.dynamodb.conditions import Key
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO)


def fetch_items_from_dynamo(user_id: str, table_name: str):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").begins_with("LIST#")
    )
    return response.get("Items", [])


def create_dataframe_from_items(items: list):
    spark = SparkSession.builder.appName("FetchDynamo").getOrCreate()
    return spark.createDataFrame(items)


if __name__ == "__main__":
    import os

    user_id = "73acaa5a-1071-704c-aa8e-fdcee0e21b64"
    table_name = os.getenv("DYNAMODB_TABLE", "todo-list-dev")

    items = fetch_items_from_dynamo(user_id, table_name)
    logging.info(f"{len(items)} itens fetched from DynamoDB.")

    df = create_dataframe_from_items(items)
    df.show(truncate=False)
    df.printSchema()
