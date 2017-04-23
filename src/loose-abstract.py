import codecs
from corpus import Corpus
import math
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk import FreqDist
import operator
from unidecode import unidecode

DATA_DIRECTORY_PATH = "../data/"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus"
CORPUS_EXTENSION = ".dat"

def readFile(filename):
	document_file = codecs.open(filename, "r", "utf-8")
	contents = document_file.read()
	contents = unidecode(contents)
	document_file.close()

	return contents

def TF_IDF(word, word_counts, corpus):
	frequency_in_document = 0
	frequency_in_corpus = corpus.wordFrequency(word)
	number_of_documents = corpus.numberOfDocuments()

	for word_count_pair in word_counts:
		current_word = word_count_pair[0]
		current_count = word_count_pair[1]
		
		if (current_word == word):
			frequency_in_document = current_count

	#print word, frequency_in_document

	term_frequency = frequency_in_document

	inverse_document_frequency = math.log(1 + (number_of_documents / (1 + frequency_in_corpus)))

	return (term_frequency * inverse_document_frequency)


def main():
	contents = readFile("../data/test/computational_theory.txt")

	sentences = sent_tokenize(contents)
	tokens = word_tokenize(contents)
	frequency_distribution = FreqDist(tokens)
	number_of_samples = len(frequency_distribution)
	word_counts = frequency_distribution.most_common(number_of_samples)
	
	computer_science_corpus = Corpus(COMPUTER_SCIENCE_CORPUS_PATH)

	tf_idf = { }

	for sentence in sentences:
		total_score = 0
		
		words = sentence.split()
	
		for word in words:
			total_score = total_score + TF_IDF(word, word_counts, computer_science_corpus)

		tf_idf[sentence] = total_score

	sorted_sentence_scores = sorted(tf_idf.items(), key = operator.itemgetter(1), reverse = True)

	for sentence_score_pair in range(0, 10):
		sentence = sorted_sentence_scores[sentence_score_pair][0]
		score = sorted_sentence_scores[sentence_score_pair][1]
		
		print ""
		print ""
		print ""
		print ""
		print "==============================="
		print sentence, score
			

main()
