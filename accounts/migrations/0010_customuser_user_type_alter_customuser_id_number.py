# Generated by Django 5.0 on 2024-05-05 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20240506_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(default='collaborator', max_length=15),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id_number',
            field=models.CharField(default='6yqnrzl865jc9t2', max_length=15, unique=True),
        ),
    ]