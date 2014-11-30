from django.shortcuts import render
from django.http import HttpResponse
from django import http
from django.template import RequestContext, loader
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import urllib2
import json
from json import JSONEncoder
from hnproj.models import HNUser
from hnproj.models import HNStory
from hnproj.models import TopStoryIdsByTime
from hnproj.models import HNTopStory

def home(request):
  topStories = HNTopStory.objects.all()
  storyJSONs = []
  for story in topStories:
    storyJSONs.append(json.loads(story.story))
  # sort by score
  stories = sorted(storyJSONs, key=lambda st: int(st.get('score')));
  template = loader.get_template('topstories.html')
  context = RequestContext(request, {
               'allStories': mark_safe(json.dumps(stories, cls=DjangoJSONEncoder))
            })
  return http.HttpResponse(template.render(context))
