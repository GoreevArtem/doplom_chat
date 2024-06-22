from redis import Redis
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from service.posts import PostSingleton
from setting.settings import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

MONGO_URI = f"mongodb://mongo:27017"
post_singleton = PostSingleton(MONGO_URI)

redis_startup = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


def get_db():
    with SessionLocal() as db:
        yield db
