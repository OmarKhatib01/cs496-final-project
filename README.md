<h3 style="text-align:left;">
    Northwestern University
    <span style="float:right;">
        CS496 Deep Generative Models
    </span>
    <br>
    <span style="float:right;">
        Bryan Pardo (<a href="pardo@northwestern.edu">pardo@northwestern.edu</a>)
    </span>
</h3>
<br/>
<br/>
<h1 align=center> A Quantitative and Behavioral Profile of GPT-3 </h1>

# Authors
### Caden Howell - cadenhowell2023@u.northwestern.edu
### Connor McIntee - connormcintee2023@u.northwestern.edu
### Omar Khatib - omarkhatib2023@u.northwestern.edu

#  Overview
Testing Davinci-003, Curie-001, and Babbage-001 (OpenAI GPT-3 models) on Quantitative and Qualitative tests
* Qualitative
    * Myers-Briggs [Link to Site](keystocognition.com)
    * Psychopath Screening [Link to Site](psychopathyis.org)
* Quantitative
    * ACT [Link to Site](https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/english-practice-test-questions.html?page=0&chapter=0)
    * LSAT [Link to Site](https://www.cracklsat.net/lsat/logical-reasoning/)

# Table of contents
- [Abstract](#abstract)
- [Dataset](#datasets-structures)
- [Results](#results)
    - [ACT](#act-results)
    - [LSAT](#lsat-results)
    - [Myers-Briggs](#myers-briggs-results)
    - [Psychopath Screening](#psychopath-screening-results)
    - [Distribution of Answers](#distribution-of-answers)
- [Future Works](#possible-avenues-of-future-work)
- [References](#references)

# Abstract
There have been countless tests on the GPT models testing their accuracy and ability to produce text output that is comparable to humans. However, most, if not all, of these tests simply provide us with an score that we can use to compare the model to the previous SOTA. There has been a lack of research on the model's ability to complete more human tests. We aim to fill this gap in current research by passing 3 different models through 4 tests that will allow us to compare the models to the human population instead of other language models.   
   
Our project involves 3 current GPT-3 based models from OpenAI: Davinci-003, Curie-001, and Babbage-001. Davinci is the largest and most prolific GPT-3 model that OpenAI provides, while Curie and Babbage are relativley smaller models that are optimized for simpler tasks. In our project, we take these models and test them on the ACT, LSAT, Myers-Briggs Personality Test, and a Psychopath Screening Test.    
   
For the Quantitative tests, the ACT and LSAT, we scrapped practice test questions from https://www.act.org and https://www.cracklsat.net/lsat respectively. Our dataset for these questions included a passage (if applicable), the actual question, multiple choice options in ABC format, and the correct answer. All elements (except the answer) were passed to the models along with a prompt of "Choose One of \<Options>. Answer:". The models output was then compared to the correct answer. For the Qualitative tests, the Myers-Briggs and Psychopath tests, we scraped questions from http://keys2cognition.com and https://psychopathyis.org/screening respectively. Our dataset for these questions included the question and possible answers. The possible answers were reformatted into the ABC format of the Quantitative tests, and the same method of passing the questions was used as before. Model answers were then manually input into the given websites to obtain results.   
   
On the Quantitative tests, Davinci performed the best, scoring the 95th percentile (of humans) on the ACT reading. However, on most of the other sections Davinci's performance was around the 50th percentile. Curie and Babbage performed much worse, slightly above random choice. On the Qualitative tests, patterns emerged in the model's answers that suggested the models were not responding well to the question/answer format. The model's consistently never choose one of the options for each test, bringing the validity of these test results into question. This model inconsistency showed up in the Myers-Briggs results where each model received a different (seemingly random) personality. However in the psychopath test, the results show that all models have a low psychopath score (low chance of being a psychopath), a relatively low meanness and boldness score, and a relatively high disinhibition score.

# Datasets Structures
We created the datasets by parsing the websites for each of the ACT, LSAT, Myers-Briggs, Psychopath Screening tests in the [Overview](#overview) section above. The JSON format for each one is shown below:
<br>
## [ACT](https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/english-practice-test-questions.html?page=0&chapter=0) and [LSAT](https://www.cracklsat.net/lsat/logical-reasoning/) 
    {test section": [
        {
            "passage": ...(if in section),
            "questions": [
                {
                    "question": ...,
                    "options": [
                        "A. option A,
                        "B. option B,
                        "C. option C,
                        "D. option D
                    ],
                    "answer": Answer letter (e.g. "C"),
                },
                ...
        },

#### * Note: ACT math section does not have passages so it is structured similarly to Myers-Briggs & Psychopath Screening shown below

## [Myers-Briggs](keystocognition.com)
    "questions": [
        {
            "id": question number,
            "question": ...
            {
                "A": "not like me",
                "B": "a little like me",
                "C": "somewhat like me",
                "D": "mostly like me",
                "E": "exactly like me"
            },
            ...
        }

## [Psychopath Screening](https://psychopathyis.org/screening)
    "questions": [
        {
            "id": question number,
            "question": ,
            "options": {
                "A": "true",
                "B": "somewhat true",
                "C": "somewhat false",
                "D": "false"
            },
            ...
        },

## Recording Answers
The answers for each model for each test are recorded and added to the dataset JSONs as in the [data](/data/) folder. The answers are added at the same indentation level as the question in the following manner:

                "text-davinci-003 Answer": Answer letter,
                "text-curie-001 Answer": Answer letter,
                "text-babbage-001 Answer": Answer letter,

The answers are then recorded in a csv file for each test to run statistical analysis on them in the [data](/data/) folder


# Results
## ACT Results
[See act.json for questions and answers](/data/act.json)
### Best Model Scores (out of 36)
* Reading: 33 (95th percentile) - text-davinci-003
* English: 16 (36th percentile) - text-davinci-003
* Math: 18 (47th percentile) - text-davinci-003
* Science: N/A

![image](/results/accuracies/act.png)
<p align=center><b>Figure 1:</b>
Above is the accuracy on the ACT for the three different models (text-davinci-003, text-curie-001, text-babbage-001) across all ACT sections (Reading, Math, and English) except Science, where there were too many figures and tables to get well formed inputs to the model. For the math section, questions which had figures, tables, exponentiation, or subscripts were removed from the dataset for the same reason.
</p>

## LSAT Results
[See lsat.json for questions and answers](/data/lsat.json)
### Best Model Score (out of 180) *
* Scaled Composite: 147 (33.1 percentile) - text-davinci-003
#### * Note the LSAT scores are not reported section by section (as far as we could find), so we are only reporting the scaled composite score. This score is the raw result, but scaled and normalized.

![image](/results/accuracies/lsat.png)
<p align=center><b>Figure 2:</b>
This figure shows the accuracy on the LSAT for the three different models (text-davinci-003, text-curie-001, text-babbage-001) across all LSAT sections (Reading Comprehension, Analytical Reasoning, and Logical Reasoning. These questions are well formed so nothing was removed from the dataset.
</p>

## Psychopath Screening Results
[See psychopath-screening.json for questions and answers](/data/psychopath-screening.json)
### Highest Model Score
* Composite: 84/174 (73 percentile) - text-davinci-003
* Boldness: 32 - text-curie-001
* Meanness: 24 - text-davinci-003 and text-babbage-001
* Disinhibition: 31 - text-davinci-003

The models seem to score higher on disinhibiition than Connor, suggesting that they are more impulsive and less likely to think before acting. That said, all models were given a low likelihood of classifying as psychopaths.
![image](/results/psycopath-screening-results/table.png)
<p align=center><b>Figure 3:</b>
This figure shows the score for each of the models (text-davinci-003, text-curie-001, text-babbage-001) on the psychopath screening test. It is scored out of 174 where a higher number indicates more psychopathic tendencies. The percentile indicates the number of people who scored lower than the model on the test. The word in parenthesis--"low" in all cases--indicates the likelihood of the model classifying as a psychopath. The scores are broken down into subscores: boldness, meanness, and disinhibition which sum to form the overall score. Connor's score is given as a baseline.
</p>

## Myers-Briggs Results
[See myers-briggs.json for questions and answers](/data/myers-briggs.json)
#### There was no distinct pattern between all models here. Specifically, there was no one trait that was present in all three models. The largest model, text-davinci-003, was ESFP (see link in table below for breakdown and definitions).
|Model|Profile|
|--|--|
|text-davinci-003|[ESFP](/results/myers-briggs-results/myers-briggs-text-davinci-003.html)|
|text-curie-001|[ISTJ](/results/myers-briggs-results/myers-briggs-text-curie-001.html)|
|text-babbage-001|[ENTP](/results/myers-briggs-results/myers-briggs-text-babbage-001.html)|
|Connor|ENTP|
<p align=center><b>Figure 4:</b>
The four letter personality score is reported for each model. Links will take you to the specific report of their scores, which covers their meaning in more detail. In general, it's Extroversion (E) vs Introversion (I), Sensing (S) vs Intuition (N), Thinking (T) vs Feeling (F), Judging (J) vs Perceiving (P). The four letters represent one of 16 possible personality configurations. For example, Davinci is an ESFP, which means that it is extroverted, sensing, feeling, and perceiving.

</p>

## Distribution of Answers
### Patterns
There are some  observed patterns for the models' behavior in selecting answers. 
1) text-curie-001 and text-babbage-001 love C
2) On psychopath screening
    * text-davinci-003 never answered C
    * text-babbage-001 only answered C
        * When given different options it always chose the third
    * text-curie-001 never answered A
3) On Myers-Briggs
    * Each model had a letter they never chose
### Take Aways 
1) Low amount of confidence in behavioral results
2) Higher trust in Qualitative Tests (ACT/LSAT) for text-davinci-003


![image](/results/distribution.png)
<p align=center><b>Figure 5:</b>
Above is the distribution of answers for each test. The top subplots show the deviation from the actual answer for each model. For example, a % error from ground truth of 50% for 'C' means that the model choose 'C' 50% more than 'C' showed up in the correct answer for that test. The bottom subplots show the number of times each model picked a given answer for each test.
</p>


# Possible Avenues of Future Work
1. **Compare Results to Better Language models** 
    * Curie and Babbage seem unable to complete the tasks at hand, exploring more recent and larger models might yield interesting comparison results to Davinci (Chat GPT does incredibly well on math problems)
    * Comparing GPT models to BERT models would be very informative
2. **Prompt Engineering**
    * Can we change the Personality of the model by prefacing the prompt with certain words or phrases?
    * Does changing the way the options are phrased improve test performance?
3. **Moving on from “Zero-shot”**
    * Does prefacing the question with a previous question answer pair improve our results?
    * Can we achieve better performance by fine tuning an open source GPT model on these given test? 
  
# References
1. Saketh Reddy Karra, Son Nguyen, and Theja Tulabandhula. 2022. AI Personification: Estimating the Personality of Language Models. arXiv preprint arXiv:2204.12000 (2022). https://arxiv.org/abs/2204.12000 
2. Asahi Ushio, Luis Espinosa-Anke, Steven Schockaert, and Jose Camacho-Collados. 2021. BERT is to NLP what AlexNet is to CV: can pre-trained language models identify analogies? arXiv preprint arXiv:2105.04949 (2021). https://arxiv.org/abs/2105.04949
3. Wanjun Zhong, Siyuan Wang, Duyu Tang, Zenan Xu, Daya Guo, Jiahai Wang, Jian Yin, Ming Zhou, and Nan Duan. 2021. AR-LSAT: Investigating Analytical Reasoning of Text. arXiv:2104.06598 [cs.CL]. https://github.com/zhongwanjun/AR-LSAT