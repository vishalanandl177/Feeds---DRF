from django.db import models
import uuid
from utils.validators import *
from config.settings import APP_USER_SESSION_EXPIRE_DAY_COUNT


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, validators=[text_validator, string_with_space_validator])
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, validators=[mobile_number_validator])
    profile_pic = models.ImageField(upload_to='user/')

    token = models.CharField(max_length=200, blank=True, null=True)
    token_expire_on = models.DateField(null=True)

    city = models.CharField(max_length=50, null=True, blank=True,
                            validators=[text_validator, string_with_space_validator])
    state = models.CharField(max_length=50, null=True, blank=True,
                             validators=[text_validator, string_with_space_validator])
    country = models.CharField(max_length=50, null=True, blank=True,
                               validators=[text_validator, string_with_space_validator])

    # Auto add timestamp when created
    added_on = models.DateTimeField(null=True, auto_now_add=True)

    # block user to perform any operation.
    is_blocked = models.BooleanField(default=False)

    # Always update timestamp when updated
    updated_on = models.DateTimeField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def login_data(self):
        return {
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'token': self.token,
            'profile_pic': self.profile_pic.url
        }

    def get_instance(self):
        return self

    def profile(self):
        return {
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'city': self.city,
            'state': self.state,
            'country': self.country,
        }

    def update_token(self):
        self.token = self.get_token
        self.token_expire_on = timezone.now() + timezone.timedelta(days=APP_USER_SESSION_EXPIRE_DAY_COUNT)
        self.save()

    @property
    def get_token(self):
        return str(uuid.uuid4())

    def logout(self):
        self.token = None
        self.token_expire_on = None
        self.save()
        return True

    class Meta:
        ordering = ('-added_on',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'


