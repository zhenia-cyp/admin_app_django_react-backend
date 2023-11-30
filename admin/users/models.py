from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password


class Permission(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Право доступа"
        verbose_name_plural = "Права доступа"
        ordering = ['id']



class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ['id']



class MyUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200, blank=True, null=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL, null=True)
    order_num = models.BigIntegerField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return '{0},{1},{2},{3}'.format(self.first_name, self.last_name, self.email, self.password)

    def is_password_valid(self, password):
        return check_password(password, self.password)

    def assign_order_numbers(self):
        print('assign_order_numbers')
        users = MyUser.objects.all().order_by('id')
        for index, user in enumerate(users, start=1):
            user.order_num = index
            user.save()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id']






