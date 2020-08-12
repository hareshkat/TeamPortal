# Generated by Django 3.0.6 on 2020-07-03 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import isr_tracking.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IsrTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsrNumber', models.CharField(max_length=20, unique=True, verbose_name='ISR Number')),
                ('RequestCategory', models.CharField(choices=[('assessment', 'Assessment'), ('finding', 'Finding'), ('exception', 'Exception')], max_length=20, verbose_name='Request Category')),
                ('IsrStatus', models.CharField(choices=[('open', 'Open'), ('wip', 'Work In Progress'), ('closed', 'Closed'), ('discard', 'Discard')], max_length=20, verbose_name='ISR Status')),
                ('Description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('LmsInstance', models.CharField(blank=True, choices=[('emp_lms', 'Employee LMS'), ('partner_lms', 'Partner LMS'), ('tech_lms', 'Tech LMS')], max_length=20, verbose_name='LMS Instance')),
                ('FindingEnv', models.CharField(blank=True, choices=[('sit', 'SIT'), ('replica', 'Replica'), ('production', 'Production')], max_length=20, verbose_name='Finding Environment')),
                ('SevirityLevel', models.CharField(blank=True, choices=[('low', 'Low(1)'), ('medium', 'Medium(2)'), ('high', 'High(3)')], max_length=20, verbose_name='Sevirity Level')),
                ('RequestDate', models.DateField(blank=True, null=True, verbose_name='Request Date')),
                ('ClosingDate', models.DateField(blank=True, null=True, verbose_name='Closing Date')),
                ('FeatureDefectNumber', models.CharField(blank=True, max_length=20, null=True, verbose_name='Feature/Defect Number')),
                ('Assignee', models.ManyToManyField(blank=True, to='account.TeamMember')),
            ],
            options={
                'verbose_name': 'ISR',
                'verbose_name_plural': 'ISR',
            },
        ),
        migrations.CreateModel(
            name='IsrUsefulDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Documents', models.FileField(blank=True, upload_to=isr_tracking.models.isr_doc_directory_path, verbose_name='Attachments/Supporting Documents')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='isr_tracking.IsrTracking')),
            ],
        ),
        migrations.CreateModel(
            name='IsrTaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaskId', models.CharField(blank=True, max_length=20, unique=True, verbose_name='Task Id')),
                ('TaskCategory', models.CharField(blank=True, choices=[('app_sec_assessment', 'App. Security Assessment'), ('eqxe_request', 'Exception Request'), ('privacy_assessment', 'Privacy Assessment (App/Device)'), ('infra_assessment', 'Infrastructure Assessment'), ('other', 'Other')], max_length=50, verbose_name='Task Category')),
                ('TaskStatus', models.CharField(blank=True, choices=[('open', 'Open'), ('closed', 'Closed'), ('discard', 'Discard')], max_length=50, verbose_name='Task Status')),
                ('TaskAssignee', models.CharField(blank=True, max_length=100, verbose_name='Task Spoc person/Team')),
                ('TargetClosureDate', models.DateField(blank=True, null=True, verbose_name='Task Closure Date')),
                ('IsrNumber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='isr_tracking.IsrTracking')),
            ],
            options={
                'verbose_name': 'ISR - Task',
                'verbose_name_plural': 'ISR - Tasks',
            },
        ),
        migrations.CreateModel(
            name='HistoricalIsrTracking',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('IsrNumber', models.CharField(db_index=True, max_length=20, verbose_name='ISR Number')),
                ('RequestCategory', models.CharField(choices=[('assessment', 'Assessment'), ('finding', 'Finding'), ('exception', 'Exception')], max_length=20, verbose_name='Request Category')),
                ('IsrStatus', models.CharField(choices=[('open', 'Open'), ('wip', 'Work In Progress'), ('closed', 'Closed'), ('discard', 'Discard')], max_length=20, verbose_name='ISR Status')),
                ('Description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('LmsInstance', models.CharField(blank=True, choices=[('emp_lms', 'Employee LMS'), ('partner_lms', 'Partner LMS'), ('tech_lms', 'Tech LMS')], max_length=20, verbose_name='LMS Instance')),
                ('FindingEnv', models.CharField(blank=True, choices=[('sit', 'SIT'), ('replica', 'Replica'), ('production', 'Production')], max_length=20, verbose_name='Finding Environment')),
                ('SevirityLevel', models.CharField(blank=True, choices=[('low', 'Low(1)'), ('medium', 'Medium(2)'), ('high', 'High(3)')], max_length=20, verbose_name='Sevirity Level')),
                ('RequestDate', models.DateField(blank=True, null=True, verbose_name='Request Date')),
                ('ClosingDate', models.DateField(blank=True, null=True, verbose_name='Closing Date')),
                ('FeatureDefectNumber', models.CharField(blank=True, max_length=20, null=True, verbose_name='Feature/Defect Number')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical ISR',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
