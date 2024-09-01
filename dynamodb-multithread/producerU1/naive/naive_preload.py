import json
import sys

import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed


def update_item(primary_key_value, entity_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ReadModelTable')

    response = table.get_item(
        Key={
            'PrimaryKey': primary_key_value
        }
    )
    item = response.get('Item')

    if f'{entity_id}_version' in item:
        version = item[f'{entity_id}_version'] + 1  # Increment the version
        item[f'{entity_id}_version'] = version
        item[entity_id] = {
            'Name': entity_id,
            'version': version
        }
    else:
        item[f'{entity_id}_version'] = 1  # Initialize if it doesn't exist

    # Update the item in DynamoDB
    response = table.put_item(Item=item)
    # print(f"UpdateItem succeeded for: {response}")


def main():
    # Arguments passed to the script
    args = sys.argv[1:]
    primary_key = args[0]
    req_count = int(args[1])
    workers = int(args[2])
    entity_id = args[3]

    primary_keys = [primary_key]  # List of primary keys to update
    primary_keys = primary_keys * req_count  # 100 ops

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Start the load operations and mark each future with its primary key
        futures = {executor.submit(update_item, key, entity_id): key for key in primary_keys}

        for future in as_completed(futures):
            primary_key = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Exception occurred for {primary_key}: {e}")


if __name__ == "__main__":
    main()
