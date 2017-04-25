import arxiv
from document_processor import DocumentProcessor
import os
import pickle
import textract

DATA_DIRECTORY_PATH = "../data/"  # Import from document_processor(?)
COMPUTER_SCIENCE_METADATA_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus_metadata.dat"
COMPUTER_SCIENCE_CORPUS_PATH = DATA_DIRECTORY_PATH + "computer_science_corpus.dat"

class DocumentRetriever(object):

	def __init__(self):
		pass

	def getDocuments(self, query, number_of_results):
		documents = self.retrieveDocuments(query, number_of_results)
		metadata = self.extractMetadata(documents)
		
		return documents, metadata
		
	def retrieveDocuments(self, query, number_of_results):
		documents = arxiv.query(query,
					prune = True, 
			              	start = 0, 
			              	max_results = number_of_results)

		return documents

	def extractMetadata(self, documents):
		metadata = { }

		for document in documents:
			document_id = document["id"]

			metadata[document_id] = { }
			metadata[document_id]["id"] = document_id
			metadata[document_id]["title"] = document["title"]
			metadata[document_id]["summary"] = document["summary_detail"]["value"]
			metadata[document_id]["category"] = document["arxiv_primary_category"]["term"]

		return metadata

	def getDocumentPDF(self, document):
		document_pdf_file_path = arxiv.download(document, DATA_DIRECTORY_PATH)

		return document_pdf_file_path

	def processDocuments(self, documents, metadata):
		metadata_file = open(COMPUTER_SCIENCE_METADATA_PATH, "rb")
		
		corpus_metadata = { }

		if (len(metadata_file.read()) != 0):
			metadata_file.seek(0)  # Reset the file pointer.
			corpus_metadata = pickle.load(metadata_file)
			metadata_file.close()
		
		number_of_documents = len(documents)
		number_of_successes = 0
		number_of_failures = 0

		for document in documents:
			document_id = document["id"]

			if document_id not in corpus_metadata:	
				# Download the document
				document_pdf_file_path = arxiv.download(document, DATA_DIRECTORY_PATH)
				document_text_file_path = ""  # Do we need this?
				print "\t Downloaded document ", (number_of_successes + number_of_failures), "/", number_of_documents,


				try:
					# Send the document for processingsublinme
					document_processor = DocumentProcessor(document_pdf_file_path)
					# Convert the document to text and delete the PDF
					#document_text_file_path = self.convertDocumentToText(document_pdf_file_path)
					#print("Converted document to text")

				except Exception as exception:
					#print("Could not decode the document correctly")
					os.remove(document_pdf_file_path)
					number_of_failures = number_of_failures + 1
					print " - failed (", str(type(exception).__name__), ")"  
				else:
					# Add this document to the corpus metadata
					corpus_metadata[document_id] = metadata[document_id]
				
					# Send it for processing
					

					#document_processor.processText()
					#document_processor.writeToCorpus()
					#print("Processed document")
					
					# Remove both the .pdf and .txt. version of the file from disk
					#os.remove(document_pdf_file_path)
					#os.remove(document_text_file_path)

					number_of_successes = number_of_successes + 1
					print " - succeeded"
		
		
		print ""
		print ""
		print "Total documents: ", number_of_documents
		print "Number of successes: ", number_of_successes
		print "Number of failures: ", number_of_failures	
					
		# Write the updated corpus out to the file
		metadata_file = open(COMPUTER_SCIENCE_METADATA_PATH, "wb")
		pickle.dump(corpus_metadata, metadata_file)
		metadata_file.close()

def main():
	retriever = DocumentRetriever()
	
	documents, metadata = retriever.getDocuments("programming+languages", 374)
	
	print(len(documents))

	for document in metadata:
		print document

	#retriever.processDocuments(documents, metadata)

	#documents, metadata = retriever.getDocuments("Programming Languages", 100)
	#retriever.processDocuments(documents, metadata)

	#documents, metadata = retriever.getDocuments("Graphics", 100)
	#retriever.processDocuments(documents, metadata)
	
	#documents, metadata = retriever.getDocuments("Operating Systems", 100)
	#retriever.processDocuments(documents, metadata)

	#documents, metadata = retriever.getDocuments("Computer Architecture", 100)
	#retriever.processDocuments(documents, metadata)
		
	#corpus_file = open(COMPUTER_SCIENCE_CORPUS_PATH, "rb")
	#corpus = pickle.load(corpus_file)
	#corpus_file.close()

	#for word in corpus:
	#	print word, ":", corpus[word]

	#print("\n")
	#print("the: ", corpus["the"])
	print ("Completed program")

if __name__ == "__main__":
	main()
