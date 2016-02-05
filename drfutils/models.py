import uuid

from django.db import models


class Token(models.Model):
    """
    A token that can be used for API authentication and authorisation.

    Initially intended to use to authorise an API client, this may later
    be extended to support user or team tokens.

    """
    key = models.CharField(max_length=50, primary_key=True, editable=False)
    label = models.CharField(
        max_length=200,
        help_text="""
        A label to distinguish between tokens.
        May be e.g. the provider/client name.
        """
    )

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = str(uuid.uuid4())
        super(Token, self).save(*args, **kwargs)
