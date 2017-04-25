import codecs
from corpus import Corpus
import math
from nltk import FreqDist
from nltk import word_tokenize
from nltk import sent_tokenize
import operator
import string
from unidecode import unidecode

DATA_DIRECTORY_PATH = "../data/"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus"

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
        term_frequency = self.word_frequencies[word]

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

    def calculateTFIDF(self):
        word_tf_idf_scores = { }

        for word in self.word_frequencies:
            word_tf_idf_scores[word] = self.tf_idf(word)

        self.word_tf_idf_scores = sorted(word_tf_idf_scores.items(),
                                         key = operator.itemgetter(1),
                                         reverse = True)

        for word in self.word_tf_idf_scores:
            print word

        self.word_tf_idf_scores = dict(self.word_tf_idf_scores)
        
    def createAbstract(self):
        self.calculateTFIDF()
        
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
    
    def processDocument(self):        
        self.tokens = word_tokenize(self.document)
        self.cleanTokens()
        self.sentences = sent_tokenize(self.document)
        self.frequency_distribution = FreqDist(self.tokens)
        self.number_of_unique_tokens = self.frequency_distribution.N()
        self.word_frequencies = dict(self.frequency_distribution.most_common
                                    (self.number_of_unique_tokens))

        #self.removeReferences() (include?)
        #print self.document
        
        #for sentence in self.sentences:
        #    print ""
        #    print ""
        #    print "===================="
        #    print sentence
        #    print "===================="

def main():
        computational_theory_path = "../data/test/human_computer_interaction.txt"

        abstract = Abstract(computational_theory_path)
        print abstract.getAbstract()

if __name__ == "__main__":
    main()