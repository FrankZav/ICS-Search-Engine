#Francisco Zavalza 62706684
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import word_tokenize
import math


validdocs = 0
index = defaultdict(list)



def checkFiles():
    global validdocs
    false = 0
    for file in range(37497):
        folder = str(file/500)
        filenum = str(file%500)
        path = 'WEBPAGES_RAW' +'\\' + folder + '\\' + filenum
        f = open(path, 'r')
        fd = f.read()
        f.close()
        if (bool(BeautifulSoup(fd,"html.parser").find())):
            validdocs += 1
            soup = BeautifulSoup(fd, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]'])]
            visible_text = soup.getText()

            print path
            visible_text = re.sub(r'[^a-zA-Z]', " ", visible_text)
            terms = word_tokenize(visible_text)
            terms = map(lambda x: x.lower(),terms)
            id = folder + '/' + filenum
            set_terms = set(terms)
            for term in set_terms:
                term_count = terms.count(term)
                posting = [id, float(term_count)/float(len(terms))]
                index[term].append(posting)
        else:
            print(path + " IS INVALID")
            false += 1

    print ("Total unprocessed {}, Total processed {}".format(false, validdocs))


def saveToDatabase():
    global validdocs
    for term, postings in index.iteritems():
        df = math.log(float(validdocs)/float(len(postings)))
        for termcount in postings:
            tf_idf = float(termcount[1]) * float(df)
            termcount.append(tf_idf)
        db_terms2.insert({
                        'term': term,
                        'postings': postings})


def main():
    checkFiles()
    saveToDatabase()


if __name__ == "__main__":
    client = MongoClient()
    db_terms2 = client['SearchEngine']['terms']
    main()
