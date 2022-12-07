import json
from pprint import pprint
from collections import defaultdict

import numpy as np
import pandas as pd


# get answers for each model from each dataset
def getAnswersJson():
    files=['myers-briggs.json','lsat.json','psychopath-screening.json', 'act.json']
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
        answers = pd.DataFrame(columns=['Test','Category', 'Answer'] + models)
        categories = ['readingComprehension', 'analyticalReasoning', 'logicalReasoning']
        for category in categories:
            for j in range(len(data[category])):
                for k in range(len(data[category][j]['questions'])):
                    row = [file[:-5],category, data[category][j]['questions'][k]['answer']]
                    for model in models:
                        # get answers from json
                        row.append(data[category][j]['questions'][k][f'{model} Answer'])
                        # turn dictionary into dataframe
                    answers.loc[len(answers.index)]=row
    elif file == 'act.json':
        answers = pd.DataFrame(columns=['Test','Category', 'Answer'] + models)
        categories = ['reading', 'english', 'math']
        for category in categories:
            if category == 'math':
                for k in range(len(data[category])):
                    row = [file[:-5], category, data[category][k]['answer']]
                    for model in models:
                        # get answers from json
                        row.append(data[category][k][f'{model} Answer'])
                        # turn dictionary into dataframe
                    answers.loc[len(answers.index)]=row
            else:
                for j in range(len(data[category])):
                    for k in range(len(data[category][j]['questions'])):
                        row = [file[:-5],category, data[category][j]['questions'][k]['answer']]
                        for model in models:
                            # get answers from json
                            row.append(data[category][j]['questions'][k][f'{model} Answer'])
                            # turn dictionary into dataframe
                        answers.loc[len(answers.index)]=row
    else:
        answers = pd.DataFrame(columns= ['Test']+models)
        for i in range(len(data['questions'])):
            row=[file[:-5]]
            for model in models:
                # get answers from json
                row.append(data['questions'][i][f'{model} Answer'])
            answers.loc[len(answers.index)] = row
    return answers

# get statistics for each model on each dataset
def getStatistics(files, models):
    infinite_defaultdict = lambda: defaultdict(infinite_defaultdict)
    stats = defaultdict(infinite_defaultdict)
    for file, categories in files.items():
        # get answers for each dataset
        with open('../data/' + file) as json_file:
            data = json.load(json_file)
            answers = getAnswers(file, data, models)

            num_total = len(answers)
            stats[file]['num_total'] = str(num_total)

            for model in models:
                if file in ['lsat.json', 'act.json']:
                    num_correct = np.sum(answers[model]==answers['Answer'])
                    stats[file][model]['num_correct'] = str(num_correct)

                    stats[file][model]['accuracy'] = str(num_correct / num_total)

                for letter in ['A','B','C','D', 'E']:
                    number_of_letter = np.sum(answers[model] == letter)
                    stats[file][model]['answer_distribution'][letter]['number_of_letter'] = str(number_of_letter)
                    stats[file][model]['answer_distribution'][letter]['percentage_of_letter'] = str(number_of_letter / num_total)

                for category in categories:
                    relevant_answers = answers[answers['Category'] == category]

                    num_total_category = len(relevant_answers)
                    stats[file][model]['categories'][category]['num_total'] = str(num_total_category)

                    num_correct_category = np.sum(relevant_answers[model] == relevant_answers['Answer'])
                    stats[file][model]['categories'][category]['num_correct'] = str(num_correct_category)

                    stats[file][model]['categories'][category]['accuracy'] = str(num_correct_category / num_total_category)

                    for letter in ['A','B','C','D', 'E']:
                        number_of_letter_category = np.sum(relevant_answers[model] == letter)
                        stats[file][model]['categories'][category]['answer_distribution'][letter]['number_of_letter'] = str(number_of_letter_category)
                        stats[file][model]['categories'][category]['answer_distribution'][letter]['percentage_of_letter'] = str(number_of_letter_category / num_total_category)
            
            if file in ['lsat.json', 'act.json']:
                average_accuracy = np.mean([float(stats[file][model]['accuracy']) for model in models])
                stats[file]['average_accuracy'] = str(average_accuracy)

                for letter in ['A','B','C','D', 'E']:
                    number_of_letter = np.sum(answers['Answer']==letter)
                    stats[file]['ground_truth_distribution'][letter]['number_of_letter'] = str(number_of_letter)
                    stats[file]['ground_truth_distribution'][letter]['percentage_of_letter'] = str(number_of_letter / num_total)
    return stats

if __name__ == '__main__':
    # uncomment to repopulate answer csv files
    # getAnswersJson()

    files = {
        'lsat.json': ['readingComprehension', 'analyticalReasoning', 'logicalReasoning'], 
        'act.json': ['reading', 'english', 'math'],
        'myers-briggs.json': [],
        'psychopath-screening.json': [],
    }
    models = ['text-davinci-003', 'text-curie-001', 'text-babbage-001']
    stats = getStatistics(files, models)
    with open('../data/stats.json', 'w') as json_file:
        json.dump(dict(stats), json_file, indent=4)