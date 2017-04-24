def getDocumentContents(filepath):
	document = open(filepath, "r")
	contents = document.read()
	document.close()
	return contents

def getAbstract(document):
	document_lowercase = document.lower()
	start_of_abstract = document_lowercase.index("abstract")
	end_of_abstract = document_lowercase.index("introduction")
	abstract = document[start_of_abstract : end_of_abstract]

	return abstract

def main():
	contents = getDocumentContents("../data/test/computational_theory.txt")
	print(getAbstract(contents))
main()
