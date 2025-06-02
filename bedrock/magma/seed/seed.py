import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape
from sqlalchemy.orm import Session
from datetime import datetime

from magma.core.dependencies import AsyncSessionDep
from magma.models.slink import Slink
from magma.models.sspeed_record import SspeedRecord
from magma.core.database import async_engine, Base


async def async_db_create_all():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_links(session: Session, file_path: str):
    df = pd.read_parquet(file_path)

    for _, row in df.iterrows():
        geometry_obj = shape(json.loads(row["geo_json"]))
        link = Slink(
            id=row["link_id"],
            _length=float(row["_length"]) if row["_length"] else None,
            road_name=row["road_name"],
            usdk_speed_category=row["usdk_speed_category"],
            funclass_id=row["funclass_id"],
            speedcat=row["speedcat"],
            volume_value=row["volume_value"],
            volume_bin_id=row["volume_bin_id"],
            volume_year=row["volume_year"],
            volumes_bin_description=row["volumes_bin_description"],
            geometry=f"SRID=4326;{geometry_obj.wkt}",
        )
        session.add(link)

    session.commit()
    print("✅ Links loaded.")


async def load_speed_records(session: Session, file_path: str):
    df = pd.read_parquet(file_path)
    df["date_time"] = pd.to_datetime(df["date_time"])

    records = [
        SspeedRecord(
            slink_id=row["link_id"],
            date_time=row["date_time"],
            freeflow=row["freeflow"],
            count=row["count"],
            std_dev=row["std_dev"],
            min=row["min"],
            max=row["max"],
            confidence=row["confidence"],
            average_speed=row["average_speed"],
            average_pct_85=row["average_pct_85"],
            average_pct_95=row["average_pct_95"],
            day_of_week=row["day_of_week"],
            period=row["period"],
        )
        for _, row in df.iterrows()
    ]

    session.bulk_save_objects(records)
    session.commit()
    print("✅ SpeedRecords loaded.")


if __name__ == "__main__":
    seed_session = AsyncSessionDep
    try:
        async_db_create_all()
        load_links(seed_session, "data/link_info.parquet.gz")
        load_speed_records(seed_session, "data/duval_jan1_2024.parquet.gz")
    finally:
        seed_session.close()

