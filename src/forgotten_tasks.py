import logging

from pyspark.sql.functions import col, current_date, datediff, to_date

logging.basicConfig(level=logging.INFO)


def identify_forgotten_tasks(df):
    df_date = df.withColumn("createdAt", to_date("createdAt"))
    df_todo = df_date.filter(col("status") == "todo")

    abandoned_tasks = df_todo.filter(
        (
            (col("type_of_task") == "Task")
            & (datediff(current_date(), col("createdAt")) > 15)
        )
        | (
            (col("type_of_task") == "Shopping_Item")
            & (datediff(current_date(), col("createdAt")) > 30)
        )
    )

    logging.info("Abandoned tasks identified: ")
    abandoned_tasks.show(truncate=False)

    return abandoned_tasks
