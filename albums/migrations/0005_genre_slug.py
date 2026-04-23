from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Genre = apps.get_model('albums', 'Genre')
    for genre in Genre.objects.all():
        genre.slug = slugify(genre.name)
        genre.save()


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0004_album_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True, default='', unique=False),
        ),
        migrations.RunPython(populate_slugs),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]