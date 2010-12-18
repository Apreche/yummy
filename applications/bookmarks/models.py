from datetime import datetime
from django.db import models
from taggit.managers import TaggableManager

class Bookmark(models.Model):
    title = models.TextField()
    url = models.URLField(verify_exists=False, max_length=2500)
    owner = models.ForeignKey('auth.user')
    pub_date = models.DateTimeField(default=datetime.now())
    edit_date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    private = models.BooleanField(default=False)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
