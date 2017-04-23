from document_retriever import DocumentRetriever
import pickle


DATA_DIRECTORY_PATH = "../data/"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus"
COMPUTER_SCIENCE_QUERIES_PATH = DATA_DIRECTORY_PATH + "computer_science_queries.txt"
CORPUS_EXTENSION = ".dat"


COMPUTER_SCIENCE_QUERIES = [#"Artificial+Intelligence",
                            "Computation+and+Language",
			    "Computational+Complexity",
			    "Computational+Engineering,+Finance,+and+Science",
		            "Computational+Geometry",
			    "Computer+Science+and+Game+Theory",
			    "Computer+Vision+and+Pattern+Recognition",
			    "Computers+and+Society",
			    "Cryptography+and+Security",
			    "Data+Structures+and+Algorithms",
			    #"Databases",
			    "Digital+Libraries",
			    "Discrete+Mathematics",
			    "Distributed,+Parallel,+and+Cluster+Computing",
			    "Emerging Technologies",
			    "Formal Languages and Automata Theory",
		            "General Literature",
			    "Graphics",
			    "Hardware Architecture",
			    "Human-Computer Interaction",
			    "Information Retrieval",
			    "Information Theory",
			    "Machine Learning",
			    "Logic in Computer Science",
			    "Mathematical Software",
			    "Multiagent Systems",
			    "Multimedia",
			    "Networking and Internet Architecture",
			    "Neural and Evolutionary Computing",
			    "Numerical Analysis",
			    "Operating Systems",
			    "Performance",
			    "Programming Languages",
			    "Robotics",
			    "Social and Information Networks",
			    "Software Engineering",
			    "Sound",
			    "Symbolic Computation",
			    "Systems and Control"]

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
		
			documents, metadata = document_retriever.getDocuments(query, 50)
			document_retriever.processDocuments(documents, metadata)
			
			del document_retriever
			

def main():
	computer_science_corpus = Corpus(COMPUTER_SCIENCE_CORPUS_PATH)
	#print "Total documents: ", computer_science_corpus.numberOfDocuments()
	#print "Total words: ", computer_science_corpus.totalWords()
	#print "Frequency of 'the': ", computer_science_corpus.wordFrequency("the")
	#print "Frequency of 'algorithm': ", computer_science_corpus.wordFrequency("algorithm")
	#print "Frequency of 'philosophy': ", computer_science_corpus.wordFrequency("philosophy")
	#print "Frequency of 'Donald': ", computer_science_corpus.wordFrequency("Donald")
	#print "Frequency of 'Knuth': ", computer_science_corpus.wordFrequency("Knuth")
	#print "Frequency of 'artificial': ", computer_science_corpus.wordFrequency("artificial")
	#print "Frequency of 'intelligence': ", computer_science_corpus.wordFrequency("intelligence")
	#print "Frequency of 'India': ", computer_science_corpus.wordFrequency("India")
	computer_science_corpus.buildCorpus()
	

	
if __name__ == "__main__":
	main()
