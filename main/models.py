from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.conf import settings

# Create your models here.


# PROFILE model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(verbose_name='Аватар', upload_to='pics/ava/%Y/%m/%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.bio:
            item = self.bio
        else:
            item = "empty profile bio of user " + str(self.user)
        return item

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# POSTS model
class Posts (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Content', blank=True, max_length=2000)
    photo = models.ImageField(verbose_name='Image', upload_to='pics/%Y/%m/%d/')
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('one_post', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']


# COMMENTS model


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='comment', max_length=400)
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']


# FOLLOW model


class Follow(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
