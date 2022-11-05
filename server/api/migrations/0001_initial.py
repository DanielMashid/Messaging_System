# Generated by Django 4.0.8 on 2022-11-05 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(help_text='The subject of the message.', max_length=180)),
                ('message_content', models.CharField(max_length=1000)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(help_text='The receiver of message.', on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(help_text='The sender of the message.', on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
