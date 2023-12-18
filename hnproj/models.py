from django.db import models

#
class HNStory(models.Model):
  storyJSON = models.TextField()
  hnUserId = models.IntegerField()
  hnStoryId = models.IntegerField(unique = True, primary_key = True)

# object for storing the list of top HN story ids as of a given time.
class TopStoryIdsByTime(models.Model):
  storyIds = models.TextField()
  topTime = models.DateTimeField(auto_now = True, unique = True, primary_key = True)

# Object for storing a top story from HN.
class HNTopStory(models.Model):
  hnStoryId = models.IntegerField(unique = True, primary_key = True)
  date = models.DateField(auto_now = True)
  story = models.TextField()
  marked_deleted = models.BooleanField(default = False)
