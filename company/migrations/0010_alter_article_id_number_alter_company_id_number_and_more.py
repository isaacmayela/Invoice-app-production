# Generated by Django 5.0 on 2024-05-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_alter_article_id_number_alter_company_id_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id_number',
            field=models.CharField(default='kp00si0umpminx8', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='id_number',
            field=models.CharField(default='', editable=False, max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id_number',
            field=models.CharField(default='o74oe9ykl67ux0h', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='id_number',
            field=models.CharField(default='wh7w7ba6u6jgxhy', max_length=15, unique=True),
        ),
    ]
