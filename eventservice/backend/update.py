import logging

from apscheduler.schedulers.background import BackgroundScheduler
from backend.api import sender_email

from datetime import datetime

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sender_email, 'interval', seconds=10, start_date=datetime.now() )
    scheduler.start()
    logger.error("scheduler.start()")