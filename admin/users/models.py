from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password


class OrderedModel(models.Model):
    order_num = models.BigIntegerField(blank=True, null=True)
    class Meta:
        abstract = True

    @classmethod
    def assign_order_numbers(cls):
        objects = cls.objects.all().order_by('id')
        for index, obj in enumerate(objects, start=1):
            obj.order_num = index
            obj.save()


class Permission(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Право доступа"
        verbose_name_plural = "Права доступа"
        ordering = ['id']



class Role(OrderedModel):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ['id']



class MyUser(OrderedModel, AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200, blank=True, null=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return '{0},{1},{2},{3}'.format(self.first_name, self.last_name, self.email, self.password)

    def is_password_valid(self, password):
        return check_password(password, self.password)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id']






