# Generated by Django 4.0.4 on 2022-08-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0049_alter_registration_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='childrens_epilepsy_surgical_service_referral_criteria_met',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name="Have the criteria for referral to a children's epilepsy surgery service been met?"),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='childrens_epilepsy_surgical_service_referral_made',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name="Has a referral to a children's epilepsy surgery service been made?"),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='consultant_paediatrician_input_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Date seen by a consultant paediatrician with expertise in epilepsy.'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='consultant_paediatrician_referral_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Date of referral to a consultant paediatrician with expertise in epilepsy.'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='consultant_paediatrician_referral_made',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has a referral been made to a consultant paediatrician with an interest in epilepsy?'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='epilepsy_specialist_nurse_referral_made',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has a referral to an epilepsy nurse specialist been made?'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='lead_hospital',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='lead_hospital'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='paediatric_neurologist_input_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Date seen by consultant paediatric neurologist.'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='paediatric_neurologist_referral_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Date of referral to a consultant paediatric neurologist.'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='paediatric_neurologist_referral_made',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has a referral to a consultant paediatric neurologist been made?'),
        ),
        migrations.AlterField(
            model_name='epilepsycontext',
            name='diagnosis_of_epilepsy_withdrawn',
            field=models.BooleanField(default=None, null=True, verbose_name='has the diagnosis of epilepsy been withdrawn?'),
        ),
        migrations.AlterField(
            model_name='epilepsycontext',
            name='is_there_a_family_history_of_epilepsy',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Uncertain')], default=None, max_length=3, null=True, verbose_name='is there a family history of epilepsy?'),
        ),
        migrations.AlterField(
            model_name='epilepsycontext',
            name='previous_acute_symptomatic_seizure',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Uncertain')], default=None, max_length=2, null=True, verbose_name='has there been a previous acute symptomatic seizure?'),
        ),
        migrations.AlterField(
            model_name='epilepsycontext',
            name='previous_febrile_seizure',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Uncertain')], default=None, max_length=2, null=True, verbose_name='has there been a previous febrile seizure?'),
        ),
        migrations.AlterField(
            model_name='epilepsycontext',
            name='previous_neonatal_seizures',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Uncertain')], default=None, max_length=2, null=True, verbose_name='were there seizures in the neonatal period?'),
        ),
        migrations.AlterField(
            model_name='initialassessment',
            name='general_paediatrics_referral_made',
            field=models.BooleanField(default=None, null=True, verbose_name='date of referral to general paediatrics'),
        ),
        migrations.AlterField(
            model_name='management',
            name='has_an_aed_been_given',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has an antiepilepsy medicine been prescribed?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='has_individualised_care_plan_been_updated_in_the_last_year',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has the individualised care plan been updated in the last year?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='has_rescue_medication_been_prescribed',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has a rescue medicine been prescribed?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_addresses_sudep',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan address sudden unexplained death in epilepsy?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_addresses_water_safety',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan address water safety?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='On what date was the individualised care plan put in place?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_has_parent_carer_child_agreement',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has the parent or carer and child agreement to an individualised care plan been documented?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_in_place',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Has an individualised care plan been put in place?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_include_first_aid',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan include first aid advice?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_includes_aihp',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan include AIHP?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_includes_ehcp',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan include an educational health care plan (EHCP)?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_includes_general_participation_risk',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan include general participation and risk assessment?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_includes_service_contact_details',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan include service contact details?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='individualised_care_plan_parental_prolonged_seizure_care',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Does the individualised care plan include parental advice on managing prolonged seizures?'),
        ),
        migrations.AlterField(
            model_name='management',
            name='rescue_medication_prescribed',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Which rescue medicine has been prescribed?'),
        ),
    ]