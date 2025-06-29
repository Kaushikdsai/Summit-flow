# Generated by Django 5.2.1 on 2025-06-01 12:24

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_emailsettings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailsettings',
            old_name='email_port',
            new_name='port',
        ),
        migrations.RenameField(
            model_name='emailsettings',
            old_name='email_use_tls',
            new_name='use_tls',
        ),
        migrations.RemoveField(
            model_name='emailsettings',
            name='email_host',
        ),
        migrations.RemoveField(
            model_name='emailsettings',
            name='email_host_password',
        ),
        migrations.RemoveField(
            model_name='emailsettings',
            name='email_host_user',
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='password',
            field=models.CharField(default='default_password', max_length=128),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='smtp_server',
            field=models.CharField(default='default_smtp_server', max_length=100),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='username',
            field=models.CharField(default='default_username', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_when', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user')),
            ],
        ),
    ]
