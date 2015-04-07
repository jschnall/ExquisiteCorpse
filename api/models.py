__author__ = 'jschnall'

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

from allauth.account.models import EmailAddress


class Profile(models.Model):
    owner = models.OneToOneField(User)

    def __unicode__(self):
            return "{}'s profile".format(self.user.username)

    def account_verified(self):
        if self.owner.is_authenticated:
            result = EmailAddress.objects.filter(email=self.owner.email)
            if len(result):
                return result[0].verified
        return False
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Composition(models.Model):
    OPEN = 'OPEN'
    INVITE_ONLY = 'INVITE_ONLY'
    JOIN_POLICY_CHOICES = (
        (OPEN, 'Open'),
        (INVITE_ONLY, 'Invite only'),
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    started = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User)
    users = models.ManyToManyField(User, related_name="composition_users", blank=True)
    max_users = models.IntegerField(default=2, blank=False)
    title = models.CharField(max_length=100, blank=False, unique=True)
    turns = models.IntegerField(default=1, blank=True)
    min_part_chars = models.IntegerField(default=1, blank=False)
    max_part_chars = models.IntegerField(default=500, blank=False)
    join_policy = models.CharField(choices=JOIN_POLICY_CHOICES, default=OPEN, max_length=100)
    # Whether to publicly list the final result for everyone to see
    public_result = models.BooleanField(default=True, blank=True)

    def __unicode__(self):
        return self.title + ' (' + str(self.pk) + ')'


class Part(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    composition = models.ForeignKey(Composition)
    text = models.TextField(blank=True, max_length=10000)
    segue = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return str(self.pk)

