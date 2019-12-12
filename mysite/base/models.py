from django.db import models
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from autodatetimefields.models import AutoDateTimeField


class BaseModel(models.Model):
    idx = ShortUUIDField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = AutoDateTimeField()
    is_obsolete = models.BooleanField(default=False)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return

    @classmethod
    def new(cls, **kwargs):
        return cls.objects.create(**kwargs)

    def delete(self, force_delete=True, **kwargs):
        if force_delete:
            super(BaseModel,self).delete(**kwargs)
        else:
            self.update(is_obsolete=True)
            return self

    class Meta:
        abstract = True
