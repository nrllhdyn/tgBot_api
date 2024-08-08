# Generated by Django 5.1 on 2024-08-08 21:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0003_userdailyreward_is_referral_reward'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdailyreward',
            old_name='is_referral_reward',
            new_name='is_referral_bonus',
        ),
        migrations.AlterUniqueTogether(
            name='userdailyreward',
            unique_together={('user', 'day', 'is_referral_bonus')},
        ),
    ]
