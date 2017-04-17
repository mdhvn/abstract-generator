import arxiv
import textract

class DocumentRetriever(object):

	def __init__(self):
		print("Hello world!")

	def retrieveDocuments(self, query, number_of_results):
		results = arxiv.query(query, 
			                  prune = True, 
			                  start = 0, 
			                  max_results = number_of_results)

		for result in results:
			for key in result:
				print key, ":", result[key]

		# Keys (data) to keep:
		#	- Link(s) [this is also just the 'id' or 'arxiv_url']
		#	- summary_detail(?)
		#   - Title
		#   - Category (arxiv_primary_category): Ensure that each paper
		#     is (categorized as) a Computer Science paper. (cs.XX) for
		#     all Computer Science sub-fields, where XX is the two-letter
		#     code for a sub-field.



def main():
	retriever = DocumentRetriever()
	retriever.retrieveDocuments("cryptography", 1)

if __name__ == "__main__":
	main()