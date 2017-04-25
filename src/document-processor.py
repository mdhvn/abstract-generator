import codecs
import nltk

class Document():

    def __init__(self, filename):
        self.filename = filename

    def readDocument(self):
        document_file = codecs.open(self.filename, "r", "utf-8")
        
        self.contents = document_file.read()
        print(self.contents)
        
        document_file.close()

    def process(self):
        self.readDocument()
        self.frequency_distribution = nltk.FreqDist(self.contents)

    def getDocumentContents(self):
        return self.contents

    def getFrequencyDistribution(self):
        return self.frequency_distribution

    
def main():
    document = Document("data/handout_naivebayes.txt")
    document.process()

    frequency_distribution = document.getFrequencyDistribution()

    for word, frequency in frequency_distribution.most_common(50):
        print(u'{};{}'.format(word, frequency))
    
main()
