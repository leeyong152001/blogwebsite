# Generated by Django 4.2.1 on 2023-05-22 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_body_alter_post_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='featured',
        ),
    ]
