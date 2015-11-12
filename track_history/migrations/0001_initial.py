# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.serializers.json
import decimal
import django_pgjsonb.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackHistoryFullSnapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history_data', django_pgjsonb.fields.JSONField(encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
            ],
        ),
        migrations.CreateModel(
            name='TrackHistoryRecord',
            fields=[
                ('full_snapshot', models.OneToOneField(primary_key=True, serialize=False, to='track_history.TrackHistoryFullSnapshot')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date and time this record was created.', verbose_name='date created', db_index=True)),
                ('object_id', models.TextField(help_text='Primary key of the model under track history control.')),
                ('object_id_int', models.IntegerField(help_text="An indexed, integer version of the stored model's primary key, used for faster lookups.", null=True, db_index=True, blank=True)),
                ('record_type', models.PositiveSmallIntegerField(choices=[(0, 'Created'), (1, 'Modified'), (2, 'Deleted')])),
                ('changes', django_pgjsonb.fields.JSONField(default={}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
                ('content_type', models.ForeignKey(help_text='Content type of the model under track history control.', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', to=settings.AUTH_USER_MODEL, help_text='The user who created this record.', null=True)),
            ],
        ),
    ]
