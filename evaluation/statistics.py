import os
import json
import scipy
import pandas as pd

# get answers for each model from each dataset
def getAnswersJson():
    files=['myers-briggs.json','lsat.json','psychopath-screening.json']
    models = ['text-davinci-003', 'text-curie-001', 'text-babbage-001']
    # get data from data folder 
    for file in files:
        with open('../data/' + file) as json_file:
            data = json.load(json_file)
            # get answers for each file
            answers = getAnswers(file, data, models)
            # write answers to csv
            filename = file.split('.')[0] + '-answers.csv'
            answers.to_csv(f'../data/{filename}')
    return

def getAnswers(file, data, models):
    if file == 'lsat.json':
        categories = ['readingComprehension', 'analyticalReasoning', 'logicalReasoning']
        answers = {model: {category: [] for category in categories} for model in models}
        for category in categories:
            answerList = []
            for j in range(len(data[category])):
                for k in range(len(data[category][j]['questions'])):
                    for model in models:
                        # get answers from json
                        answer = data[category][j]['questions'][k][f'{model} Answer']
                        answerList.append(answer)
                        # append answers to dataframe
                        answers[model][category] = pd.Series(answerList)
                        # turn dictionary into dataframe
                        answers = pd.DataFrame(answers)

    else:
        answers = pd.DataFrame({model: [] for model in models})
        for model in models:
            answerList = []
            for i in range(len(data['questions'])):
                # get answers from json
                answer = data['questions'][i][f'{model} Answer']
                answerList.append(answer)

                # append answers to dataframe
                answers[model] = pd.Series(answerList)
    # print(answers)
    return answers

# get statistics for each model on each dataset
def getStatistics(model, dataset):
    # get answers for each dataset
    answers = getAnswers(model, dataset)
    # get statistics for each dataset
    statistics = []
    for i in range(len(answers)):
        statistics.append(scipy.stats.describe(answers[i]))
    return statistics
# get accuracy for each model from each dataset
# get average accuracy for each model
# get average accuracy for each dataset
# get average accuracy for each model for each dataset


# with open('../data/lsat.json') as json_file:
#     data = json.load(json_file)
# getAnswers('lsat.json', data, ['text-davinci-003', 'text-curie-001', 'text-babbage-001'])

getAnswersJson()