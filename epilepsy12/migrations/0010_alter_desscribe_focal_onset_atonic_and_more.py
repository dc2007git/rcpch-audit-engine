# Generated by Django 4.0.4 on 2022-05-22 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0009_alter_desscribe_relevant_impairments_behavioural_educational'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_atonic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_automatisms',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_autonomic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_behavioural_arrest',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_centrotemporal',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_clonic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_cognitive',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_emotional',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_epileptic_spasms',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_focal_to_bilateral_tonic_clonic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_frontal',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_gelastic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_hyperkinetic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_impaired_awareness',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_left',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_myoclonic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_occipital',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_other',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_parietal',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_right',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_sensory',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_temporal',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='focal_onset_tonic',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='non_epileptic_seizure_type',
            field=models.CharField(blank=True, choices=[('SAS', 'Syncope And Anoxic Seizures'), ('BPP', 'Behavioral Psychological And Psychiatric Disorders'), ('SRC', 'Sleep Related Conditions'), ('PMD', 'Paroxysmal Movement Disorders'), ('MAD', 'Migraine Associated Disorders'), ('ME', 'Miscellaneous Events'), ('Oth', 'Other')], default=None, max_length=3, null=True),
        ),
    ]