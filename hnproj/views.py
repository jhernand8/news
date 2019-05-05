from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django import http
from django.template import RequestContext, loader
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from urllib.request import urlopen
import json
from json import JSONEncoder
from hnproj.models import HNUser
from hnproj.models import HNStory
from hnproj.models import HNTopStory
from hnproj.models import TopStoryIdsByTime

def home(request):
    HNUser.objects.all()
    return http.HttpResponse('Hello World test!')
def users(request):
    user_list = HNUser.objects.all()
    if not user_list:
        jh = HNUser(username = 'nkzednan', last_run_max_id = 8000000)
        jh.save()
        k = HNUser(username = 'kogir', last_run_max_id = 8000000);
        k.save()
    return render(request, 'hn_users.html', {'users': user_list});

def clear_out_users(request):
    users = HNUser.objects.all()
    for u in users:
        u.delete();
    return http.HttpResponse("Deleted all users.");
    
def get_max_item_id():
    maxItemUrl = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
    maxItemData = json.load(urlopen(maxItemUrl))
    return long(maxItemData);

# Logic for page to view the stories submitted by users following.
def newsByUser(request):
    user_list = HNUser.objects.order_by("username").all()
    stories = HNStory.objects.order_by("-hnStoryId").all()

    usersToStories = {}
    
    usernames = []
    for user in user_list:
      userStories = []
      for story in stories:
        if story.hnUserId == user.user_id:
          userStories.append(json.loads(story.storyJSON))
      usersToStories[user.username] = userStories
      usernames.append(user.username)

    context = {
               'users': mark_safe(json.dumps(usernames, cls=DjangoJSONEncoder)),
               'storiesByUser': mark_safe(json.dumps(usersToStories, cls=DjangoJSONEncoder))}
    return render(request, 'userStories.html', context)

# requests the item with the given id, return the json object.
def get_item(item_id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(item_id) + '.json'
    return json.load(urlopen(url))

def is_story(item_json):
    return "story" == item_json.get('type')

def is_deleted(item_json):
    return True == item_json.get('deleted')

def get_item_list_since(last_id, userjson):
    items = []
    for id in userjson["submitted"]:
      if id > last_id:
        items.append(id)
    return items

def get_user_data(username):
       url = 'https://hacker-news.firebaseio.com/v0/user/' + username + '.json'
       userResp = urlopen(url)
       userjson = json.load(userResp)
       return userjson

def follow_user(request):
    usernames = request.POST.getlist('hnUsername')
    curr_max_id = get_max_item_id()
    users = ""
    for username in usernames:
        if ((not username) or username == ""):
            continue
        # start out a little bit before the current max to see items from recently
        hnuser = HNUser(username, curr_max_id - 20000);
        hnuser.save();
        users += username + ", "
    return http.HttpResponse("now following user(s): " + users);

def update_top_items(request):
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json';
    data = json.load(urlopen(url));
    jsonStr = json.dumps(data);
    topIdsObj = TopStoryIdsByTime(storyIds = data);
    topIdsObj.save();
    return http.HttpResponse("updated");

# removes top stories from the db.
def remove_top_items(request):
    ids = request.POST.getlist('storyId');
    allTopStories = HNTopStory.objects.all();
    delCount = 0;
    i = "ids: ";
    for si in ids:
        i = i + " " + str(si) + " " + str(type(si)) + " ";
    for story in allTopStories:
        storyId = story.hnStoryId
        if str(storyId) in ids or storyId in ids:
            story.marked_deleted = True
            story.save()
            delCount = delCount + 1;
    return redirect("/topStories");

