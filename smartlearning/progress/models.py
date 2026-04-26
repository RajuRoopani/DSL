from django.db import models


class Progress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return f"Progress({self.user.username}: {self.xp})"
