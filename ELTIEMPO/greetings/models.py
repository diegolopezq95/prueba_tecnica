from django.db import models


class Senior(models.Model):
    name = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    greeting = models.CharField(max_length=130)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name

