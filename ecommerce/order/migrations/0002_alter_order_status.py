# Generated by Django 4.1.2 on 2022-12-30 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='Confirmed', max_length=150),
        ),
    ]
