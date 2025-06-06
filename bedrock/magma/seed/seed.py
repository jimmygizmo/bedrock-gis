import json
import asyncio
import pandas as pd
from shapely.geometry import shape
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from magma.core.database import Base
from magma.models.link import Link
from magma.models.speed_record import SpeedRecord


DATABASE_URL = 'postgresql+asyncpg://bedrock:bedrock@localhost:45432/bedrockdb'

seed_async_engine = create_async_engine(DATABASE_URL)

# This is the correct way to get our async DB session in a standalone script, as opposed to using core.dependencies
AsyncSessionLocal = sessionmaker(
        bind=seed_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def async_db_create_all():
    # This create_all is here to handle special cases. The full stack has a primary startup create_all.
    async with seed_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_links(session: AsyncSession, file_path: str):
    print(f"Loading links from {file_path}")
    df = pd.read_parquet(file_path)

    for _, row in df.iterrows():
        geometry_obj = shape(json.loads(row["geo_json"]))
        link = Link(
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

    await session.commit()
    print("✅ Links loaded.")


async def load_speed_records(session: AsyncSession, file_path: str):
    print(f"Loading speed_records from {file_path}")
    df = pd.read_parquet(file_path)

    # Preserve timezone awareness (best practice): Convert string/object values to true datetime type for col date_time
    df["date_time"] = pd.to_datetime(df["date_time"])


    records = [
        SpeedRecord(
            link_id=row["link_id"],
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

    # Row-by-row is deliberate, to avoid datetime issues with bulk methods like add_all()
    records = df.to_dict(orient="records")  # Becuase we use to_dict() our col names must match data file col names.
    for record in records:
        obj = SpeedRecord(**record)
        session.add(obj)
    # ************************************************************

    await session.commit()
    print("✅ SpeedRecords loaded.")


async def main():
    await async_db_create_all()

    async with AsyncSessionLocal() as session:
        await load_links(session, "../../../datavolume/link_info.parquet.gz")
        await load_speed_records(session, "../../../datavolume/duval_jan1_2024.parquet.gz")


if __name__ == "__main__":
    asyncio.run(main())

