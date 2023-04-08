# Generated by Django 4.2 on 2023-04-08 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("epilepsy12", "0079_alter_comorbidityentity_conceptid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comorbidity",
            name="comorbidity",
            field=models.ForeignKey(
                default=None,
                help_text={
                    "label": "What is the comorbidity?",
                    "reference": "What is the comorbidity?",
                },
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="epilepsy12.comorbidityentity",
            ),
        ),
    ]