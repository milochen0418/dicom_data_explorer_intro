import duckdb
import logging
import idc_index_data as idc_data

PARQUET_PATH = str(idc_data.IDC_INDEX_PARQUET_FILEPATH)


def get_db_connection():
    return duckdb.connect()


def fetch_collections() -> list[dict]:
    try:
        conn = get_db_connection()
        query = f"\n            SELECT DISTINCT collection_id\n            FROM '{PARQUET_PATH}'\n            WHERE collection_id IS NOT NULL\n            ORDER BY collection_id\n        "
        df = conn.execute(query).fetchdf()
        return [{"Collection": row["collection_id"]} for _, row in df.iterrows()]
    except Exception as e:
        logging.exception(f"Error fetching IDC collections: {e}")
        return []


def fetch_modalities(collection: str = "") -> list[dict]:
    try:
        conn = get_db_connection()
        where_clause = "WHERE Modality IS NOT NULL"
        if collection:
            where_clause += f" AND collection_id = '{collection}'"
        query = f"\n            SELECT DISTINCT Modality\n            FROM '{PARQUET_PATH}'\n            {where_clause}\n            ORDER BY Modality\n        "
        df = conn.execute(query).fetchdf()
        return [{"Modality": row["Modality"]} for _, row in df.iterrows()]
    except Exception as e:
        logging.exception(f"Error fetching IDC modalities: {e}")
        return []


def fetch_body_parts(collection: str = "") -> list[dict]:
    try:
        conn = get_db_connection()
        where_clause = "WHERE BodyPartExamined IS NOT NULL"
        if collection:
            where_clause += f" AND collection_id = '{collection}'"
        query = f"\n            SELECT DISTINCT BodyPartExamined\n            FROM '{PARQUET_PATH}'\n            {where_clause}\n            ORDER BY BodyPartExamined\n        "
        df = conn.execute(query).fetchdf()
        return [
            {"BodyPartExamined": row["BodyPartExamined"]} for _, row in df.iterrows()
        ]
    except Exception as e:
        logging.exception(f"Error fetching IDC body parts: {e}")
        return []


def fetch_series(
    collection: str = "", modality: str = "", body_part: str = "", limit: int = 1000
) -> list[dict]:
    try:
        conn = get_db_connection()
        conditions = ["1=1"]
        if collection:
            conditions.append(f"collection_id = '{collection}'")
        if modality:
            conditions.append(f"Modality = '{modality}'")
        if body_part:
            conditions.append(f"BodyPartExamined = '{body_part}'")
        where_clause = " AND ".join(conditions)
        query = f"\n            SELECT \n                SeriesInstanceUID,\n                collection_id as Collection,\n                Modality,\n                BodyPartExamined,\n                SeriesDate,\n                SeriesDescription,\n                instanceCount as ImageCount,\n                series_size_MB,\n                series_aws_url\n            FROM '{PARQUET_PATH}'\n            WHERE {where_clause}\n            LIMIT {limit}\n        "
        df = conn.execute(query).fetchdf()
        df = df.fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        logging.exception(f"Error fetching IDC series: {e}")
        return []