import os
import json
import scipy
import pandas as pd

# get answers for each model from each dataset
def getAnswersJson():
    datasets = ['lsat.json', 'myers-briggs.json', 'psychopath-screening.json']
    models = ['text-davinci-003', 'text-curie-001', 'text-babbage-001']
    # get data from data folder 
    for file in os.listdir('../data/'):
        with open('../data/' + file) as json_file:
            data = json.load(json_file)
    return

def getAnswers(file, data, model):
    answers = pd.DataFrame()
    if file == 'lsat.json':
        # lsat categories
        categories = ['readingComprehension', 'analyticalReasoning', 'logicalReasoning']
        for category in categories:
            answers[category] = []
            for j in range(len(data[category])):
                for k in range(len(data[category][j]['questions'])):
                    answers[category].append(data[category][j]['questions'][k][f'{model} Answer'])
    print(answers)

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
with open('../data/lsat.json') as json_file:
    data = json.load(json_file)
getAnswers('lsat.json', data, 'text-davinci-003')