# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Yamls(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    number = models.IntegerField(default=1)
    template_id = models.CharField(max_length=30)
    create_date_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)
    content = models.TextField()
    args = models.CharField(max_length=400)

    class Meta:
        default_permissions = ()
        ordering = ['-create_date_time']


class Templates(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    create_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        default_permissions = ()
        ordering = ['-create_date_time']


# 存放模板中的变量
class ActionTemplates(models.Model):
    status_choices=(
        (0, '正常'),
        (1, '禁用'),
    )
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    status = models.IntegerField(choices=status_choices, default=0)
    template_id = models.CharField(max_length=30)
    template_value = models.TextField()
    create_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        default_permissions = ()
        ordering = ['-create_date_time']

