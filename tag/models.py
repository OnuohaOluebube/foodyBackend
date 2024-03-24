from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid

class Tag(models.Model):
    label = models.CharField(max_length = 255)


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)
    #The object the tag is applied to
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    #Id of the object the tag is applied to
    object_id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)
    #The particula object that a tag is applied to
    content_object = GenericForeignKey()