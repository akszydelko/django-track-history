# Generated by Django 3.0.6 on 2020-05-24 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track_history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackhistoryrecord',
            name='object_id',
            field=models.TextField(db_index=True, help_text='Primary key of the model under track history control.'),
        ),
    ]
