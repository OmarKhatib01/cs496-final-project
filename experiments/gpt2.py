from transformers import pipeline
import json
import os 

# initialize the pipeline
text_generation = pipeline("text-generation", model="gpt2")


def generateAnswersJson():
    # loop data folder to load data from json, pass into the pipeline, and write answers to a new json
    for file in os.listdir('../data/'):
        with open('../data/' + file) as json_file:
            data = json.load(json_file)
            # pass data into pipeline
            data = generateAnswers(data, file)

            # write answers to json
            with open('../data/' + file.split('.')[0] + '-answers.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)



# function to psas in question and options to the pipeline depending on json_file
def generateAnswers(data, file):
    if file == 'lsat.json':
        # lsat categories
        categories = ['readingComprehension', 'analyticalReasoning', 'logicalReasoning']
        for category in categories:
            for j in range(len(data[category])):
                passage = data[category][j]['passage']
                for k in range(len(data[category][j]['questions'])):
                    print(data[category][j]['questions'][k]['question'])
                    question = data[category][j]['questions'][k]['question']
                    options = '\n'.join(str(opt) for opt in data[category][j]['questions'][k]['options'])
                    # pass question and options to pipeline
                    answer = text_generation(f'{passage} \n {question} \n {options} \n choose the best answer A, B, C, D, E:', max_length=1000, do_sample=True, top_p=0.95, top_k=60, num_return_sequences=1)
                    print(answer)
                    # write questions and answers to data
                    data[category][j]['questions'][k]['gpt2-answer'] = answer[0]['generated_text'].split('E:')[1]
                    print(data[category][j]['questions'][k]['gpt2-answer'])
    else:
        for j in range(len(data['questions'])): 
            question = data['questions'][j]['question']
            print(question)
            options = data['questions'][j]['options']
            print(options)
            # pass question and options to pipeline
            answer = text_generation(question + str(options) + ' answer:', max_length=100, do_sample=True, top_p=0.95, top_k=60, num_return_sequences=1)
            # write questions and answers to json
            data['questions'][j]['gpt2-answer'] = answer[0]['generated_text'].split('answer:')[1]
    return data

generateAnswersJson()