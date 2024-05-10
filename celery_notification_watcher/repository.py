from sqlalchemy.orm import Session, joinedload

from celery_notification_watcher import SessionLocal
from celery_notification_watcher.models import TicketNotify


class TicketNotificationRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def all(self):
        with self.db() as session:
            session: Session
            return (session.query(TicketNotify)
                    .options(
                joinedload(TicketNotify.auth_user),
                joinedload(TicketNotify.tickets_ticket)
            )
                    .all())

    def save(self, notification: TicketNotify):
        with self.db() as session:
            session.add(notification)
            session.commit()
