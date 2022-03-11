from django.db import models
from django.conf import settings

# Create your models here.
class StatusList(models.Model):
    # 1 author can post many statuses
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name = "author")
    textUpdate = models.CharField(max_length=140, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='date posted', auto_now_add=True)

    def __str__(self):
        return self.author.username
    
    def get_textUpdate(self):
        return self.textUpdate
    
    def get_created_at(self):
        return self.created_at