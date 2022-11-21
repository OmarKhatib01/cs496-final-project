from bs4 import BeautifulSoup as bs
import requests as req
import html5lib


url = "https://psychopathyis.org/screening/tripm/"
r = req.get(url)
soup = bs(r.text, "html5lib")

# scrape questions from psychopathyis.org
questions = []
for paragraph in soup.find_all('legend', class_="gfield_label"):
    # replace "required" with empty string
    text = paragraph.text.replace("(Required)","")

    question = { 
        "Question": text,
        "choose one": {
            0: "true",
            1: "somewhat true",
            2: "somewhat false",
            3: "false"
        }
     }
    questions.append(question)

print(questions)