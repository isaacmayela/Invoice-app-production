# Generated by Django 5.0 on 2024-05-05 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_article_id_number_alter_company_id_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id_number',
            field=models.CharField(default='5404tu127h0v2xi', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='id_number',
            field=models.CharField(default='xzpzpfodane9jpb', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id_number',
            field=models.CharField(default='8m774w0u8fp802v', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='id_number',
            field=models.CharField(default='okngc9eopgoll1e', max_length=15, unique=True),
        ),
    ]