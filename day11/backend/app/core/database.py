from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    from app.models import User, Resume, JobDescription, ATSReport, CoverLetter, ColdEmail
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        user = await session.get(User, "local-demo-user")
        if user is None:
            session.add(
                User(
                    id="local-demo-user",
                    email="local@ats-optimizer.app",
                    name="Local User",
                    hashed_password="authentication-disabled",
                )
            )
            await session.commit()
