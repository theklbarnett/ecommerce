# Generated by Django 2.2 on 2020-04-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200413_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_photo',
            field=models.ImageField(upload_to='product_images'),
        ),
    ]