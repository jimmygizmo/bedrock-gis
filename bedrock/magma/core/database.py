import magma.core.config as cfg
from magma.core.logger import log
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ########    DATABASE INITIALIZATION    ########

async_engine = create_async_engine(cfg.DATABASE_URL)

# Async session factory - WE PROBABLY WILL NOT USE THIS. External scripts can construct their own and should perhaps.
# AsyncSessionLocal = sessionmaker(
#         bind=async_engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#     )
# TODO: CLeanup including the imports

Base = declarative_base()  # Pydantic Declarative Base - Reference DB schema used for database creation/changes


log.debug(f"🔵  Async DB session initialized  🔵")

