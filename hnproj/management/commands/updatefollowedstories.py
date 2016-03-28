from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import urllib2
import json
from hnproj.models import HNUser
from hnproj.models import HNStory
from hnproj import storyutils
from datetime import datetime
from datetime import timedelta
from datetime import date

# Cron job to find new stories submitted by users
# that we're following.
class Command(BaseCommand):
  # main method to get and store new stories
  def handle(self, *args, **options):
    self.removeOldStories()
    allUsers = HNUser.objects.all()

    currMax = storyutils.get_max_item_id()
    for user in allUsers:
      self.updateStoriesForUser(user)
      user.last_run_max_id = currMax
      user.save()

  # Deletes old stories for users following
  def removeOldStories(self):
    stories = HNStory.objects.all()
    for story in stories:
      jsonStory = json.loads(story.storyJSON)
      oldTime = jsonStory.get("time")
      # handle case oldTime is NoneType
      if not oldTime:
        story.delete()
        continue
      secs = int(jsonStory.get("time"))
      storyDate = datetime.fromtimestamp(secs);
      if ((date.today() - timedelta(days=30)) > storyDate.date()):
        story.delete()

     
  # Finds new stories for the user
  def updateStoriesForUser(self, hnuser):
    maxId = hnuser.last_run_max_id
    updatedUser = self.get_user_data(hnuser.username)
    itemsSince = []
    # find items since our last run - maxId
    # after this itemsSince will contain HN ids of new
    # stories and comments, etc
    for id in updatedUser["submitted"]:
      if id > maxId:
        itemsSince.append(id)
    # now find just the submitted stories and save those
    # to the db.
    for id in itemsSince:
      item = storyutils.get_item(id)
      if not item:
        continue
      if storyutils.is_story(item) and not storyutils.is_deleted(item):
        storyItem = HNStory(hnStoryId = int(id), hnUserId = hnuser.user_id, storyJSON = json.dumps(item, cls=DjangoJSONEncoder))
        storyItem.save()

  
  # Returns the json of the HN user requesting it from the API
  def get_user_data(self, username):
    url = 'https://hacker-news.firebaseio.com/v0/user/' + username + '.json'
    userResp = urllib2.urlopen(url)
    userjson = json.load(userResp)
    return userjson
     
