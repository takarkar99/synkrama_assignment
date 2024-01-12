from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField(null=True, blank=True)



class UserBlock(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')
    block_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block_user')

    class Meta:

        unique_together = ('blocker','block_user')
