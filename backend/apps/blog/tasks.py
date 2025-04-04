from celery import shared_task
import logging

from .models import PostAnalytics
logger = logging.getLogger(__name__)

@shared_task
def increment_post_impressions(post_id):
    """Incrementa las impressiones del post asociado"""
    logger.info("Task to: Update Post Impressions")
    try:
        analytics, created = PostAnalytics.objects.get_or_create(post__id=post_id)
        analytics.increment_impression()
    except Exception as e:
        logger.info(f"Error incrementando las impresiones para el Post ID {post_id}:{str(e)}")
