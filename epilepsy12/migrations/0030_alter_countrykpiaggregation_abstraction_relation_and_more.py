# Generated by Django 4.2.4 on 2023-08-22 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("epilepsy12", "0029_nationalkpiaggregation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="countrykpiaggregation",
            name="abstraction_relation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="epilepsy12.onscountryentity",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="countrykpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name="icbkpiaggregation",
            name="abstraction_relation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="epilepsy12.integratedcareboardentity",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="icbkpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name="nationalkpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name="nhsregionkpiaggregation",
            name="abstraction_relation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="epilepsy12.nhsregionentity",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="nhsregionkpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name="openukkpiaggregation",
            name="abstraction_relation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="epilepsy12.openuknetworkentity",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="openukkpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name="organisationkpiaggregation",
            name="abstraction_relation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="epilepsy12.organisation",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="organisationkpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name="trustkpiaggregation",
            name="abstraction_relation",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="trustkpiaggregation",
            name="cohort",
            field=models.PositiveSmallIntegerField(default=None, unique=True),
        ),
    ]
