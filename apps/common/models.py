from django.db import models
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False, verbose_name=_("Model id"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class VersionHistory(BaseModel):
    version = models.CharField(_("Version"), max_length=64)
    required = models.BooleanField(_("Required"), default=True)

    class Meta:
        verbose_name = _("Version history")
        verbose_name_plural = _("Version histories")

    def __str__(self):
        return self.version
