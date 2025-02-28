# Generated by Django 4.2.8 on 2024-05-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_movies',
            field=models.ManyToManyField(related_name='like_users', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='user',
            name='recent_watched_movie',
            field=models.ManyToManyField(related_name='watched_users', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='user',
            name='recommendation_movie',
            field=models.ManyToManyField(related_name='recommended_users', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
