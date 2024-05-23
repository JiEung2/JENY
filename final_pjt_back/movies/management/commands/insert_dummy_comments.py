import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from movies.models import Movie, Comment
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Inserts dummy comments from a CSV file into the database'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        file_path = 'movies/management/commands/Comments_Dummy_Data.csv'  # 실제 CSV 파일 경로로 변경
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                content = row['content']
                created_at = parse_datetime(row['created_at'])
                movie_id = int(row['movie_id'])
                user_id = int(row['user_id'])

                movie = Movie.objects.get(id=movie_id)
                user = User.objects.get(id=user_id)

                Comment.objects.create(
                    content=content,
                    created_at=created_at,
                    movie=movie,
                    user=user
                )

        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy comments'))
