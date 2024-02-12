# Generated by Django 4.2.5 on 2024-02-12 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_mycart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_items',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cart_items',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cart_items',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mycart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='mycart',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.RemoveField(
            model_name='product_images',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='tbl_user',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('seller', 'Seller'), ('admin', 'Admin'), ('tailor', 'Tailor')], default='customer', max_length=10),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Cart_items',
        ),
        migrations.DeleteModel(
            name='category',
        ),
        migrations.DeleteModel(
            name='MYcart',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='product_images',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]