import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from celery_notification_watcher.config import DATABASE_URL, ECHO

engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       echo=ECHO)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

