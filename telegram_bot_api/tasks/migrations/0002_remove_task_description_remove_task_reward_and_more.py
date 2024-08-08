# Generated by Django 5.1 on 2024-08-08 00:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
        migrations.RemoveField(
            model_name='task',
            name='reward',
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('SOCIAL', 'Social'), ('BONUS', 'Bonus'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='rewards',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'task')},
            },
        ),
    ]
