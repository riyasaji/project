# Generated by Django 4.2.5 on 2024-03-18 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_tbl_brand_brand_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbl_product',
            old_name='brand_name',
            new_name='brand',
        ),
    ]
