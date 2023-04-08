# Generated by Django 4.2 on 2023-04-07 21:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("epilepsy12", "0067_remove_historicalsyndrome_syndrome_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsyndromeentity",
            name="syndrome_name",
            field=models.CharField(
                blank=True,
                default=None,
                help_text={
                    "label": "The name of a given syndrome",
                    "reference": "The name of a given syndrome",
                },
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="syndromeentity",
            name="syndrome_name",
            field=models.CharField(
                blank=True,
                default=None,
                help_text={
                    "label": "The name of a given syndrome",
                    "reference": "The name of a given syndrome",
                },
                null=True,
            ),
        ),
    ]