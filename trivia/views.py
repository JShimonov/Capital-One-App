from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests

def home(request):
    req = 'http://jservice.io/api/random?count=8'
    response = requests.get(req)
    trivia_set = response.json()
    content = []
    for trivia in trivia_set:
        dict = {'id': trivia['id'], 'question' : trivia['question'], 'answer' : trivia['answer'], 'category' : trivia['category']['title']}
        content.append(dict)
    return render(request, 'trivia/home.html', {'trivia':content})

def categories(request):
    req = 'http://jservice.io/api/categories?100'
    response = requests.get(req)
    category_set = response.json()
    content = []
    for category in category_set:
        dict = {'id': category['id'], 'title': category['title'], 'clues_count': category['clues_count']}
        content.append(dict)
    return render(request, 'trivia/categories.html', {'categories':content})

def results(request):
    return render(request, 'trivia/results.html')



def about(request):
    return render(request, 'trivia/about.html')
