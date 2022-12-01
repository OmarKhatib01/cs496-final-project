from bs4 import BeautifulSoup as bs
import requests
import json

def getQuestions():
    url = "http://keys2cognition.com/explore.htm"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")

    questions = []

    options = {
        'A': "not like me",
        'B': "a little like me",
        'C': "somewhat like me",
        'D': "mostly like me",
        'E': "exactly like me"
    }

    for paragraph in soup.find_all('p', align="top"):
        # replace italics of text with empty string
        text = paragraph.text.split(". ", 1)[1].replace("\xa0","")
        question = { 
            "id": paragraph.text.split(". ", 1)[0],
            "question": text,
            "options": options
        }
        questions.append(question)

    return questions

# create json file with questions
def createJson():
    data = {
        'questions': getQuestions()
    }
    with open('../data/myers-briggs.json', 'w') as file:
        json.dump(data, file, indent=4)

createJson()
