# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SqaureCustomer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=100, blank=True)),
                ('access_token', models.CharField(default=None, max_length=200, blank=True)),
                ('location', models.CharField(default=None, max_length=100, blank=True)),
                ('expiry_date', models.DateField(default=None, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
