# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 09:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('offers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20161207_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedOfferNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CommentNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='MessageNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Note')),
            ],
        ),
        migrations.CreateModel(
            name='NewOfferNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('read', models.BooleanField()),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.Notification')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offers.Offer')),
            ],
        ),
        migrations.CreateModel(
            name='RefusedOfferNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_notification', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.OfferNotification')),
            ],
        ),
        migrations.AddField(
            model_name='newoffernotification',
            name='offer_notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.OfferNotification'),
        ),
        migrations.AddField(
            model_name='messagenotification',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.Notification'),
        ),
        migrations.AddField(
            model_name='commentnotification',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.Notification'),
        ),
        migrations.AddField(
            model_name='acceptedoffernotification',
            name='offer_notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.OfferNotification'),
        ),
    ]
