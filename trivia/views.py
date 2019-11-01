from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from trivia.searchtags import searchform
import datetime
import random
import requests

print("hi")

# this method is what
def home(request):
    print("hey")
    if request.method == 'POST':
        print("hello")
        form = searchform(request.POST)
        print("hi")
        if form.is_valid():
            data = form.cleaned_data
            # inputting values from the data
            category = data['category'] if data['category']!='' else None
            diff = data['difficulty'] if data['difficulty']!= "" else None
            from_date = data['from_date'] if data['from_date'] != None else datetime.date(1966, 1, 1)
            to_date = data['to_date'] if data['to_date'] != None else datetime.date(2011, 12, 12)
            print(category)
            print("hello 1")
            
            return results_trivia(request, category, diff, (from_date, to_date))

    req = 'http://jservice.io/api/random?count=15'
    response = requests.get(req)
    trivia_set = response.json()
    content = []
    for trivia in trivia_set:
        dict = {'id': trivia['id'], 'question' : trivia['question'], 'answer' : trivia['answer'], 'category' : trivia['category']['title'], 'value' : trivia['value'], 'airdate' : trivia['airdate'][:10], 'category_id' : trivia['category_id']}
        content.append(dict)

    return render(request, 'trivia/home.html', {'trivia':content})

def categories(request):
    if request.method == 'POST':
        form = searchform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # inputting values from the data
            category = data['category'] if data['category']!='' else None
            diff = data['difficulty'] if data['difficulty']!= "" else None
            from_date = data['from_date'] if data['from_date'] != None else datetime.date(1966, 1, 1)
            to_date = data['to_date'] if data['to_date'] != None else datetime.date(2011, 12, 12)

            return results_trivia(request, category, diff, (from_date, to_date))

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
        dict = {'id':clues['id'], 'category':category_set['title'], 'value':clues['value'], 'airdate':clues['airdate'][:10],'answer':clues['answer'], 'question':clues['question']}
        content.append(dict)
    return render(request, 'trivia/listcategory.html', {'clues':content})

def results_trivia(request, cat, diff, date):
    content_set = []
    clues_set = []

    offset = 0
    categories = []
    while True:
        req = "http://jservice.io/api/categories?count=100&offset=" + str(offset)
        response = requests.get(req)
        category_set = response.json()
        # base: overflow
        if offset >= 1000:
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
                clue_question_set = clue_response.json()

                for clue in clue_question_set:
                    value = clue['value'] # this determines the difficulty of the question
                    airdate = datetime.date(int(clue['airdate'][:4]), int(clue['airdate'][5:7]), int(clue['airdate'][8:10]))

                    if value == None:
                        continue

                    # Max difficulty value == 1000
                    dict = {'easy': 0 < value <= 300, 'intermediate': 300 < value <= 700, 'difficult': 700 < value <= 1000, None:True}
                    difficulty = dict[diff]

                    # filter date here
                    timeframe = date[0] <= airdate <= date[1]

                    if difficulty and timeframe:
                        clues_set.append(clue)

        offset += 1000

    f = open("all_categories.txt", "w")
    f.write(str(categories))

    for clue in clues_set:
        dict = {'id': clue['id'], 'question':clue['question'], 'answer':clue['answer'], 'category':clue['category']['title'], 'airdate':clue['airdate'][:10], 'value':clue['value'], 'category_id':clue['category_id']}
        content_set.append(dict)

    return render(request, 'trivia/results.html', {'trivia':content_set, 'category':cat, 'difficulty':diff, 'date':date})

def difficultytrivia(request, id='100'):
    req = "http://jservice.io/api/clues?value="+id
    response = requests.get(req)
    trivia_set = response.json()
    content = []
    for trivia in trivia_set:
        dict = {'id': trivia['id'], 'question': trivia['question'], 'answer': trivia['answer'], 'airdate': trivia['airdate'][:10], 'value': trivia['value'],
                'category_id' : trivia['category']['id'], 'category': trivia['category']['title']}
        content.append(dict)
    return render(request, 'trivia/results.html', {'trivia':content, 'title':id})

def airdatetrivia(request, id='2012-01-01'):
    req = "http://jservice.io/api/clues?min_date="+id+"T12:00:00.000Z&max_date="+id+"T12:00:00.000Z"
    response = requests.get(req)
    trivia_set = response.json()
    content = []
    for trivia in trivia_set:
        dict = {'id': trivia['id'], 'question': trivia['question'], 'answer': trivia['answer'], 'airdate': trivia['airdate'][:10], 'value': trivia['value'],
                'category_id' : trivia['category']['id'], 'category': trivia['category']['title']}
        content.append(dict)
    return render(request, 'trivia/results.html', {'trivia':content, 'title':id})

def test(request):
    if request.method == 'POST':
        form = searchform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # inputting values from the data
            category = data['category'] if data['category']!='' else None
            diff = data['difficulty'] if data['difficulty']!= "" else None
            from_date = data['from_date'] if data['from_date'] != None else datetime.date(1966, 1, 1)
            to_date = data['to_date'] if data['to_date'] != None else datetime.date(2011, 12, 12)

            return results_trivia(request, category, diff, (from_date, to_date))
    return render(request)
