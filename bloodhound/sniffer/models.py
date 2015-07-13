import uuid

from django.db import models


class CrawlFrontier(models.Model):
    sniff_session = models.UUIDField()
    url = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visited = models.BooleanField(default=False)
    visited_at = models.DateTimeField(null=True)
    status_code = models.IntegerField(null=True)
