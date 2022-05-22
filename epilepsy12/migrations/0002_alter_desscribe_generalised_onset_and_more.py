# Generated by Django 4.0.4 on 2022-05-20 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desscribe',
            name='generalised_onset',
            field=models.CharField(choices=[('TCl', 'Tonic-clonic'), ('Clo', 'Clonic'), ('Ton', 'Tonic'), ('MyC', 'Myoclonic'), ('MTC', 'Myoclonic-tonic-clonic'), ('MAt', 'Myoclonic-atonic'), ('Ato', 'Atonic'), ('EpS', 'Epileptic spasms'), ('TAb', 'Typical absence'), ('Aab', 'Atypical absence'), ('MAb', 'Myoclonic absence'), ('AEM', 'Absence with eyelid myoclonia'), ('Oth', 'Other')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_behavioural',
            field=models.CharField(choices=[('a', 'Daydreaming /inattention'), ('b', 'Infantile gratification'), ('c', 'Eidetic imagery'), ('d', 'Tantrums and rage reactions'), ('e', 'Out of body experiences'), ('f', 'Panic attacks'), ('g', 'Dissociative states'), ('h', 'Non-epileptic seizures'), ('i', 'Hallucinations in psychiatric disorders'), ('j', 'Fabricated / factitious illness')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_migraine',
            field=models.CharField(choices=[('a', 'Migraine with visual aura'), ('b', 'Familial hemiplegic migraine'), ('c', 'Benign paroxysmal torticollis'), ('d', 'Benign paroxysmal vertigo'), ('e', 'Cyclical vomiting')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_miscellaneous',
            field=models.CharField(choices=[('a', 'Benign myoclonus of infancy and shuddering attacks'), ('b', 'Jitteriness'), ('c', 'Sandifer syndrome'), ('d', 'Non-epileptic head drops'), ('e', 'Spasmus nutans'), ('f', 'Raised intracranial pressure'), ('g', 'Paroxysmal extreme pain disorder'), ('h', 'Spinal myoclonus')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_other',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_paroxysmal',
            field=models.CharField(choices=[('a', 'Tics'), ('b', 'Stereotypies'), ('c', 'Paroxysmal kinesigenic dyskinesia'), ('d', 'Paroxysmal nonkinesigenic dyskinesia'), ('e', 'Paroxysmal exercise induced dyskinesia'), ('f', 'Benign paroxysmal tonic upgaze'), ('g', 'Episodic ataxias'), ('h', 'Alternating hemiplegia'), ('i', 'Hyperekplexia'), ('j', 'Opsoclonus-myoclonus syndrome')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_sleep',
            field=models.CharField(choices=[('a', 'Sleep related rhythmic movement disorders'), ('b', 'Hypnogogic jerks'), ('c', 'Parasomnias'), ('d', 'REM sleep disorders'), ('e', 'Benign neonatal sleep myoclonus'), ('f', 'Periodic leg movements'), ('g', 'Narcolepsy-cataplexy')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_syncope',
            field=models.CharField(choices=[('a', 'Vasovagal syncope'), ('b', 'Reflex anoxic seizures'), ('c', 'Breath-holding attacks'), ('d', 'Hyperventilation syncope'), ('e', 'Compulsive valsalva'), ('f', 'Neurological syncope'), ('g', 'Imposed upper airways obstruction'), ('h', 'Orthostatic intolerance'), ('i', 'Long QT and cardiac syncope'), ('j', 'Hyper-cyanotic spells')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='desscribe',
            name='nonepileptic_seizure_unknown_onset',
            field=models.CharField(choices=[('TCl', 'Tonic-clonic'), ('EpS', 'Epileptic spasms'), ('BAr', 'Behaviour arrest'), ('Oth', 'Other')], default=None, max_length=3, null=True),
        ),
    ]
