from django.shortcuts import render
from django.http import HttpResponse
from django import http
from django.template import RequestContext, loader
import urllib2
import json
from hnproj.models import HNUser
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
    template = loader.get_template('hn_users.html')
    context = RequestContext(request, {
               'users': user_list})
    return http.HttpResponse(template.render(context))

def clear_out_users(request):
    users = HNUser.objects.all()
    for u in users:
        u.delete();
    return http.HttpResponse("Deleted all users.");
    
def get_max_item_id():
    maxItemUrl = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
    maxItemData = json.load(urllib2.urlopen(maxItemUrl))
    return long(maxItemData);

def newsByUser(request):
    user_list = HNUser.objects.all()
    # max item id: 
    maxItemData = get_max_item_id()
    
    stories = []
    for user in user_list:
        userdata = get_user_data(user.username)
        new_items = get_item_list_since(user.last_run_max_id, userdata)
        for item_id in new_items:
            itemJSON = get_item(item_id)
            if (not is_deleted(itemJSON)) and is_story(itemJSON):
                stories.append(itemJSON)       
    template = loader.get_template('hn_users.html')
    context = RequestContext(request, {
               'users': user_list,
               'maxData': maxItemData,
               'stories': stories})
    # update the max id as we just showed that user's data
    # increment it by half, so that we will see most recent items
    # again but always increasing the id
    for userhn in user_list:
        diffid = long(maxItemData) - userhn.last_run_max_id
        userhn.last_run_max_id += int(diffid/2);
        userhn.save();
    return http.HttpResponse(template.render(context))

# requests the item with the given id, return the json object.
def get_item(item_id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(item_id) + '.json'
    return json.load(urllib2.urlopen(url))

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
       userResp = urllib2.urlopen(url)
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
    data = json.load(urllib2.urlopen(url));
    jsonStr = json.dumps(data);
    topIdsObj = TopStoryIdsByTime(storyIds = data);
    topIdsObj.save();
    return http.HttpResponse("updated");


