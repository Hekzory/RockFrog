from django.core.management.base import BaseCommand, CommandError
from news_feed.models import NewsFeedArticlesList

class Command(BaseCommand):	
    def handle(self, *args, **options):
    	if NewsFeedArticlesList.objects.filter(list_type='best').exists():
    		best_articles_list = NewsFeedArticlesList.objects.get(list_type='best')
    		best_articles_list.generate_articles(days=4, limit=30)

    	if NewsFeedArticlesList.objects.filter(list_type='hot').exists():
    		best_articles_list = NewsFeedArticlesList.objects.get(list_type='hot')
    		best_articles_list.generate_articles(days=1, limit=25)