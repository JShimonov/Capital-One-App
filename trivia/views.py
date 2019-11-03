from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from trivia.searchtags import searchform
import datetime
import random
import requests

def home(request):
    if request.method == 'POST':
        category = request.POST["Category"]
        from_date = request.POST["airdate-start"]
        to_date = request.POST["airdate-end"]
        diff = request.POST["Difficulty"]
        return results_trivia(request, category, diff, from_date, to_date)

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
        category = request.POST["Category"]
        from_date = request.POST["airdate-start"]
        to_date = request.POST["airdate-end"]
        diff = request.POST["Difficulty"]
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

def results_trivia(request, cat, diff, from_date, to_date):
    content_set = []
    clues_set = []

    offset = 0

    while True:
        req = "http://jservice.io/api/categories?count=100&offset=" + str(offset)
        response = requests.get(req)
        category_set = response.json()

        if offset >= 10000: # prevent crashing with blank category
            break

        # Find right category
        for category in category_set:
            if category['title'] == None:
                break

            # Filter By Category
            # Add all the questions/clues from that category and append to larger list
            elif (cat == None) or (cat != "" and cat in category['title']):  # if there is no query or if there is a query
                clue_req = "http://jservice.io/api/clues?category=" + str(category['id'])
                clue_response = requests.get(clue_req)
                clue_question_set = clue_response.json()

                for clue in clue_question_set: # Loop through all the questions in one category
                    if clue['value'] == None:
                        continue
                    else:
                        value = int(clue['value'])
                    airdate = datetime.date(int(clue['airdate'][:4]), int(clue['airdate'][5:7]), int(clue['airdate'][8:10]))

                    # look thru the difficulty
                    dict = {'Easy': 0 < value <= 300, 'Intermediate': 300 < value <= 700, 'Difficult': 700 < value <= 1000}
                    difficulty = dict[diff]

                    # look thru the time airdate
                    time_airdate = datetime.date(int(from_date[:4]), int(from_date[5:7]), int(from_date[8:10])) <= airdate <= datetime.date(int(to_date[:4]), int(to_date[5:7]), int(to_date[8:10]))
                    if difficulty:
                        clues_set.append(clue)

        offset += 100

    for clue in clues_set:
        dict = {'id': clue['id'], 'question':clue['question'], 'answer':clue['answer'], 'category':clue['category']['title'], 'airdate':clue['airdate'][:10], 'value':clue['value'], 'category_id':clue['category_id']}
        content_set.append(dict)
    print(content_set)

    return render(request, 'trivia/results.html', {'trivia':content_set})

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
