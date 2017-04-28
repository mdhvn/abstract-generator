import codecs
import copy
from corpus import Corpus
import math
import nltk
from nltk import FreqDist
from nltk import word_tokenize
from nltk import sent_tokenize
import operator
import string
from unidecode import unidecode

DATA_DIRECTORY_PATH = "../data/"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus"
STOP_WORDS_PATH = DATA_DIRECTORY_PATH + "stop_words.txt"

special_words = ["goal",
	 "summary",
	 "research",
	 "conclusion",
	 "to this end",
         #"then",
         "we then",
	 "show",
         "believe",
	 #"in",
	 "this",
	 "paper",
	 "in this paper",
	 "present",
         "novel",
         "problem",
         "evaluate",
	 "results",
         "improves",
	 "outperforms",
         "our",
         "explore",
         "try",
         "reveal",
         "show",
         "prior",
         "previous",
	 "described",
	 "achieves",
         "in conclusion",
         "finally",
	 "%",
         "this problem",
         "in this work",
         "we consider",
         "introduce",
         "our approach",
         "improve",
         "result",
         "seminal",
         "consider",
         "main",
         "we propose",
         "we",
         "investigate",
         "in this context",
         "aims",
         "experiments",
         "describes"]

# Go through a lot of abstracts and count the frequencies of all the words
# that occur over the entire collection of abstracts. Weigh (sentences with)
# these words higher in the query document.

# Past-tense verbs?
# Use POS tagging to identify words that signify:
#	- Possession ("our results show...")
# 	- Past tense ("we computed the score...")
# 	as well as present tense ("we then find the maximum value...")

# Look for numbers ("64% improvement...")

# Weigh words/sentences more heavily for having:
#	- Words that occur in the title
# 	- Words that feature commonly in abstracts

# https://arxiv.org/pdf/1704.07649.pdf
# https://arxiv.org/pdf/1704.05263.pdf
# https://arxiv.org/pdf/1703.07194.pdf
# https://arxiv.org/pdf/1704.07619.pdf

class Abstract(object):

    def __init__(self, filename):
        self.document = self.getDocumentContents(filename)
        self.processDocument()
        
        # For now, always use the Computer Science corpus.
        self.corpus = Corpus(COMPUTER_SCIENCE_CORPUS_PATH)
        
        self.abstract = self.createAbstract()
        
    def getDocumentContents(self, filename):
        document_file = codecs.open(filename, "r", "utf-8")
	contents = document_file.read()
	contents = unidecode(contents)
	document_file.close()
	
	return contents

    def getAbstract(self):
        #document_lowercase = self.document.lower()
	#start_of_abstract = document_lowercase.index("abstract")
	#end_of_abstract = document_lowercase.index("introduction")
	#abstract = self.document[start_of_abstract : end_of_abstract]
	return self.abstract

    def tf_idf(self, word):
	# Normalize the term frequency for document length.
	# https://www.cs.bgu.ac.il/%7Eelhadad/nlp16/nenkova-mckeown.pdf
	term_frequency = self.word_frequencies[word]
	#term_frequency = float(self.word_frequencies[word])
	#term_frequency = term_frequency / self.word_frequencies[self.most_frequent_word]
	#print term_frequency

        number_of_documents = self.corpus.numberOfDocuments()
        frequency_in_corpus = self.corpus.wordFrequency(word)

        inverse_document_frequency = number_of_documents / (1 + frequency_in_corpus)

        # FIX!!!!
        # The frequency in corpus for any term cannot be greater
        # than the number of documents in the corpus. Fix this
        # during corpus processing. Remove the +1 from argument
        # to math.log().
        try:
            inverse_document_frequency = math.log(1 + inverse_document_frequency)
        except:
            print "Number of documents: ", number_of_documents
            print "Frequency in corpus: ", frequency_in_corpus

        tf_idf = term_frequency * inverse_document_frequency

        return tf_idf


    def getStopWords(self):
		stop_words_file = open(STOP_WORDS_PATH, "r")
		stop_words = stop_words_file.read().splitlines()
		
		return stop_words

    def calculateTFIDF(self):
        word_tf_idf_scores = { }
        stop_words = self.getStopWords()

        for word in self.word_frequencies:
            if word in stop_words:
                word_tf_idf_scores[word] = 0
            else:
                word_tf_idf_scores[word] = self.tf_idf(word)

        self.sorted_word_tf_idf_scores = sorted(word_tf_idf_scores.items(),
                                                key = operator.itemgetter(1),
                                                reverse = True)

        for word_score_tuple in self.sorted_word_tf_idf_scores:
            print word_score_tuple

        self.word_tf_idf_scores = dict(self.sorted_word_tf_idf_scores)

    def calculateSentenceScores(self):
        self.sentence_tf_idf_scores = { }

	for sentence in self.sentences:
		sentence_score = 0
		
		for word in sentence:
			if word in self.word_tf_idf_scores:
				sentence_score = sentence_score + self.word_tf_idf_scores[word]

		self.sentence_tf_idf_scores[sentence] = sentence_score


        self.sorted_sentence_tf_idf_scores = sorted(self.sentence_tf_idf_scores.items(),
                                                    key = operator.itemgetter(1),
                                                    reverse = True)

    def getAverageSentenceTFIDFScore(self):
	total_tf_idf_score = 0

	for sentence in self.sentence_tf_idf_scores:
		total_tf_idf_score = total_tf_idf_score + self.sentence_tf_idf_scores[sentence]

	return (total_tf_idf_score / len(self.sentence_tf_idf_scores))

    def selectSentences(self):
	# Set up a score for each sentence in this document. 
        # This dictionary stores the main score for each sentence, which 
        # is derived of/from other (smaller) subscores. The sentences with the
        # highest scores are used to form a summary for this document.
	self.sentence_scores = { }
                
	# Initialize every sentence's score to 0.
	for sentence in self.sentences:
		self.sentence_scores[sentence] = 0


	# For every word, add its tf-idf score to the sentence it
	# first occurs in.
	sentences_seen = [ ]
	sentences_seen_per_word = dict.fromkeys(self.word_tf_idf_scores.keys(), 0)

	for word_score_tuple in self.sorted_word_tf_idf_scores:
		word = word_score_tuple[0]
		score = word_score_tuple[1]
		#print word_score_tuple

		for sentence in self.sentences:
			if word in sentence:
				if sentence not in sentences_seen:
					occurrences = sentences_seen_per_word[word]

					if occurrences < self.number_of_sentences:
						self.sentence_scores[sentence] = self.sentence_scores[sentence] + score
						#sentences_seen.append(sentence)

						sentences_seen_per_word[word] = occurrences + 1

	# To begin with, score each sentence based on where in the paper (how early)
        # it occurs. The earlier it occurs, the higher its score. This score arises
        # from the observation that most abstracts tend to have same order and logical 
	# flow as the (rest of the) paper to which they belong.
	# for sentence_index in range(0, len(self.sentences)):
	# 	sentence = self.sentences[sentence_index]
	# 	self.sentence_scores[sentence] = len(self.sentences) - sentence_index
	# 	#self.sentence_scores[sentence] = math.pow(self.sentence_scores[sentence], 2)
	# 	self.sentence_scores[sentence] = math.pow(2, self.sentence_scores[sentence])

	# Add each sentence's tf-idf score to its overall score.
	#for sentence in self.sentence_tf_idf_scores:
	# 	# +1 to tf_idf_score
	 	#tf_idf_score = math.pow(self.sentence_tf_idf_scores[sentence] + 1, 1)
		#self.sentence_scores[sentence] = self.sentence_scores[sentence] * tf_idf_score
		#self.sentence_scores[sentence] = self.sentence_scores[sentence] + self.sentence_tf_idf_scores[sentence]

	# Increase each sentence's score by a factor of 1.5 for every word it
        # contains that is in the title of the document.
	print self.title_tokens

	for sentence_index in range(0, len(self.sentences)):
		sentence = self.sentences[sentence_index]
	 	sentence_tokens = sentence.lower().split()

		seen_in_title = [ ]
		
		number_of_title_words = 0

	 	for token in sentence_tokens:
	 		if token in self.title_tokens:
				number_of_title_words = number_of_title_words + 1
				seen_in_title.append(token)
	
		#print number_of_title_words, seen_in_title, sentence

		self.sentence_scores[sentence] = self.sentence_scores[sentence] * math.pow(1.1, number_of_title_words)

	# Take the logarithm of each score.
	# for sentence in self.sentence_scores:
	# 	self.sentence_scores[sentence] = math.log(self.sentence_scores[sentence])

	# For every word w, add w's tf-idf score to the sentence it 
        # first occurs in.
	# for word_score_tuple in self.sorted_word_tf_idf_scores:
	# 	word = word_score_tuple[0]
	# 	score = word_score_tuple[1]
		
	# 	for sentence in self.sentences:
	# 		if word in sentence:
	# 			score = math.pow(score, 2)
	# 			self.sentence_scores[sentence] = self.sentence_scores[sentence] + score
	# 			break

	for sentence in self.sentences:
		sentence_lowercase = sentence.lower()

	 	for word in special_words:
	 		word = word.lower()

	 		if word in sentence_lowercase:
	 			word_tokens = word.split()
	 			#multiplier = math.pow(len(word_tokens), 2) + 0.5
	 			#print multiplier
	 			self.sentence_scores[sentence] = self.sentence_scores[sentence] * (len(word_tokens) + 1)

	########## Output ##########
	# for sentence in self.sentence_scores:
	# 	self.sentence_scores[sentence] = math.log(self.sentence_scores[sentence])

	self.sorted_sentence_scores = sorted(self.sentence_scores.items(),
                                             key = operator.itemgetter(1),
                                             reverse = True)


	for sentence_score_tuple in self.sorted_sentence_scores:
		sentence = sentence_score_tuple[0]
		score = sentence_score_tuple[1]

		print "===================="
		print sentence
		print ""
		print score
		print ""

    def createAbstractString(self):
	sentence_score_tuples = self.sorted_sentence_scores[:self.number_of_sentences]

	sentences = [ ]
   
        for sentence_score_tuple in sentence_score_tuples:
		sentences.append(sentence_score_tuple[0])

	return " ".join(sentences)
        
    def createAbstract(self):
	self.number_of_sentences = 10

        self.calculateTFIDF()               # Calculate the tf-idf score for every word in this document.
        self.calculateSentenceScores()      # Calculate the total tf-idf score for every sentence in this document.
	
	#for word_score_tuple in self.sorted_word_tf_idf_scores:
	#	print word_score_tuple

	self.selectSentences()

	return self.createAbstractString()


	####################
	# sentences_seen = { }

	# for word_score_tuple in self.sorted_word_tf_idf_scores:
	# 	word = word_score_tuple[0]

	# 	for sentence in self.sentences:
	# 		if (word in sentence):
 	#                       if sentence in sentences_seen:
	# 				sentences_seen[sentence] = sentences_seen[sentence] + 1
	# 			else:	
	# 				print "===================="
	# 				print sentence
	# 				sentences_seen[sentence] = 1
	# 			break
					
	# 	if (len(sentences_seen) > 10):
	# 		break

    def getTitle(self):
	#print "First sentence: ", self.sentences[0]
        first_whitespace = self.document.find(" ")
        first_newline = self.document.find("\n")
        
        #print first_newline
	
        return self.document[0 : first_newline]

    def removeReferences(self):
        # Finish this
        
        # May need try-catch-else over here for words
        # that don't occur in documents.

        # Assume that the occurrence of 'REFERENCES' denotes
        # the start of a References section, and that this
        # section is the last in the paper.
        section_index = self.document.find("REFERENCES")

        # Title
        # Acknowledgements
        # Citations
        # Appendices
        # Introduction
        # Conclusion and Future Work
        # Results
        # References
        # Experiments
        # Related Work
        # Discussion
        
        word_index = self.document.find("references")

        if section_index > word_index:
            self.references = self.document[section_index : len(self.document)]
            self.document = self.document[0 : section_index]

        print self.references

    def cleanTokens(self):
        tokens_to_delete = [ ]

        for token in range(0, len(self.tokens)):
            self.tokens[token] = self.tokens[token].strip()
            
            if self.tokens[token] in string.punctuation:
                tokens_to_delete.append(self.tokens[token])

        for token in tokens_to_delete:
            self.tokens.remove(token)

    def cleanSentences(self):
        for sentence in range(0, len(self.sentences)):
            self.sentences[sentence] = self.sentences[sentence].strip()
            self.sentences[sentence] = self.sentences[sentence].replace('\n', ' ')
            self.sentences[sentence] = self.sentences[sentence].replace('\t', ' ')

    def getSectionIndex(self, section_name):
	section_index = self.document.find(section_name.upper())

	if section_index == -1:
		section_index = self.document.find(section_name.capitalize())

	return section_index
		
    
    def processDocument(self):
        self.title = self.getTitle()
	self.title_tokens = self.title.lower().split()

        print "Title: ", self.title
        print ""
        
        # Start the document at the introduction(?)
        # Fix section identification
	# skip past the abstract
        introduction_index = self.document.find("INTRODUCTION")

	if (introduction_index == -1):
		introduction_index = self.document.find("Introduction")
	if (introduction_index == -1):
		introduction_index = 0
		
	#print ""
	#print self.document[introduction_index : len(self.document)]
	
        self.original_document = self.document
        self.document = self.document[introduction_index : len(self.document)]
        
        self.tokens = word_tokenize(self.document)
        self.cleanTokens()
        
        self.sentences = sent_tokenize(self.document)
        self.cleanSentences()
        
        self.frequency_distribution = FreqDist(self.tokens)
        self.number_of_unique_tokens = self.frequency_distribution.N()
        self.word_frequencies = dict(self.frequency_distribution.most_common
                                    (self.number_of_unique_tokens))
	
	#print (self.frequency_distribution.most_common(10))

	#print "Maximum word frequency: ", self.most_frequent_word, "(", self.word_frequencies[self.most_frequent_word], ")"


        #self.removeReferences() (include?)
        #print self.document
        
        #for sentence in self.sentences:
        #    print ""
        #    print ""
        #    print "===================="
        #    print sentence
        #    print "===================="

def main():
        document_path = "../data/test/human_computer_interaction.txt"

        abstract = Abstract(document_path)
        print abstract.getAbstract()

if __name__ == "__main__":
    main()
