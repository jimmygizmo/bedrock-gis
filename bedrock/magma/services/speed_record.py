from sqlalchemy import select
from magma.core.dependencies import AsyncSessionDep
from magma.models.speed_record import SpeedRecord
from magma.schemas.speed_record import SpeedRecordCreate


# ########    SERVICE:  speed_record    ########


async def create_speed_record(session: AsyncSessionDep, record_in: SpeedRecordCreate) -> SpeedRecord:
    record = SpeedRecord(
        timestamp=record_in.timestamp,
        speed=record_in.speed,
        link_id=record_in.link_id
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def get_speed_record(session: AsyncSessionDep, record_id: int):
    statement = select(SpeedRecord).where(SpeedRecord.id == record_id)
    result = await session.execute(statement)
    found_record = result.scalar_one_or_none()
    return found_record


async def get_speed_records(session: AsyncSessionDep, skip: int = 0, limit: int = 10):
    statement = select(SpeedRecord).offset(skip).limit(limit)
    result = await session.execute(statement)
    speed_records = result.scalars().all()
    return speed_records


async def get_speed_records_by_link(
            session: AsyncSessionDep,
            link_id: int,
            skip: int = 0,
            limit: int = 10,
        ) -> list[SpeedRecord]:
    statement = select(SpeedRecord).where(SpeedRecord.link_id == link_id).offset(skip).limit(limit)
    result = await session.execute(statement)
    speed_records = result.scalars().all()
    return speed_records

