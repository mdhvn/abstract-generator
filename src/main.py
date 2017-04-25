import arxiv
import textract

results = arxiv.query("information retrieval", prune = True, start = 0, max_results = 20)

counter = 0
words = 0

for result in results:
        #arxiv.mod_query_result(result)
        #arxiv.prune_query_result(result)
        print("\n")
        filename = arxiv.download(result)
        print("Downloaded paper")
        print("Filename: ", filename)

        try:
                text = textract.process(filename)
                text_filename = str(counter) + ".txt"
                print("Extracted text")
                words = words + len(text.split())

                output = open(text_filename, "w")
                output.write(text)
                output.close()

                counter = counter + 1
        except:
                print("Could not extract text")


        print("\n\n\n\n")
        print("Words: ", str(words))
