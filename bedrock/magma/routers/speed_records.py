from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.schemas.speed_record import SpeedRecordCreate, SpeedRecordRead
from magma.services.speed_record import create_speed_record, get_speed_record
from magma.services.speed_record import get_speed_records, get_speed_records_by_link


# ########    FastAPI ROUTER:  speed_records    ########


router = APIRouter(
    prefix='/speed-records',
    tags=['Speed Records']
)


@router.post("/", response_model=SpeedRecordRead, status_code=201)
def create_new_speed_record(session: AsyncSessionDep, record_in: SpeedRecordCreate):
    log.info(f"🧊  ----> /speed-records/    POST NEW")
    return create_speed_record(session, record_in)


@router.get("/{record_id}", response_model=SpeedRecordRead)
def read_speed_record(session: AsyncSessionDep, record_id: int):
    log.info(f"🧊  ----> /speed-records/{record_id}")
    record = get_speed_record(session, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="SpeedRecord not found")
    return record


@router.get("/", response_model=list[SpeedRecordRead])
async def read_speed_records(session: AsyncSessionDep, skip: int = 0, limit: int = 10):
    log.info(f"🧊  ----> /speed-records/")
    return await get_speed_records(session, skip=skip, limit=limit)


@router.get("/link/{link_id}", response_model=list[SpeedRecordRead])
def read_speed_records_by_link(session: AsyncSessionDep, link_id: int):
    log.info(f"🧊  ----> /speed-records/link/{link_id}")
    return get_speed_records_by_link(session, link_id)

