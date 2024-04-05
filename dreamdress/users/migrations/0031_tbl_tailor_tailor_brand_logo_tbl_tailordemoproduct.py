# Generated by Django 4.2.5 on 2024-04-04 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_tailor',
            name='tailor_brand_logo',
            field=models.ImageField(null=True, upload_to='brand_logos/'),
        ),
        migrations.CreateModel(
            name='Tbl_tailorDemoProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('product_image', models.ImageField(upload_to='demo_products/')),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demo_products', to='users.tbl_tailor')),
            ],
        ),
    ]
