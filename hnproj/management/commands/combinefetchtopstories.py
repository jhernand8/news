from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import urllib2
import json
from hnproj.models import TopStoryIdsByTime
from hnproj.models import HNStory
from hnproj.models import HNTopStory
from hnproj import storyutils
from sets import Set

# Cron job that looks at the top story ids that we have saved
# and combines them into a single list
# and fetches the stories saving them to the db in
# as HNTopStory.
class Command(BaseCommand):
  def handle(self, *args, **options):
    prevTop = HNTopStory.objects.all()

    topIds = TopStoryIdsByTime.objects.all()
    uniqueIds = Set()
    for topIdsForTime in topIds:
      ids = json.loads(topIdsForTime.storyIds)
      for currid in ids:
        uniqueIds.add(int(currid))
    print "number of unique ids: " + str(len(uniqueIds)) + ".\n"
 
    # remove previous top ones that are in the current set
    for prevStory in prevTop:
      previd = json.loads(prevStory.story).get('id')
      if int(previd) in uniqueIds:
        prevStory.delete()
    # now fetch stories
    for id in uniqueIds:
      story = storyutils.get_item(id)
      if storyutils.is_deleted(story):
        continue
      score = story.get('score')
      if score == 1:
        continue
      topStory = HNTopStory(hnStoryId = int(id), story = json.dumps(story, cls=DjangoJSONEncoder))
      topStory.save()
