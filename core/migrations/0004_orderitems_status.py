# Generated by Django 4.0 on 2022-07-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_order_orderitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='status',
            field=models.CharField(default='Ordered', max_length=255),
        ),
    ]