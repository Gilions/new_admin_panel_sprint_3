from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_film_work_persons_certificate_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(choices=[('actor', 'Актер'), ('director', 'Директор'), ('writer', 'Сценарист')], default='actor', verbose_name='role'),
        ),
    ]
