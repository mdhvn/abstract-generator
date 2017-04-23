from document_retriever import DocumentRetriever
import pickle


DATA_DIRECTORY_PATH = "../data/"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus"
COMPUTER_SCIENCE_QUERIES_PATH = DATA_DIRECTORY_PATH + "computer_science_queries.txt"
CORPUS_EXTENSION = ".dat"

class Corpus(object):
	
	def __init__(self, corpus_path):
		self.corpus_path = corpus_path + CORPUS_EXTENSION
		self.metadata_path = corpus_path + "_metadata" + CORPUS_EXTENSION
		
		self.load()

	def load(self):
		self.corpus_file = open(self.corpus_path, "rb")
		self.metadata_file = open(self.metadata_path, "rb")
		
		# Do we need to deal with this at all?
		try:
			self.corpus = pickle.load(self.corpus_file)
		except:
			self.corpus = { }
		
		try:
			self.metadata = pickle.load(self.metadata_file)
		except:
			self.metadata = { }

		self.corpus_file.close()
		self.metadata_file.close()

	def numberOfDocuments(self):
		return len(self.metadata)

	def totalWords(self):
		return sum(self.corpus.values())

	def wordFrequency(self, word):
		if word in self.corpus:
			return self.corpus[word]
		else:
			return 0

	def reload(self):
		self.loadCorpus()

	def getQueriesFromFile(self):
		queries_file = open(COMPUTER_SCIENCE_QUERIES_PATH, "r")
		queries = queries_file.read().splitlines()

		for query in range(0, len(queries)):
			queries[query] = queries[query].replace(" ", "+")

		return queries

	def buildCorpus(self):
		for query in self.getQueriesFromFile():
			document_retriever = DocumentRetriever()
		
			print ""
			print query
			print ""
		
			documents, metadata = document_retriever.getDocuments(query, 20)
			document_retriever.processDocuments(documents, metadata)
			
			del document_retriever
	
	def clearCorpus(self):
		self.corpus_file = open(self.corpus_path, "w").close()
		self.metadata_file = open(self.metadata_path, "w").close()
		print "Cleared corpus and metadata files"

def main():
	computer_science_corpus = Corpus(COMPUTER_SCIENCE_CORPUS_PATH)
	print "Total documents: ", computer_science_corpus.numberOfDocuments()
	print "Total words: ", computer_science_corpus.totalWords()
	print "Frequency of 'the': ", computer_science_corpus.wordFrequency("the")
	print "Frequency of 'algorithm': ", computer_science_corpus.wordFrequency("algorithm")
	print "Frequency of 'philosophy': ", computer_science_corpus.wordFrequency("philosophy")
	print "Frequency of 'Donald': ", computer_science_corpus.wordFrequency("Donald")
	print "Frequency of 'Knuth': ", computer_science_corpus.wordFrequency("Knuth")
	print "Frequency of 'artificial': ", computer_science_corpus.wordFrequency("artificial")
	print "Frequency of 'intelligence': ", computer_science_corpus.wordFrequency("intelligence")
	print "Frequency of 'India': ", computer_science_corpus.wordFrequency("India")
	#computer_science_corpus.buildCorpus()
	#computer_science_corpus.clearCorpus()

	
if __name__ == "__main__":
	main()
