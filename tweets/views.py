from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.views.generic import View
from django.shortcuts import render
from user_profile.models import User
from tweets.models import Tweet, HashTag
from tweets.forms import TweetForm, SearchForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
import json


class Index(View):
    def get(self, request):
        params = {}
        params["name"] = "Django"
        return render(request, 'base.html', params)


class Profile(View):
    """User Profile page reachable from /user/<username> URL"""

    def get(self, request, username):
        params = dict()
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        form = TweetForm
        params["tweets"] = tweets
        params["user"] = user
        params["form"] = form
        return render(request, 'profile.html', params)


class PostTweet(View):
    """Tweet Post form available on page /user/<username> URL"""

    def post(self, request, username):
        form = TweetForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            # tweet = Tweet(text=form.cleaned_data['text'],user=user,country=form.cleaned_data['country'])
            tweet = Tweet(text=form.cleaned_data['text'], user=user)
            tweet.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word[0] == "#":
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
        return HttpResponseRedirect('/user/' + username)


class HashTagCloud(View):
    """Hash Tag  page reachable from /hastag/<hashtag> URL"""

    def get(self, request, hashtag):
        params = dict()
        hashtag = HashTag.objects.get(name=hashtag)
        params["tweets"] = hashtag.tweet
        return render(request, 'hashtag.html', params)


class Search(View):
    """Search all tweets with query /search/?query=<query> URL"""

    def get(self, request):
        form = SearchForm()
        params = dict()
        params["search"] = form

        return render(request, 'search.html', params)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query)
            context = {"query": query, "tweets": tweets}
            return_str = render_to_string('partials/_tweet_search.html',
                                      context)
            return HttpResponse(json.dumps(return_str),
                        content_type="application/json")
        else:
            HttpResponseRedirect("/search")
