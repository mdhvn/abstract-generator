from document_processor import DocumentProcessor
from document_retriever import DocumentRetriever
import os
import pickle
import time

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

	def documentsByCategory(self, category):
		documents = [ ]

		for document in self.metadata:
			if category == document["category"]:
				documents.append(document)

		return documents
				

	def reload(self):
		self.loadCorpus()

	def containsDocument(self, document):
		return (document["id"] in self.metadata)
		
	def getQueriesFromFile(self):
		queries_file = open(COMPUTER_SCIENCE_QUERIES_PATH, "r")
		queries = queries_file.read().splitlines()

		for query in range(0, len(queries)):
			queries[query] = queries[query].replace(" ", "+")

		return queries

	def addTokensToCorpus(self, tokens):
		unique_tokens = set(tokens)

		for token in unique_tokens:
			if token in self.corpus:
				self.corpus[token] = self.corpus[token] + 1
			else:
				self.corpus[token] = 0
		

	def buildCorpus(self):
		for query in self.getQueriesFromFile():
			document_retriever = DocumentRetriever()
		
			print ""
			print query
			print ""
		
			documents, metadata = document_retriever.getDocuments(query, 10)

			for document in documents:
				if not self.containsDocument(document):
					document_id = document["id"]
					document_text_file_path = ""

					try:
						document_text_file_path = document_retriever.getDocumentTextFile(document)
						# print?
					except Exception as exception:
						# count failure
						# print
						print " - failed (", str(type(exception).__name__), ")" 

						if (len(document_text_file_path) != 0):
							os.remove(document_text_file_path)
		
					else:
						print " - succeeded"
						# GET DATA BACK FROM THE PROCESSOR
						document_processor = DocumentProcessor(document_text_file_path)
						tokens = document_processor.getTokens()
						
						self.addTokensToCorpus(tokens)
						self.metadata[document_id] = metadata[document_id]
						self.writeCorpusToDisk()
						
						if (len(document_text_file_path) != 0):
							os.remove(document_text_file_path)

						# count success
				else:
					print "- Document already in corpus"

					

							
	
			# Add retries for documents not received:
			# 	1) When fewer documents are retrieved than requested.
			# 	2) When a retrieved document already exists.

			# document_retriever.py should download a document, store it on disk
			# and return the path to the document. 

			# Let corpus.py send the document for processing
			# and delete the file. 

			#document_retriever.processDocuments(documents, metadata)
			#print "Documents: ", len(documents)
			#print "Verifying with metadata: ", len(metadata)
			
			#del document_retriever

			#print "Waiting for 3 seconds..."
			time.sleep(1)
	
	def clearCorpus(self):
		self.corpus_file = open(self.corpus_path, "w").close()
		self.metadata_file = open(self.metadata_path, "w").close()

		self.corpus = { }
		self.metadata = { }

		print "Cleared corpus and metadata files"

	def writeCorpusToDisk(self):
		self.corpus_file = open(self.corpus_path, "wb")
		self.metadata_file = open(self.metadata_path, "wb")

		pickle.dump(self.corpus, self.corpus_file)
		pickle.dump(self.metadata, self.metadata_file)	

		self.corpus_file.close()
		self.metadata_file.close()

	def __del__(self):
		self.writeCorpusToDisk()

def main():
	computer_science_corpus = Corpus(COMPUTER_SCIENCE_CORPUS_PATH)
	print "Total documents: ", computer_science_corpus.numberOfDocuments()
	#print "Total words: ", computer_science_corpus.totalWords()
	#print "Frequency of 'the': ", computer_science_corpus.wordFrequency("the")
	#print "Frequency of 'algorithm': ", computer_science_corpus.wordFrequency("algorithm")
	#print "Frequency of 'philosophy': ", computer_science_corpus.wordFrequency("philosophy")
	#print "Frequency of 'Donald': ", computer_science_corpus.wordFrequency("Donald")
	#print "Frequency of 'Knuth': ", computer_science_corpus.wordFrequency("Knuth")
	#print "Frequency of 'artificial': ", computer_science_corpus.wordFrequency("artificial")
	#print "Frequency of 'intelligence': ", computer_science_corpus.wordFrequency("intelligence")
	#print "Frequency of 'India': ", computer_science_corpus.wordFrequency("India")
	#print "Number of documents on 'Formal Languages': ", computer_science_corpus.wordFrequency("cs.FL")
	#print "Number of documents on 'Distributed and Parallel Computing': ", computer_science_corpus.wordFrequency("cs.DC")
	#print "Number of documents on 'Artificial Intellgience': ", computer_science_corpus.wordFrequency("cs.AI")
	#print "Number of documents on 'Hardware Architecture': ", computer_science_corpus.wordFrequency("cs.AR")
	#print "Number of documents on 'Databases': ", computer_science_corpus.wordFrequency("cs.DB")
	#computer_science_corpus.buildCorpus()
	#computer_science_corpus.clearCorpus()

	
if __name__ == "__main__":
	main()
