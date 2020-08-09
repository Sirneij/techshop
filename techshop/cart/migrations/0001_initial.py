# Generated by Django 3.0.5 on 2020-05-05 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(db_index=True, max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'cart_items',
                'ordering': ['date_added'],
            },
        ),
    ]
