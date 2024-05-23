import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Inserts dummy users from a CSV file into the database'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        with open('accounts/management/commands/User_Dummy_Data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                password = row['password']
                email = row['email']
                introduce = row['introduce']
                mbti = row['mbti']
                updated_at = parse_datetime(row['updated_at'])
                see = row['see'] == 'True'
                is_selected = row['is_selected'] == 'True'
                
                user = User(
                    username=username,
                    email=email,
                    introduce=introduce,
                    mbti=mbti,
                    updated_at=updated_at,
                    see=see,
                    is_selected=is_selected
                )
                user.set_password(password)
                user.save()

        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy users'))
