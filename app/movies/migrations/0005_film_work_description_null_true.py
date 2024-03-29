# Generated by Django 3.2 on 2022-04-21 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_person_film_work_role_null_false'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(choices=[('actor', 'Актер'), ('director', 'Режиссер'), ('writer', 'Сценарист')], default='actor', verbose_name='role'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['created'], name='person_creation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work', 'person', 'role'], name='film_work_person_idx_role'),
        ),
    ]
