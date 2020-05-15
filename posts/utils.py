import datetime
import re

from django.utils.html import strip_tags

def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = (count/150.0) #assumes 150wpm read comprehension
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)
