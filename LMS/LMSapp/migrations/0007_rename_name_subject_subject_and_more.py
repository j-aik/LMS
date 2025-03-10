# Generated by Django 5.0.4 on 2025-03-08 03:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMSapp', '0006_remove_customuser_designation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='name',
            new_name='subject',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='subjects_assigned',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='class_assigned',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='teacher',
        ),
        migrations.AddField(
            model_name='staff',
            name='class_assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LMSapp.classst'),
        ),
        migrations.AddField(
            model_name='staff',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LMSapp.subject'),
        ),
    ]
