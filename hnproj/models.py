from django.db import models

# Object for a user on Hacker News - the username and the max 
# id shown for stories by this user that shown when viewing stories
# by uses following.
class HNUser(models.Model):
  username = models.TextField(unique=True)
  last_run_max_id = models.IntegerField()
  user_id = models.AutoField(primary_key = True)
#
class HNStory(models.Model):
  storyJSON = models.TextField()
  hnUserId = models.IntegerField()
  hnStoryId = models.IntegerField(unique = True, primary_key = True)

# object for storing the list of top HN story ids as of a given time.
class TopStoryIdsByTime(models.Model):
  storyIds = models.TextField()
  topTime = models.DateTimeField(auto_now = True, auto_now_add = True, unique = True, primary_key = True)

# Object for storing a top story from HN.
class HNTopStory(models.Model):
  hnStoryId = models.IntegerField(unique = True, primary_key = True)
  date = models.DateField(auto_now = True, auto_now_add = True)
  story = models.TextField()
  markedDeleted = models.BooleanField(default = False)
