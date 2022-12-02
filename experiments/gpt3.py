import os
import json
import openai
import time
import numpy as np
import re

openai.api_key = "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"
global model
# model="text-davinci-003"
# model='text-curie-001'
model='text-babbage-001'

global temp
temp=1



def generateAnswersJson():
    # loop data folder to load data from json, pass into the pipeline, and write answers to a new json
    files=['myers-briggs.json','lsat.json','psychopath-screening.json']
    files = ['act.json']
    #files = ['lsat.json', 'psychopath-screening.json']
    #files=os.listdir('../data/')
    for file in files:
        with open('../data/' + file) as json_file:
            data = json.load(json_file)
            # pass data into pipeline
            data = generateAnswers(data, file)

            # write answers to json
            #with open('../data/' + file.split('.')[0] + '-answers.json', 'w') as outfile:
                #json.dump(data, outfile, indent=4)
            with open('../data/' + file, 'w') as outfile:
                json.dump(data, outfile, indent=4)



# function to psas in question and options to the pipeline depending on json_file
def generateAnswers(data, file):
    ops=['A','B','C','D','E']
    answers=[]
    right = 0
    count = 0
    if file == 'lsat.json':
        # lsat categories
        categories = ['readingComprehension', 'analyticalReasoning', 'logicalReasoning']
        for category in categories:
            print(category)
            for j in range(len(data[category])):
                passage = data[category][j]['passage']
                for k in range(len(data[category][j]['questions'])):
                    time.sleep(3)
                    #print(data[category][j]['questions'][k]['question'])
                    question = data[category][j]['questions'][k]['question']
                    options = '\n'.join(str(opt) for opt in data[category][j]['questions'][k]['options'])
                    # pass question and options to pipeline
                    answer = openai.Completion.create(
                                        model=model,
                                        prompt=f'{passage} \n {question} \n {options} \n Choose One. Answer: ',
                                        temperature=temp,
                                        max_tokens=1000,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0
                                      )['choices'][0]['text']
                    for char in answer:
                        if char in ops:
                            ans = char
                            break
                    answers.append(ans)
                    # write questions and answers to data
                    data[category][j]['questions'][k][model+' Answer'] = ans
                    print('GPT:' +data[category][j]['questions'][k][model+' Answer'])
                    print('Ans:' +data[category][j]['questions'][k]['answer'])
                    print(' ')
                    count+=1
                    if data[category][j]['questions'][k][model+' Answer'] == data[category][j]['questions'][k]['answer']: right+=1

                print(round(right/count,3))
    elif file == 'act.json':
        # act categories
        categories = ['math', 'reading', 'english']
        for category in categories:
            print(category)
            for j in range(len(data[category])):
                if category == 'reading':
                    passage = data[category][j]['passage']
                
                if category == 'math':
                    time.sleep(3)
                    #print(data[category][j]['question'])
                    question = data[category][j]['question']
                    options = '\n'.join(str(opt) for opt in data[category][j]['options'])
                    prompt = ''
                    if category == 'reading':
                        prompt = f'{passage} \n {question} \n {options} \n Choose One. Answer: '
                    else:
                        prompt = f'{question} \n {options} \n Choose One. Answer: '
                    # pass question and options to pipeline
                    answer = openai.Completion.create(
                                        model=model,
                                        prompt=prompt,
                                        temperature=temp,
                                        max_tokens=1000,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0
                                    )['choices'][0]['text']
                    for char in answer:
                        if char in ops:
                            ans = char
                            break
                    answers.append(ans)
                    # write questions and answers to data
                    data[category][j][model+' Answer'] = ans
                    print('GPT:' +data[category][j][model+' Answer'])
                    print('Ans:' +data[category][j]['answer'])
                    print(' ')
                    count+=1
                    if data[category][j][model+' Answer'] == data[category][j]['answer']: right+=1
                else:
                     for k in range(len(data[category][j]['questions'])):
                        time.sleep(3)
                        #print(data[category][j]['questions'][k]['question'])
                        question = data[category][j]['questions'][k]['question']
                        options = '\n'.join(str(opt) for opt in data[category][j]['questions'][k]['options'])
                        prompt = ''
                        if category == 'reading':
                            prompt = f'{passage} \n {question} \n {options} \n Choose One. Answer: '
                        else:
                            prompt = f'{question} \n {options} \n Choose One. Answer: '
                        # pass question and options to pipeline
                        answer = openai.Completion.create(
                                            model=model,
                                            prompt=prompt,
                                            temperature=temp,
                                            max_tokens=960,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0
                                        )['choices'][0]['text']
                        for char in answer:
                            if char in ops:
                                ans = char
                                break
                        answers.append(ans)
                        # write questions and answers to data
                        data[category][j]['questions'][k][model+' Answer'] = ans
                        print('GPT:' +data[category][j]['questions'][k][model+' Answer'])
                        print('Ans:' +data[category][j]['questions'][k]['answer'])
                        print(' ')
                        count+=1
                        if data[category][j]['questions'][k][model+' Answer'] == data[category][j]['questions'][k]['answer']: right+=1

            print(round(right/count,3))
    else:
        for j in range(len(data['questions'])):
            time.sleep(3)
            question = data['questions'][j]['question']
            print(question)
            options = data['questions'][j]['options']
            print(options)
            # pass question and options to pipeline
            answer = openai.Completion.create(
              model=model,
              prompt=question + str(options) + 'Choose One of A, B, C, or D. Answer: ',
              temperature=temp,
              max_tokens=1000,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )['choices'][0]['text']
            print(answer)
            for char in answer:
                if char in ops:
                    ans=char
                    break
                if ('false' in answer) or ('False' in answer):
                    ans='D'
                elif ('true' in answer) or ('True' in answer):
                    ans='A'
                else:
                    ans='C'
            answers.append(ans)
            # write questions and answers to data
            data['questions'][j][model+' Answer'] = ans
            print('GPT:' +data['questions'][j][model+' Answer'])
            print(' ')
    for ans in np.unique(answers):
        print(ans+': '+str(answers.count(ans)))
    return data

if __name__ == '__main__':
    generateAnswersJson()