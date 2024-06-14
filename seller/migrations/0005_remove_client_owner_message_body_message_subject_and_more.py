# Generated by Django 5.0.6 on 2024-06-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_alter_newsletter_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='owner',
        ),
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='periodicity',
            field=models.CharField(choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('daily', 'Daily')], default='weekly', max_length=20),
        ),
    ]