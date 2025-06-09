import logging
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from pyspark.sql.functions import count, date_format

logging.basicConfig(level=logging.INFO)


def generate_abandoned_summary_excel(monthly_report_df, output_excel_path):
    today = datetime.today()
    last_6_months = [
        (today - relativedelta(months=i)).strftime("%Y-%m") for i in range(5, -1, -1)
    ]

    pdf = monthly_report_df.toPandas()

    task_counts = {month: 0 for month in last_6_months}
    item_counts = {month: 0 for month in last_6_months}

    for _, row in pdf.iterrows():
        month = row["month_of_abandonment"]
        if month in last_6_months:
            if row["type_of_task"] == "Task":
                task_counts[month] += row["quantity"]
            elif row["type_of_task"] == "Shopping_Item":
                item_counts[month] += row["quantity"]

    final_df = pd.DataFrame(
        {
            "Description": ["Months", "Abandoned tasks", "Abandoned items"],
            **{
                month: [month, task_counts[month], item_counts[month]]
                for month in last_6_months
            },
        }
    )

    with pd.ExcelWriter(output_excel_path, engine="xlsxwriter") as writer:
        final_df.to_excel(writer, sheet_name="Report", index=False)

    logging.info(f"Report generated with success: {output_excel_path}")
