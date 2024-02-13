# Generated by Django 4.2.5 on 2024-02-12 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_tbl_seller_seller_business_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_bank_account_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_bank_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_brand_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_district',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_firstname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_gst_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_ifsc_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_lastname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_pan_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_pincode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_seller',
            name='seller_state',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
