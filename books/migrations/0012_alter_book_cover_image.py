# Generated by Django 4.2.7 on 2024-02-01 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_remove_book_available_for_rent_book_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]