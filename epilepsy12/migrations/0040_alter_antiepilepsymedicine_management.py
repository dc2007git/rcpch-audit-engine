# Generated by Django 4.0.4 on 2022-08-15 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0039_alter_site_hospital_trust'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='management',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilepsy12.management', verbose_name='related management'),
        ),
    ]
