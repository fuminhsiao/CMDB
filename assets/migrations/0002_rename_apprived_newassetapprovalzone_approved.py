# Generated by Django 4.0.5 on 2022-07-01 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newassetapprovalzone',
            old_name='apprived',
            new_name='approved',
        ),
    ]