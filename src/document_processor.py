import codecs
import copy
from nltk import word_tokenize
from nltk import FreqDist
import os
import pickle
import string
import textract
from unidecode import unidecode

DATA_DIRECTORY_PATH = "../data/"
TEST_DATA_DIRECTORY_PATH = DATA_DIRECTORY_PATH + "test/"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus.dat"

class DocumentProcessor(object):

	def __init__(self, filename):
		self.filename = filename
		self.readFileContents()

	def readFileContents(self):
		documentFile = codecs.open(self.filename, "r", "utf-8")
		self.documentContents = documentFile.read()
		self.documentContents = unidecode(self.documentContents)  # Decode to ASCII
		documentFile.close()

	def processText(self):
		self.tokens = word_tokenize(self.documentContents)
		self.frequency_distribution = FreqDist(self.tokens)
		self.number_of_samples = len(self.frequency_distribution)
		self.word_counts = self.frequency_distribution.most_common(self.number_of_samples)
		
		cleaned_token_list = [ ]

		# Clean the list
		for token in self.tokens:
			if token not in string.punctuation:
				cleaned_token_list.append(token)
		
		self.tokens = cleaned_token_list[:]

		#self.word_count_dictionary = { }

		#for word_count in self.word_counts:
		#	word = word_count[0]
		#	count = word_count[1]
                #
		#	self.word_count_dictionary[word] = count

	def appendToCorpus(self, corpus, word_count_dictionary):
		for word in word_count_dictionary:
			if word in corpus:
				#corpus[word] = corpus[word] + word_count_dictionary[word]
				corpus[word] = corpus[word] + 1
			else:
				corpus[word] = word_count_dictionary[word]

	def countTokensInCorpus(self, tokens):
		# Fix/improve this
		tokens_seen = { }

		for token in tokens:
			if token not in tokens_seen:
				tokens_seen[token] = 1

		return tokens_seen

	def writeToCorpus(self):
		corpus_file = open(COMPUTER_SCIENCE_CORPUS_PATH, "rb")
		
		corpus = { }

		if (len(corpus_file.read()) != 0):
			corpus_file.seek(0)  # Reset the file pointer.
			corpus = pickle.load(corpus_file)
			corpus_file.close()
		
		# Fix this
		# self.appendToCorpus(corpus, self.word_count_dictionary)
		tokens_seen_in_document = self.countTokensInCorpus(self.tokens)		
		self.appendToCorpus(corpus, tokens_seen_in_document)

		corpus_file = open(COMPUTER_SCIENCE_CORPUS_PATH, "wb")
		pickle.dump(corpus, corpus_file)
		corpus_file.close()

	def getFileContents(self):
		return self.documentContents

	def getMostCommonWords(self, number_of_words):
		return self.frequency_distribution.most_common(number_of_words)

	def readCorpus(self):
		corpus_file = open(COMPUTER_SCIENCE_CORPUS_PATH, "rb")
		corpus = pickle.load(corpus_file)
		corpus_file.close()

		for word in corpus:
			print word, ":", corpus[word]

		print("\n")
		print("the: ", corpus["the"])

def main():
	information_theory_path = TEST_DATA_DIRECTORY_PATH + "information_theory.txt"
	computation_philosophy_path = TEST_DATA_DIRECTORY_PATH + "computational_philosophy.txt"
	human_computer_interaction_path = TEST_DATA_DIRECTORY_PATH + "human_computer_interaction.txt"
	recommender_systems_path = TEST_DATA_DIRECTORY_PATH + "recommender_systems.txt"

	information_theory = DocumentProcessor(information_theory_path)
	information_theory.processText()
	information_theory.writeToCorpus()

	computational_philosophy = DocumentProcessor(computational_philosophy_path)
	computational_philosophy.processText()
	computational_philosophy.writeToCorpus()

	human_computer_interaction = DocumentProcessor(human_computer_interaction_path)
	human_computer_interaction.processText()
	human_computer_interaction.writeToCorpus()

	recommender_systems = DocumentProcessor(recommender_systems_path)
	recommender_systems.processText()
	recommender_systems.writeToCorpus()


if __name__ == "__main__":
	main()
