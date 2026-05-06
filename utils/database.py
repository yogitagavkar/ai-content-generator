from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ContentRecord(Base):
    __tablename__ = "content_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    seo_title = Column(String(255), nullable=True)
    seo_description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_content(title, prompt, content):
    db = SessionLocal()
    try:
        record = ContentRecord(
            title=title,
            prompt=prompt,
            content=content
        )
        db.add(record)
        db.commit()
    finally:
        db.close()