# Generated by Django 5.0.6 on 2024-08-10 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_options_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['updated_at']},
        ),
    ]