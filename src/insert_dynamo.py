import boto3


def get_table(table_name):
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)


def batch_write_items(table, items_batch):
    with table.batch_writer() as batch:
        for item in items_batch:
            batch.put_item(Item=item)


def chunk_items(items, chunk_size=25):
    for i in range(0, len(items), chunk_size):
        yield items[i : i + chunk_size]
