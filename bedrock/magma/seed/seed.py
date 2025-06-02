import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape
from datetime import datetime

# from magma.core.dependencies import AsyncSessionDep   # Not using this. Headache with env vars and more.
# from magma.core.database import async_engine, AsyncSessionLocal, Base   # Not using this either. Similarly.

# These must be imported for sqlalchemy.orm.declarative_base() to know about them and create them in create_all.
from magma.models.slink import Slink
from magma.models.sspeed_record import SspeedRecord
from magma.core.database import Base

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

SEED_DATABASE_URL = 'postgresql+asyncpg://bedrock:bedrock@localhost:45432/bedrockdb'


seed_async_engine = create_async_engine(SEED_DATABASE_URL)

# Async session factory
AsyncSessionLocal = sessionmaker(
        bind=seed_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

# SeedBase = declarative_base()  # Pydantic Declarative Base - Reference DB schema used for database creation/changes

async def async_db_create_all():
    async with seed_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_slinks(session: AsyncSession, file_path: str):
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

    await session.commit()
    print("✅ Links loaded.")


async def load_sspeed_records(session: AsyncSession, file_path: str):
    df = pd.read_parquet(file_path)

    # Effectively convert in place the string/object values to actual datetime type values of column date_time
    # Observed UTC timezone in many rows so data is timezone aware.
    df["date_time"] = pd.to_datetime(df["date_time"])

    # REMOVE PK CONSTRAINT TEMPORARILY - WE MAY NOT NEED TO DO THIS WITH OUR NEW VALIDATION FILTERING
    # await session.execute(text("""
    #                            ALTER TABLE sspeed_records
    #                            DROP
    #                            CONSTRAINT fk_sspeed_slink
    #                            """))
    # await session.commit()

    # Adding link_id validation so we load with referential integrity and maintain PK relationship.
    # UPDATE: Visibility below shows we actually had no bad records. All speed_record link_ids have a valid relation.
    # 1. Get all valid link_ids
    result = await session.execute(
        text("SELECT id FROM slinks")
    )
    valid_ids = set(r[0] for r in result.fetchall())  # Flatten to simple set

    # 2. Filter dataframe
    filtered_df = df[df["link_id"].isin(valid_ids)]
    print(f"ℹ️ Importing {len(filtered_df)} of {len(df)} sspeed_records with valid slink_id...")

    # 3. Visibility of bad records:
    dropped_df = df[~df["link_id"].isin(valid_ids)]
    dropped_df.to_parquet("dropped_records.parquet")


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
        # for _, row in df.iterrows()  # Original unfiltered full data source
        for _, row in filtered_df.iterrows()
    ]

    # session.add_all(records)  # Disabled for experimental fix attempt below

    # ************ SPECIAL TIMEZONE ISSUE FIX ATTEMPT ************
    # Avoids bulk load ambiguities (bugs sort of) in negotiation of typs with respect to timezone required and others.
    # filtered_df["date_time"] = pd.to_datetime(df["date_time"], utc=True)  # Already did this above

    # We must make input data names match the model names when using an import method like to_dict:
    filtered_df.rename(columns={"link_id": "slink_id"}, inplace=True)

    records = filtered_df.to_dict(orient="records")

    # ROE BY ROW RATHER THAN THE BULK add_all(records)
    for record in records:
        obj = SspeedRecord(**record)
        session.add(obj)
    # ************************************************************
    # If this does not work we will have to drop the timezone awareness which in this case if OK for now.
    # In a final production system you cannot usually drop timezone awareness unless your system is designed for that.

    await session.commit()
    print("✅ SpeedRecords loaded.")

    # ADD BACK PK CONSTRAINT:
    # await session.execute(text("""
    #                            ALTER TABLE sspeed_records
    #                                ADD CONSTRAINT fk_sspeed_slink
    #                                    FOREIGN KEY (slink_id) REFERENCES slinks (id)
    #                            """))
    # await session.commit()


async def main():
    # The correct Base (delaclarative_base) must be imported AND all needed models imported before a create_all is done.
    await async_db_create_all()

    # Check that the tables we need even exist. This requires the correct Base as well as all needed models imported
    # before the create_all ran, and many other prerequisites, so this is a valuable check.
    async with seed_async_engine.begin() as conn:
        result = await conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        print('*** EXISTING TABLES:')
        all_tables = result.fetchall()
        print(all_tables)
        print()

    async with AsyncSessionLocal() as session:
        await load_slinks(session, "../../../datavolume/link_info.parquet.gz")
        await load_sspeed_records(session, "../../../datavolume/duval_jan1_2024.parquet.gz")


if __name__ == "__main__":
    asyncio.run(main())


# Not using the dependency in thie standalone script. Using AsyncSessionLocal which I just added to magma.core.database
# if __name__ == "__main__":
#     seed_session = AsyncSessionDep
#     try:
#         async_db_create_all()
#         load_links(seed_session, "data/link_info.parquet.gz")
#         load_speed_records(seed_session, "data/duval_jan1_2024.parquet.gz")
#     finally:
#         seed_session.close()

