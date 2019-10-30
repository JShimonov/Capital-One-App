from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from trivia.searchtags import searchform

import random
import requests

def home(request):
    req = 'http://jservice.io/api/random?count=8'
    response = requests.get(req)
    trivia_set = response.json()
    content = []
    for trivia in trivia_set:
        dict = {'id': trivia['id'], 'question' : trivia['question'], 'answer' : trivia['answer'], 'category' : trivia['category']['title'], 'value' : trivia['value'], 'airdate' : trivia['airdate'][:10], 'category_id' : trivia['category_id']}
        content.append(dict)
    return render(request, 'trivia/home.html', {'trivia':content})

def categories(request):
    req = 'http://jservice.io/api/categories?count=99'
    response = requests.get(req)
    category_set = response.json()
    content = []
    for category in category_set:
        dict = {'id': category['id'], 'title': category['title'], 'clues_count': category['clues_count']}
        content.append(dict)
    return render(request, 'trivia/categories.html', {'categories':content})

def listcategory(request, id='11510'):
    req = 'http://jservice.io/api/category?id='+id
    response = requests.get(req)
    category_set = response.json()
    clues_set = category_set['clues']
    content = []
    for clues in clues_set:
        dict = {'answer':clues['answer'], 'question':clues['question']}
        content.append(dict)
    return render(request, 'trivia/listcategory.html', {'clues':content})

def results(request):
    # time to work on the search box
    if request.method == 'POST':
        form = searchform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # inputting values from the data
            category = data['category'] if data['category']!='' else None
            diff = data['difficulty'] if data['difficulty']!= "" else None

            return results_trivia(request, category, difficulty)

    form = searchform()
    content = []
    offset = random.randint(0, 2000)
    req = "http://jservice.io/api/categories?count=100" + "&offset=" + str(offset)
    response = requests.get(req)
    category_set = response.json()
    for category in category_set:
        dict = {'title':category['title'], 'id':category['id']}
        content.append(dict)
    return render(request, 'trivia/results.html', {'categories':content, 'form':form, 'title':"Search"})

def results_trivia(request, cat, diff):
    content_set = []
    clues_set = []
    success = False

    offset = 0
    categories = []
    while True:
        req = "http://jservice.io/api/categories?count=100&offset=" + str(offset)
        response = requests.get(req)
        category_set = response.json()
        # base: overflow
        if offset >= 10000:
            break
        # now find the correct set of Categories
        for category in category_set:
            categories.append(category['title'])
            # check if category exists
            if category['title'] == None:
                break

            elif (cat == None) or (cat != "" and cat in category['title']):
                clue_req = "http://jservice.io/api/clues?category=" + str(category['id'])
                clue_response = requests.get(clue_req)
                clue_question_set = clue_question.json()

                for clue in clue_question_set:
                    value = clue['value'] # this determines the difficulty of the question
                    airdate = datetime.date(int(clue['airdate'][:4]), int(clue['airdate'][5:7]), int(clue['airdate'][8:10]))

                    if value == None:
                        continue

                    # Max difficulty value == 1000
                    dict = {'easy': 0 < value <= 300, 'intermediate': 300 < value <= 700, 'difficult': 700 < value <= 1000}
                    difficulty = dict[diff]

                    # filter date here
                    timeframe = date[0] <= airdate <= date[1]

                    if difficulty and timeframe:
                        clues_set.append(clue)

        offset += 1000

    if len(clues_set) != 0:
        success = True

    f = open("all_categories.txt", "w")
    f.write(str(categories))

    for clue in clues_set:
        dict = {'id': clue['id'], 'question':clue['question'], 'answer':clue['answer'], 'category':clue['category']['title'], 'airdate':clue['airdate'][:10], 'value':clue['value'], 'category_id':clue['category_id']}
        content.append(dict)

    return render(request, {'trivia':content, 'title':cat, 'success':success, 'titleBar':cat})

def airdatetrivia(request):
    return render(request)

def difficultytrivia(request):
    return render(request)

def about(request):
    return render(request, 'trivia/about.html')
