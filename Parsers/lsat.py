import json
import requests
from bs4 import BeautifulSoup as bs

# Analytical Reasoning Questions Data
# path = '../data/lsat_TrainingData.json'
# def ardata(path):
#     with open(path) as f:
#         parsed = json.load(f)

#     questions = []

#     for i in range(50): # 25 questions in each section
#         for j in range(len(parsed[i]['questions'])):
#             question = {
#                 'id': parsed[i]['questions'][j]['id'],
#                 'question': parsed[i]['questions'][j]['question'],
#                 'options': parsed[i]['questions'][j]['options'],
#                 'answer': parsed[i]['questions'][j]['answer'],
#             }
#             questions.append(question)

#     print(json.dumps(questions, indent=4))
#     return questions


# Reading Comp Questions Data
def rcData():
    url = 'https://www.cracklsat.net/lsat/reading-comprehension/'
    questions = []
    passage = "init passage"
    passageCnt = 0

    urls = [url+f'question-{i}.html' for i in range(1,31)] # 27 questions in reading comprehension section
    for url in urls:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        if passage != soup.find('pre', class_='pre-scrollable').text:
            passage = soup.find('pre', class_='pre-scrollable').text
            questions.append({
                'passage': passage.encode('latin1').decode('utf8'),
                'questions': [
                    {
                        'id': soup.find('p').text.split(': ', 1)[1],
                        'question': soup.find('pre', class_='pre-scrollable').next_sibling.next_sibling.text,
                        'options': [option.text for option in soup.find_all('div', class_='radio')],
                        'answer' : soup.find('span', id='key').text
                    }
                ],
            })
            passageCnt += 1
        else:
            questions[passageCnt-1]['questions'].append(
                {
                    'id': soup.find('p').text.split(': ', 1)[1],
                    'question': soup.find('pre', class_='pre-scrollable').next_sibling.next_sibling.text,
                    'options': [option.text for option in soup.find_all('div', class_='radio')],
                    'answer' : soup.find('span', id='key').text
                }
            )
    return questions


# Logic Games / Analytical Reasoning Questions Data
def arData():
    url = 'https://www.cracklsat.net/lsat/logic-games/'
    questions = []
    passage = "init passage"
    passageCnt = 0

    urls = [url+f'question-{i}.html' for i in range(1,31)] # 30 questions in logic games section
    for url in urls:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        if passage != soup.find('pre', class_='pre-scrollable').text:
            passage = soup.find('pre', class_='pre-scrollable').text
            questions.append({
                'passage': passage.encode('latin1').decode('utf8'),
                'questions': [
                    {
                        'id': soup.find('p').text.split(': ', 1)[1],
                        'question': soup.find('pre', class_='pre-scrollable').next_sibling.next_sibling.text,
                        'options': [option.text for option in soup.find_all('div', class_='radio')],
                        'answer' : soup.find('span', id='key').text
                    }
                ],
            })
            passageCnt += 1
        else:
            questions[passageCnt-1]['questions'].append(
                {
                    'id': soup.find('p').text.split(': ', 1)[1],
                    'question': soup.find('pre', class_='pre-scrollable').next_sibling.next_sibling.text,
                    'options': [option.text for option in soup.find_all('div', class_='radio')],
                    'answer' : soup.find('span', id='key').text
                }
            )
    return questions



# Logical Reasoning Questions Data
def lrData():
    url = 'https://www.cracklsat.net/lsat/logical-reasoning/'
    questions = []
    passage = "init passage"
    passageCnt = 0

    urls = [url+f'question-{i}.html' for i in range(1,61)] # 30 questions in each logical reasoning section
    for url in urls:
        
        r = requests.get(url)

        # check if r is a valid url
        if r.status_code != 200:
            continue

        soup = bs(r.text, 'html.parser')
        if passage != soup.find('p').next_sibling.next_sibling.text:
            passage = soup.find('p').next_sibling.next_sibling.text
            questions.append({
                'passage': passage.encode('latin1').decode('utf8'),
                'questions': [
                    {
                        'id': soup.find('p').text.split(': ', 1)[1],
                        'question': soup.find('div', class_='radio').previous_sibling.previous_sibling.text,
                        'options': [option.text for option in soup.find_all('div', class_='radio')],
                        'answer' : soup.find('span', id='key').text
                    }
                ],
            })
            passageCnt += 1
        else:
            questions[passageCnt-1]['questions'].append(
                {
                    'id': soup.find('p').text.split(': ', 1)[1],
                    'question': soup.find('div', class_='radio').previous_sibling.previous_sibling.text,
                    'options': [option.text for option in soup.find_all('div', class_='radio')],
                    'answer' : soup.find('span', id='key').text
                }
            )
    return questions

# print(json.dumps(rcData(), indent=2))
# print(json.dumps(arData(), indent=2))
# print(json.dumps(lrData(), indent=2))


# create json that saves all the data
def createJson():
    data = {
        'readingComp': rcData(),
        'analyticalReasoning': arData(),
        'logicalReasoning': lrData()
    }
    with open('../data/lsat_data.json', 'w') as file:
        json.dump(data, file, indent=4)

createJson()