import json

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter


def graph_distributions(stats, models, dataset_to_title):
    fig = plt.figure(figsize=(11, 11))
    letters = ['A', 'B', 'C', 'D', 'E']
    x = np.arange(len(letters)) * 2
    width = 0.35
    
    for i, (dataset, dataset_stats) in enumerate(stats.items()):
        axs = plt.subplot(2, 2, i + 1)
        axs.set_title(dataset_to_title[dataset])
        axs.set_xlabel('Answer')
        axs.set_xticks(x, letters)
        axs.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
        axs.axhline(0, color='black')
        axs.set_axisbelow(True)

        if dataset in ['lsat.json', 'act.json']:
            ground_truth = np.asarray([float(dataset_stats['ground_truth_distribution'][letter]['number_of_letter']) for letter in letters])

        for j, model in enumerate(models):

            answer_distribution = np.asarray([float(dataset_stats[model]['answer_distribution'][letter]['number_of_letter']) for letter in letters])
            
            if dataset in ['lsat.json', 'act.json']:
                axs.set_ylabel('% Error from Ground Truth')
                axs.yaxis.set_major_formatter(PercentFormatter())
                axs.bar(x - (1.5 - j) * width, 100 * (answer_distribution - ground_truth) / ground_truth, width, label=model)
                axs.set_ylim(-100, 250)
            else:
                axs.set_ylabel('Number of Answers')
                axs.bar(x - (1 - j) * width, answer_distribution, width, label=model)
                axs.set_ylim(0, 60)

        handles, labels = axs.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')
    
    fig.tight_layout()
    plt.savefig(f'../results/distribution.png')
            

def graph_accuracies(stats, models, dataset_to_title):    
    for dataset_name in ['act.json', 'lsat.json']:
        fig = plt.figure(figsize=(20, 10))
        dataset = stats[dataset_name]
        accuracies = [float(dataset[model]['accuracy']) for model in models]
        axs = plt.subplot(232)
        graph_format(axs, accuracies, models, 'Overall', dataset_to_title[dataset_name])
        
        sections = ['reading', 'english', 'math'] if dataset_name == 'act.json' else ['readingComprehension', 'analyticalReasoning', 'logicalReasoning']
        section_to_title = {
            'reading': 'Reading',
            'english': 'English',
            'math': 'Math',
            'readingComprehension': 'Reading Comprehension',
            'analyticalReasoning': 'Analytical Reasoning',
            'logicalReasoning': 'Logical Reasoning'
        }
        for i, section in enumerate(sections):
            accuracies = [float(dataset[model]['categories'][section]['accuracy']) for model in models]
            axs = plt.subplot(2, 3, i + 4)
            graph_format(axs, accuracies, models, section_to_title[section], dataset_to_title[dataset_name])

        fig.tight_layout()
        plt.savefig(f'../results/accuracies/{dataset_name[:-5]}.png')

def graph_format(axs, accuracies, models, section_name, test_name):
    x = np.arange(len(models))
    axs.set_xticks(x, models)
    axs.set_ylim(0, 1)
    axs.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
    axs.set_axisbelow(True)
    axs.set_title(f"{section_name} {test_name} Accuracy")
    axs.bar(x, accuracies, color=['tab:blue', 'tab:orange', 'tab:green'])
    

if __name__ == '__main__':
    models = ["text-davinci-003", "text-curie-001", "text-babbage-001"]
    dataset_to_title = {
        "myers-briggs.json": "Myers-Briggs",
        "lsat.json": "LSAT",
        "psychopath-screening.json": "Psychopath Screening",
        "act.json": "ACT"
    }
    with open('/Users/caden/College/CS496-GDM/Final Project/cs496-final-project/data/stats.json') as json_file:
        stats = json.load(json_file)
        graph_distributions(stats, models, dataset_to_title)
        graph_accuracies(stats, models, dataset_to_title)
    exit()