__author__ = 'jschnall'

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

from allauth.account.models import EmailAddress


from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class IntegerRangeField(models.IntegerField):
    def __init__(self, min_value=None, max_value=None, *args,  **kwargs):
        self.min_value, self.max_value = min_value, max_value
        validators = []
        if isinstance(max_value, int):
            validators.append(MaxValueValidator(max_value))
        if isinstance(min_value, int):
            validators.append(MinValueValidator(min_value))
        kwargs.setdefault('validators', validators)
        super(IntegerRangeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


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
    start_time = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(User)
    users = models.ManyToManyField(User, related_name="composition_users", blank=True)
    # User who's turn it currently is
    active_user = models.ForeignKey(User, related_name="composition_active_user")
    # Users who've favorited this composition
    favorites = models.ManyToManyField(User, related_name="composition_favorites", blank=True)
    likes = models.ManyToManyField(User, related_name="composition_likes", blank=True)

    title = models.CharField(max_length=100, blank=False, unique=True)
    theme = models.CharField(max_length=100, blank=True)

    rounds = IntegerRangeField(default=3, min_value=1, max_value=100, blank=True)
    max_users = IntegerRangeField(default=2, min_value=2, max_value=100, blank=False)
    min_part_chars = IntegerRangeField(default=1, min_value=1, max_value=10000, blank=False)
    max_part_chars = IntegerRangeField(default=100, min_value=1, max_value=10000, blank=False)
    join_policy = models.CharField(choices=JOIN_POLICY_CHOICES, default=OPEN, max_length=100)
    # Whether to publicly list the final result for everyone to see
    public_result = models.BooleanField(default=True, blank=True)

    def newest_part(self):
        '''
        :return: The most recently added part
        '''
        return self.part_set.order_by('created').first()

    def next_user(self):
        '''
        :return: The user who's turn is next
        '''
        active_user_found = False
        for user in self.users.all():
            if active_user_found:
                return user
            if self.active_user == user:
              active_user_found = True
        return self.users.first()

    def current_round(self):
        if self.part_set:
            self.part_set.count() // self.users.count() + 1
        return 1

    def __unicode__(self):
        return self.title + ' (' + str(self.pk) + ')'


class Part(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name="Part_likes", blank=True)
    composition = models.ForeignKey(Composition)
    text = models.TextField(blank=True, max_length=10000)
    segue = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return str(self.pk)

