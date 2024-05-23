from django.core.management.base import BaseCommand
from movies.models import Comment

class Command(BaseCommand):
    help = 'Deletes all dummy comments from the database'

    def handle(self, *args, **kwargs):
        dummy_comments = Comment.objects.filter(movie_id=823464)
        count = dummy_comments.count()
        dummy_comments.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} dummy comments'))
