from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep


# ########    FastAPI ROUTER:  links    ########


from geoalchemy2.shape import to_shape
from magma.services.link import create_link, get_link, get_links
from magma.schemas.link import LineStringGeometryCreate, LinkStringGeometryRead

router = APIRouter(
    prefix="/links",
    tags=["Links"]
)

@router.post("/", response_model=LinkStringGeometryRead)
def create_link_endpoint(session: AsyncSessionDep, link_data: LineStringGeometryCreate):
    link = create_link(session, link_data)
    # Convert WKB to GeoJSON-like dict
    geom = to_shape(link.geom)
    return {
        "id": link.id,
        "type": "LineString",
        "coordinates": list(geom.coords)
    }


@router.get("/{link_id}", response_model=LinkStringGeometryRead)
def get_link_endpoint(session: AsyncSessionDep, link_id: int):
    link = get_link(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    geom = to_shape(link.geom)
    return {
        "id": link.id,
        "type": "LineString",
        "coordinates": list(geom.coords)
    }


@router.get("/", response_model=list[LinkStringGeometryRead])
def get_all_links_endpoint(session: AsyncSessionDep):
    links = get_links(session)
    return [
        {
            "id": link.id,
            "type": "LineString",
            "coordinates": list(to_shape(link.geom).coords)
        }
        for link in links
    ]

