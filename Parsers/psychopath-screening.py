from bs4 import BeautifulSoup as bs
import requests as req
import json

def getQuestions():
    url = "https://psychopathyis.org/screening/tripm/"
    r = req.get(url)
    soup = bs(r.text, "html.parser")

    # scrape questions from psychopathyis.org
    questions = []
    for paragraph in soup.find_all('legend', class_="gfield_label"):
        # replace "required" with empty string
        text = paragraph.text.replace("(Required)","").replace("\u2019", "'").split(".", 1)

        question = { 
            "id": text[0],
            "question": text[1],
            "options": {
                0: "true",
                1: "somewhat true",
                2: "somewhat false",
                3: "false"
            }
        }
        questions.append(question)
    return questions

# create json file with questions
def createJson():
    data = {
        'questions': getQuestions()[1:]
    }
    with open('../data/psychopath-screening.json', 'w') as file:
        json.dump(data, file, indent=4)

createJson()
