from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_film_work_certificate_file_path_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filmwork',
            options={'verbose_name': 'Filmwork', 'verbose_name_plural': 'Filmwork'},
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.Person'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='certificate',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='certificate'),
        ),
    ]
