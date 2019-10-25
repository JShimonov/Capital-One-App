from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
import re

'''
questions = [
    {
        "id":11510,
        "title":"pair of dice, lost",
        "clues_count":5
    },
    {
        "id":11531,
        "title":"mixed bag",
        "clues_count":5
    }
]
'''


def home(request):
    req = 'http://jservice.io/api/random?count=12'
    response = requests.get(req)
    trivia_set = response.json()
    content = []
    for trivia in trivia_set:
        dict = { 'id': trivia['id'], 'question' : trivia['question'], 'answer' : trivia['answer'], 'category' : trivia['category']['title']}
        content.append(dict)
    return render(request, 'trivia/home.html', {'trivia':content})


def about(request):
    return render(request, 'trivia/about.html')

def categories(request):
    return render(request, 'trivia/categories.html')
