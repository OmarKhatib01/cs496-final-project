import os
import re
from collections import defaultdict
from dataclasses import dataclass

import dill
from bs4 import BeautifulSoup
from selenium import webdriver


@dataclass
class Question:
	question: str
	answers: list[str]
	correct_answer: int

	def __post_init__(self):
		if self.correct_answer not in range(len(self.answers)):
			raise ValueError("Correct answer idx must be in range of answers")

	def __str__(self) -> str:
		return f"{self.question}\n{self.answers}\nCorrect answer: {self.correct_answer}"

@dataclass
class MathQuestion(Question):
	contains_figure: bool
	contains_script: bool
	
	def __post_init__(self):
		if len(self.answers) != 5:
			raise ValueError("There must be 5 answers")

	def __str__(self) -> str:
		return f"{self.question}\n{self.answers}\nCorrect answer: {self.correct_answer}\nContains figure: {self.contains_figure}\nContains super/sub script: {self.contains_script}"

@dataclass
class ReadingQuestion(Question):
	passage_idx: int
	
	def __post_init__(self):
		if len(self.answers) != 4:
			raise ValueError("There must be 4 answers")

	def __str__(self) -> str:
		return f"Passage Index: {self.passage_idx}\n{self.question}\n{self.answers}\nCorrect answer: {self.correct_answer}"

@dataclass
class EnglishQuestion(Question):
	sample_question: str
	passage_idx: int
	
	def __post_init__(self):
		if len(self.answers) != 4:
			raise ValueError("There must be 4 answers")

	def __str__(self) -> str:
		return f"Passage Index: {self.passage_idx}\n{self.sample_question or self.question}\n{self.answers}\nCorrect answer: {self.correct_answer}"


@dataclass
class ACT():
	questions = defaultdict(list)
	passages = defaultdict(list)
	
	def __post_init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		browser = webdriver.Chrome(options=options, executable_path='chromedriver')

		self._parse_reading(browser)
		self._parse_math(browser)
		self._parse_english(browser)

		browser.quit()


	def _parse_reading(self, browser):
		# get passage, ignore line numbers
		for i in range(5):
			browser.get(f"https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/reading-practice-test-questions.html?page=0&chapter={i}")
			html = browser.page_source
			soup = BeautifulSoup(html, features="html.parser")

			parsed_passage = soup.select('.quiz-area p')
			passage = ''
			for line in parsed_passage:
				if line.span:
					line.span.decompose()
				else:
					passage += f'{line.text} '
			self.passages['reading'].append(passage)

		for i in range(5):
			for j in range(2):
				browser.get(f"https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/reading-practice-test-questions.html?page={j}&chapter={i}")
				html = browser.page_source
				soup = BeautifulSoup(html, features="html.parser")

				parsed_questions = soup.select('.quiz_list')
				for question in parsed_questions:

					# get question
					question_text = question.select_one('p strong').text

					# get answers, and note correct idx
					answers = []
					correct_answer = -1
					for j, answer in enumerate(question.select('.qa-form .radio')):
						meta = answer.select_one('input')
						if meta.attrs['data-correctness'] == 'right':
							correct_answer = j
						answer = answer.select_one('p').text
						answers.append(answer)
					
					# add question to dict
					self.questions['reading'].append(
						ReadingQuestion(
							passage_idx = i,
							question = question_text, 
							answers = answers, 
							correct_answer = correct_answer, 
						)
					)		


	def _parse_math(self, browser):
		for i in range(5):
			browser.get(f"https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/math-practice-test-questions.html?page=0&chapter={i}")
			html = browser.page_source
			soup = BeautifulSoup(html, features="html.parser")

			parsed_questions = soup.select('.individualQuestion')
			for question in parsed_questions:

				# get question, and deal with some bad HTML formatting
				question_text = question.select('p strong')
				question_text = next(filter(lambda x: x.text, question_text)).text
				
				# get answers, and note correct idx
				answers = []
				correct_answer = -1
				for j, answer in enumerate(question.select('.qa-form .radio')):
					meta = answer.select_one('input')
					if meta.attrs['data-correctness'] == 'right':
						correct_answer = j
					answer = answer.select_one('p').text
					# remove '\xa0' from answer
					answer = answer.replace('\xa0', ' ').strip()
					answers.append(answer)

				
				# if question has an image, note that
				contains_figure = bool(question.select_one('img') or question.select_one('table'))

				# if question has a superscript, note that
				contains_script = bool(question.select_one('sup') or question.select_one('sub'))

				# add question to dict
				self.questions['math'].append(
					MathQuestion(
						question = question_text, 
						answers = answers, 
						correct_answer = correct_answer, 
						contains_figure = contains_figure, 
						contains_script = contains_script
					)
				)


	def _parse_english(self, browser):

		for i in range(5):
			browser.get(f"https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/english-practice-test-questions.html?page=0&chapter={i}")
			html = browser.page_source
			soup = BeautifulSoup(html, features="html.parser")

			# get passage with _ in place of underlined words
			parsed_passage = soup.select('.quiz-area p')
			passage = ' '.join([line.text for line in parsed_passage])
			passage = passage.replace(u'\xa0', ' ')
			self.passages['english'].append(passage)

		for i in range(5):
			# get underlined questions
			for j in range(3):
				browser.get(f"https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/english-practice-test-questions.html?page={j}&chapter={i}")
				html = browser.page_source
				soup = BeautifulSoup(html, features="html.parser")

				underlines = soup.select('.quiz-area p span')
				quizzes = [underline.text for underline in underlines]

				parsed_questions = soup.select('.quiz_list')
				for question in parsed_questions:
					# get question
					question_text = question.select_one('p strong').text.strip()
					sample_question_text = None

					# get quiz index
					idx = int(question.select_one('.order-list-no').text[:-1]) - 1
					context = quizzes[idx]
					passage = self.passages['english'][i]
					passage_idx_s = passage.find(context)

					# form new question if question is 'Choose the best answer.
					if re.match(question_text, r'Choose the best answer?.'):
						question_preface = 'Fill in the _:\n'

						# Create a sample question for printing purposes
						sentence_idx_s = passage.rfind('.', 0, passage_idx_s) + 2
						sentence_idx_e = passage.find('.', passage_idx_s)
						sample_passage = passage[max(0, sentence_idx_s):sentence_idx_e + 1]
						sample_question_text = question_preface + sample_passage.replace(context, '_')

						question_text = question_preface + passage.replace(context, '_')

					# get answers, and note correct idx
					answers = []
					correct_answer = -1
					for j, answer in enumerate(question.select('.qa-form .radio')):
						meta = answer.select_one('input')
						if meta.attrs['data-correctness'] == 'right':
							correct_answer = j
						answer = answer.select_one('p').text
						if answer == 'NO CHANGE':
							answer = context
						answers.append(answer.replace(u'\xa0', '').strip())

					# add question to dict
					self.questions['english'].append(
						EnglishQuestion(
							passage_idx = i,
							sample_question = sample_question_text,
							question = question_text, 
							answers = answers, 
							correct_answer = correct_answer, 
						)
					)	


	def print_reading(self):
		old_idx = -1
		for i, question in enumerate(self.questions['reading']):
			if question.passage_idx != old_idx:
				print(f'{self.passages["reading"][question.passage_idx]}\n')
				old_idx = question.passage_idx
			print(f'{i+1}\n{question}\n')


	def print_math(self, only_valid=False):
		math_questions = self.questions['math']
		if only_valid:
			math_questions = filter(lambda x: not x.contains_figure and not x.contains_script, self.questions['math'])
		for i, question in enumerate(math_questions):
			print(f'{i+1}\n{question}\n')
		

	def print_english(self):
		old_idx = -1
		for i, question in enumerate(self.questions['english']):
			if question.passage_idx != old_idx:
				print(f'{self.passages["english"][question.passage_idx]}\n')
				old_idx = question.passage_idx
			print(f'{i+1}\n{question}\n')

def main():
	act = None
	# doesn't work for some reason rn
	if os.path.exists('act.obj'):
		with open('act.obj', 'rb') as f:
			act = dill.load(f)
	else:
		act = ACT()
		with open('act.obj', 'wb') as f:
			dill.dump(act, f)

	act.print_reading()
	act.print_math(only_valid=True)
	act.print_english()


if __name__ == '__main__':
	main()