from sqlalchemy.ext.automap import automap_base

from celery_notification_watcher.database import engine


Base = automap_base()

Base.prepare(autoload_with=engine)

TicketNotify = Base.classes.tickets_ticketnotify
News = Base.classes.users_news
Ticket = Base.classes.tickets_ticket
User = Base.classes.auth_user

