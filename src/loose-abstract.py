import codecs
from corpus import Corpus
import math
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk import FreqDist
import operator
import string
#from textblob import TextBlob
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

def cleanToken(token):
	token = token.lstrip()
	token = token.rstrip()
	return token

def isValid(token):
	if token in string.punctuation:
		return False

	return True

def main():
	contents = readFile("../data/test/recommender_systems.txt")

	sentences = sent_tokenize(contents)
	tokens = word_tokenize(contents)
	frequency_distribution = FreqDist(tokens)
	number_of_samples = len(frequency_distribution)
	word_counts = frequency_distribution.most_common(number_of_samples)
	
	computer_science_corpus = Corpus(COMPUTER_SCIENCE_CORPUS_PATH)
	print "Frequency of 'the' (document): ",

	for word_count_pair in word_counts:
		if (word_count_pair[0] == "the"):
			print word_count_pair[1]
			break

	print "Frequency of 'the' (corpus): ", computer_science_corpus.wordFrequency("the")

	tf_idf = { }

	tf_idf_scores = { }

	# Clean tokens; move this step to when tokens are first
        # added to the corpus.
	for token in range(0, len(tokens)):
		tokens[token] = cleanToken(tokens[token])

	for token in tokens:
		if isValid(token):
			tf_idf_scores[token] = TF_IDF(token, word_counts, computer_science_corpus)

	tf_idf_scores = sorted(tf_idf_scores.items(), key = operator.itemgetter(1), reverse = True)

	sentences_used = [ ]

	for word_score_pair in tf_idf_scores:
		word = word_score_pair[0]
		score = word_score_pair[1]
		
		print ""
		print ""
		print ""
		print ""
		print "Word: ", word, ": ", score
		
		for sentence in sentences:
			if word not in sentence:
				pass
			else:	
				if sentence not in sentences_used:
					#sentence_sentiment = TextBlob(sentence)
					print "\t - ", sentence
					#print "\t", "-", sentence, sentence_sentiment.sentiment
					sentences_used.append(sentence)
					break

		print "-------------------------------------------"
			

	for sentence in sentences:
		total_score = 0
		
		words = sentence.split()
	
		for word in words:
			total_score = total_score + TF_IDF(word, word_counts, computer_science_corpus)

		tf_idf[sentence] = total_score

	sorted_sentence_scores = sorted(tf_idf.items(), key = operator.itemgetter(1), reverse = True)

	#for sentence_score_pair in range(0, 10):
	#	sentence = sorted_sentence_scores[sentence_score_pair][0]
	#	score = sorted_sentence_scores[sentence_score_pair][1]
	#	
	#	print ""
	#	print ""
	#	print ""
	#	print ""
	#	print "==============================="
	#	print sentence, score
	#		

main()
