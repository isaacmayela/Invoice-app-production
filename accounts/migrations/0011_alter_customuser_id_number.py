# Generated by Django 5.0 on 2024-05-10 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_customuser_user_type_alter_customuser_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id_number',
            field=models.CharField(default='cfsaa72i3uyf17k', max_length=15, unique=True),
        ),
    ]