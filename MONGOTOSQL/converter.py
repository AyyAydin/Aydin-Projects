import json
import pymongo
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB = os.getenv("MONGO_DB")
COL = os.getenv("MONGO_COLLECTION")


# Convert BSON types → SQL-friendly types
def convert_value(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, list):
        return json.dumps(value)
    if isinstance(value, dict):
        return json.dumps(value)
    return value


# Flatten nested dictionaries using dot notation
def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, convert_value(v)))
    return dict(items)


def infer_sql_type(value):
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "FLOAT"
    return "TEXT"


def main():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB]
    col = db[COL]

    docs = list(col.find())
    if not docs:
        print("No documents found.")
        return

    flattened_docs = [flatten_dict(d) for d in docs]

    # Infer SQL table columns
    columns = {}
    for doc in flattened_docs:
        for key, value in doc.items():
            if key not in columns:
                columns[key] = infer_sql_type(value)

    table_name = f"{COL}_table"

    # Build CREATE TABLE statement
    create_stmt = f"CREATE TABLE {table_name} (\n"
    for col_name, col_type in columns.items():
        create_stmt += f"  `{col_name}` {col_type},\n"
    create_stmt = create_stmt.rstrip(",\n") + "\n);"

    # Build INSERT statements
    insert_statements = []
    for doc in flattened_docs:
        keys = ", ".join(f"`{k}`" for k in doc.keys())
        values = ", ".join(f"'{str(v).replace('\'', '\"')}'" for v in doc.values())
        insert_statements.append(f"INSERT INTO {table_name} ({keys}) VALUES ({values});")

    # Output file
    with open("mongo_to_sql_output.sql", "w", encoding="utf-8") as f:
        f.write(create_stmt + "\n\n")
        for stmt in insert_statements:
            f.write(stmt + "\n")

    print("Conversion complete!")
    print("Output saved to: mongo_to_sql_output.sql")


if __name__ == "__main__":
    main()
