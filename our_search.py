from pymongo import MongoClient
from collections import defaultdict
import json, math

def abbreviation(search):
    ''' return the abbreviation of a search query'''
    my_string = ""
    for i in search:
        my_string += i[0]
    return my_string

def match(bookkeeping,search_string, matches):
    """give more weight to urls with search string in its name"""
    exact = search_string[-1] + ".ics.uci.edu"
    counter = 0
    for book in bookkeeping:
        if bookkeeping[book] == exact or bookkeeping[book] == search_string:
            matches[book] = matches[book] * 100
        elif bookkeeping[book].find(search_string[-1]) != -1:
            matches[book] = matches[book] * (100.0/len(bookkeeping[book]))
    for n in sorted(matches, key= matches.get, reverse = True):
        for books in bookkeeping:
            if n == books:
                print (bookkeeping[books])
                if counter == 9:
                    return counter
                counter += 1
                break
    return counter

def main():
    ''' Access PyMongo and make queries using user input '''
    client = MongoClient()
    db_terms = client['SearchEngine']['terms']
    while(1):
        matches = defaultdict(int)
        names = raw_input("\nWhat's your search? ")
        print("searching...")
        full_search = names.lower().split(" ")
        if len(full_search) > 1:
            shortened = abbreviation(full_search)
            full_search.append(shortened)
        for name in full_search:
            for post in db_terms.find({"term": name}):
                for n in post['postings']:
                    matches[n[0]] += n[2]
        fd = open('WEBPAGES_RAW/bookkeeping.json', 'r')
        bookkeeping = json.load(fd)
        fd.close()
        match(bookkeeping, full_search, matches)
    return 0

if __name__ == "__main__":
    main()
