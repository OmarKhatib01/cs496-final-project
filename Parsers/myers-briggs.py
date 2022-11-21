from bs4 import BeautifulSoup as bs
import requests as req
import html5lib


url = "http://keys2cognition.com/explore.htm"
r = req.get(url)
soup = bs(r.text, "html5lib")

questions = []

options = {
    0: "not like me",
    1: "a little like me",
    2: "somewhat like me",
    3: "mostly like me",
    4: "exactly like me"
}

for paragraph in soup.find_all('p', align="top"):
    # replace italics of text with empty string
    text = paragraph.text.replace("\xa0","")
    question = { 
        "Question": text,
        "choose one": options
     }
    questions.append(question)

print(questions)
