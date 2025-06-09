def generate_dynamo_items(df):
    pandas_df = df.toPandas()

    dynamo_items = []
    for _, row in pandas_df.iterrows():
        item = {
            "PK": row["PK"],
            "SK": row["SK"],
            "item_id": row["item_id"],
            "name": row["name"],
            "status": row["status"],
            "createdAt": row["createdAt"],
            "date": row["date"],
            "type_of_task": row.get("task_type", None),
        }
        clean_item = {k: v for k, v in item.items() if v is not None}
        dynamo_items.append(clean_item)

    return dynamo_items
