from sqlalchemy import select
from magma.core.dependencies import AsyncSessionDep
from magma.models.link import Link
from magma.schemas.link import LineStringGeometryCreate, LineStringGeometryRead
from geoalchemy2.shape import to_shape
from shapely.geometry import LineString


# ########    SERVICE:  link    ########


async def create_link(session: AsyncSessionDep, link_data: LineStringGeometryCreate) -> Link:
    # Convert GeoJSON coordinates to WKT LineString  # TODO: This conversion needs to be tested well, documented
    line = LineString(link_data.coordinates)
    new_link = Link(geom=f'SRID=4326;{line.wkt}')
    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)
    return new_link


async def get_link(session: AsyncSessionDep, link_id: int) -> Link:
    statement = select(Link).where(Link.id == link_id)
    result = await session.execute(statement)
    found_record = result.scalar_one_or_none()
    return found_record


async def get_links(session: AsyncSessionDep, skip: int = 0, limit: int = 10):
    statement = select(Link).offset(skip).limit(limit)
    result = await session.execute(statement)
    links = result.scalars().all()
    return links

