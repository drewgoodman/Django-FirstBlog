# Generated by Django 3.0.5 on 2020-05-14 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='height_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='width_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]