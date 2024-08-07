from django.core.management.base import BaseCommand
from rewards.models import DailyReward

class Command(BaseCommand):
    help = 'Populates the DailyReward model with initial data'

    def handle(self, *args, **kwargs):
        rewards = [
            (1, 500), (2, 1000), (3, 1500), (4, 2000),
            (5, 2500), (6, 3000), (7, 3500), (8, 4000),
            (9, 4500), (10, 5500), (11, 6000), (12, 8000)
        ]

        for day, amount in rewards:
            DailyReward.objects.get_or_create(day=day, amount=amount)

        self.stdout.write(self.style.SUCCESS('Successfully populated daily rewards'))