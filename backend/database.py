from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./astro_matching.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class UserProfileDB(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=True)

    birth_date = Column(String(20), nullable=False)
    birth_time = Column(String(20), nullable=False)
    birth_city = Column(String(100), nullable=False)

    sun_sign = Column(String(20), nullable=True)
    moon_sign = Column(String(20), nullable=True)
    mercury_sign = Column(String(20), nullable=True)
    venus_sign = Column(String(20), nullable=True)
    mars_sign = Column(String(20), nullable=True)
    jupiter_sign = Column(String(20), nullable=True)
    saturn_sign = Column(String(20), nullable=True)

    ascendant = Column(String(20), nullable=True)
    ascendant_sign = Column(String(20), nullable=True)

    planetary_positions = Column(Text, nullable=True)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
