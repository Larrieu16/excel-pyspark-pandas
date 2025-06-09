import boto3
from pyspark.sql.functions import col, count, current_date, date_format


def summarize_forgotten_tasks_monthly(df):
    return (
        df.withColumn("month_of_abandonment", date_format(col("createdAt"), "yyyy-MM"))
        .groupBy("type_of_task", "month_of_abandonment")
        .agg(count("*").alias("quantity"))
    )
