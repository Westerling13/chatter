from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    avatar = models.ImageField('Аватар профиля', upload_to='avatars')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Profile#{self.id}'


class User(AbstractUser):
    profile = models.OneToOneField(Profile, verbose_name='Профиль пользователя', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.profile = Profile.objects.create()
        super().save(*args, **kwargs)
