from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import urllib2
import json
from hnproj.models import TopStoryIdsByTime
from hnproj.models import HNStory
from hnproj.models import HNTopStory
from hnproj import storyutils
from sets import Set
from datetime import date
from datetime import datetime
from datetime import timedelta

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
        try:
          uniqueIds.add(int(currid))
        except:
          pass;
    print "number of unique ids: " + str(len(uniqueIds)) + ".\n"
 
    # remove previous top ones that are in the current set
    for prevStory in prevTop:
      previd = json.loads(prevStory.story).get('id')
      if int(previd) in uniqueIds:
        prevStory.delete()
    # now fetch stories
    for id in uniqueIds:
      story = storyutils.get_item(id)
      try:
        if storyutils.is_deleted(story):
          continue
      except:
        continue;
      score = story.get('score')
      if score == 1:
        continue
      topStory = HNTopStory(hnStoryId = int(id), story = json.dumps(story, cls=DjangoJSONEncoder))
      topStory.save()

    # now delete top ids
    for topIdsForTime in TopStoryIdsByTime.objects.all():
      topIdsForTime.delete()

    # also remove old top stories, ie more than n days old
    for prevStory in prevTop:
      if int(json.loads(prevStory.story).get('id')) in uniqueIds:
        continue
      daysOld = timedelta(days = 3)
      if (prevStory.date + daysOld) < date.today():
        prevStory.delete()
      # also delete stories based on submission date - as sometimes these
      # will later make it back into the top 100 stories
      else:
        storyTime = int(json.loads(prevStory.story).get('time'))
        storyDate = datetime.fromtimestamp(storyTime).date()
        if (storyDate + daysOld + daysOld) < date.today():
          prevStory.delete()


