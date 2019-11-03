# Capital One Web App Challenge

To complete the challenge, build a web application that:
1. Has a search function that displays in an intuitive, responsive, mobile friendly, easy to navigate interface
2. Gives users the ability to refine search results by:
   - Date or timeframe aired (you can search by a day, a week, a month)
   - Trivia category
   - Level of difficulty of the question
   - Any other smart searching criteria you see fit

Optional: You may want to include these bonus features:
  - Game board simulation with the categories and questions in the proper place (as it would be organized in the game with easier questions on top
  - Marking or saving questions into a "favorites" collection

# Website URL
https://jshimonovcapapp.herokuapp.com

# Tech Stack

## Front-End
- HTML/CSS
- Bootstrap
- Javascript (implemented within the HTML code)
## Back-End
- Django
## APIs Used
- JService

# Features Included

The required criteria for the website have been completed:
- [x] Search function that displays in an intuitive, responsive, mobile friendly, easy to navigate interface
- [x] Ability to refine search results (Date, Category, Difficulty)

Optional features that have been implemented:
- [x] The home page features the search for categories, difficulty, and airdate forms, as well as 15 random questions from 'api/random'
- [x] The categories page lists the first 99 categories from '/api/categories'
- [x] When the user views the questions they are also able to press on the Category, Airdate, and also the Difficulty to find other questions that match that description
- [x] Added gradient background in the wherever there is a form for the user to input their categories
- [x] Added feature where the user has to press a button to show the answer to the question that they are viewing

Future features to be implemented:
- [ ] Create an auto-complete for the search bar so that when the user types, they can see all the possible choices based on what they are typing.
- [ ] Create a game that functions like a speed round, where you test the user's knowledge of trivia in a timed setting
- [ ] Make the search algorithm faster
- [ ] Add more CSS and designs to the website

# How the Search Algorithm Works
1. Posts all the information that the user inputs to search fields (search bar,  start date, end date, and difficulty)
2. If Post is true, then input all the values given to results_trivia(params)
3. For the search algorithm to work as efficiently as possible, once in results_trivia, we have to traverse through all of the categories.
4. Because there is a limit to the amount that we can see from the API, there is an offset for every 100 categories. This utilizes the first outer for-loop in the results_trivia() method. In order to prevent overflow, I set the max offset to 10000
5. To ensure that there is a category that should be checked, we check if there is a title for that category; if there isn't then we break.
6. Otherwise, we now have access to the Category_Id, which also allows us to find questions related to the category that the user entered in the search field. We are able to do this by using 'api/clues'.
7. To optimize the search, we now have to check if those questions found in the clues API are within the date/time range that the user specified in the forms.
8. Additionally, we have to check if the value of the question fits the difficulty that the user specified
9. Based off of the responses from numbers 7 and 8 (re: above), '/results' will render the content based on those responses.

# Challenges
- At first, the challenge seemed to be intimidating because I haven't done HTML/CSS in a long time. However, after reviewing some videos on how to get started, I was able to start making the website. The real challenges started then.
1. Parsing values from API in an efficient way
2. Adding JS to show answers to each question
3. Making the Search features function properly to output values onto the results page

# Walkthroughs

## Home Page
<img src = 'https://github.com/JShimonov/Capital-One-App/blob/master/CapitalOneAppWalkThru1.gif' />

## Categories Page
<img src = 'https://github.com/JShimonov/Capital-One-App/blob/master/CapitalOneAppWalkThru2.gif' />

## Results Page
<image src = 'https://github.com/JShimonov/Capital-One-App/blob/master/CapitalOneAppWalkThru3.gif' />
