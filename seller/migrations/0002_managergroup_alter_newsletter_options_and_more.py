# Generated by Django 5.0.6 on 2024-06-10 19:42

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('seller', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
            ],
            options={
                'permissions': [('custom_view_newsletter', 'Может просматривать любой новостной бюллетень'), ('view_users', 'Может просматривать список пользователей сервиса'), ('block_users', 'Может заблокировать пользователей сервиса'), ('disable_newsletter', 'Может отключить новостные бюллетени')],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('custom_view_newsletter', 'Может просматривать любой новостной бюллетень'), ('view_users', 'Может просматривать список пользователей сервиса'), ('block_users', 'Может заблокировать пользователей сервиса'), ('disable_newsletter', 'Может отключить новостные бюллетени')]},
        ),
        migrations.AddField(
            model_name='newsletter',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='newsletters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
