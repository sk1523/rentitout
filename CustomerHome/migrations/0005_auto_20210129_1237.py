# Generated by Django 3.0.4 on 2021-01-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerHome', '0004_customer_customer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_age',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_gender',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_license',
            field=models.ImageField(upload_to='img/Customer_License/'),
        ),
    ]
