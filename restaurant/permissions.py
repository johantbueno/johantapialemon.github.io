from django.db import models
import uuid
from django.db.models import Model, Manager


class AbstractQuerySet(models.QuerySet):
    pass

class AbstractManager(Manager.from_queryset(AbstractQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)