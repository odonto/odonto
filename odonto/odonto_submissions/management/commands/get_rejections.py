"""
Get's a csv of episodes that cannot be processed by compass
"""
import csv
import os


FILE_NAME = os.path.join("..", "rejections.csv")

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pass