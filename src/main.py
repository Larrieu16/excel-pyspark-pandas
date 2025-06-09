import argparse
import json
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)
from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from fetch_from_dynamo import (create_dataframe_from_items,
                               fetch_items_from_dynamo)
from forgotten_month_of_tasks import generate_abandoned_summary_excel
from forgotten_tasks import identify_forgotten_tasks
from generate_items import generate_dynamo_items
from insert_dynamo import batch_write_items, chunk_items, get_table
from monthly_report import summarize_forgotten_tasks_monthly
from read_excel import read_excel_file
from transform_excel import transform_dataframe


def main():
    csv_path = "C:\\Users\\Larri\\Downloads\\amostragem.csv"
    output_csv = "C:\\Users\\Larri\\Downloads\\dynamo_transformed_sampling.csv"
    output_json = "C:\\Users\\Larri\\Downloads\\dynamo_items.json"
    output_excel = "C:\\Users\\Larri\\Downloads\\report_for_abandoned_tasks.xlsx"

    dynamodb_table_name = os.getenv("DYNAMODB_TABLE", "todo-list-dev")
    user_sub = "73acaa5a-1071-704c-aa8e-fdcee0e21b64"

    spark = SparkSession.builder.appName("MainDynamo").getOrCreate()
    table = get_table(dynamodb_table_name)

    parser = argparse.ArgumentParser(description="Process data for DynamoDB.")
    parser.add_argument(
        "--fetch-from-dynamo",
        action="store_true",
        help="Fetch data directly from DynamoDB",
    )
    parser.add_argument(
        "--insert-from-json",
        action="store_true",
        help="Insert data into DynamoDB with JSON file",
    )
    args = parser.parse_args()

    try:
        if args.fetch_from_dynamo:
            logging.info("\nFetching data from DynamoDB...")

            items = fetch_items_from_dynamo(
                user_id=user_sub, table_name=dynamodb_table_name
            )
            logging.info(f"{len(items)} items found.")

            df = create_dataframe_from_items(items)
            df.toPandas().to_csv(output_csv, sep=";", index=False)
            df.show(truncate=False)

            abandoned_tasks = identify_forgotten_tasks(df)
            monthly_summary_df = summarize_forgotten_tasks_monthly(abandoned_tasks)
            generate_abandoned_summary_excel(monthly_summary_df, output_excel)

        elif args.insert_from_json:
            logging.info("\nInserting data into DynamoDB with JSON file...")
            with open(output_json, "r") as file:
                items = json.load(file)

            logging.info(f"Total items to insert: {len(items)}")
            for batch in chunk_items(items):
                batch_write_items(table, batch)
            logging.info("Inserted items into DynamoDB successfully.")

        else:
            logging.info("\nReading CSV file and generating JSON for DynamoDB...")
            df = read_excel_file(csv_path)
            df_transformed = transform_dataframe(df)
            df_transformed.toPandas().to_csv(output_csv, sep=";", index=False)

            dynamo_items = generate_dynamo_items(df_transformed)
            with open(output_json, "w") as file:
                json.dump(dynamo_items, file, indent=2)
            logging.info(f"JSON file generated at: {output_json}")

    except Exception as e:
        logging.info(f"Error during execution: {e}")


if __name__ == "__main__":
    main()
