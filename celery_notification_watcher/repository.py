from sqlalchemy.orm import Session, joinedload

from celery_notification_watcher import SessionLocal
from celery_notification_watcher.models import TicketNotify, News, User, Ticket


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


class UsersRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def all(self):
        with self.db() as session:
            session: Session
            return session.query(User).all()

    def get_notified_users(self):
        with self.db() as session:
            session: Session
            return session.query(User).filter_by(is_receive_news=True).all()

    def save(self, notification: User):
        with self.db() as session:
            session.add(notification)
            session.commit()


class NewsRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def all(self):
        with self.db() as session:
            session: Session
            return session.query(News).all()

    def save(self, notification: News):
        with self.db() as session:
            session.add(notification)
            session.commit()

    def delete(self, news):
        with self.db() as session:
            session.delete(news)
            session.commit()


class TicketsRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def all(self):
        with self.db() as session:
            session: Session
            return session.query(Ticket).all()

    def save(self, ticket: Ticket):
        with self.db() as session:
            session.add(ticket)
            session.commit()

    def delete(self, ticket):
        with self.db() as session:
            session.delete(ticket)
            session.commit()