# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-07 05:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm_to_pocket', '0011_product_type_of_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='type_of_user',
        ),
    ]