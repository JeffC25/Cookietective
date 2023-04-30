import re
from difflib import SequenceMatcher

def urlComp(url1, url2):
    # convert strings to lowercase to make comparison case-insensitive
    url1 = url1.lower()
    url2 = url2.lower()

    # splits
    regex = re.compile(r'\b[a-zA-Z]+\b')
    wordsUrl1 = regex.findall(url1)
    wordsUrl2 = regex.findall(url2)

    # find all that match
    matches = []
    for word in wordsUrl1:
        if word in wordsUrl2:
            matches.append(word)

    return matches

def longestStr(url1, url2): #returns the
    # remove anything after a "/" in the url
    index = url1.find("/")
    if index != -1:
        url1 = url1[:index]

    index = url2.find("/")
    if index != -1:
        url2 = url2[:index]

    # remove everything except alpha-numeric characters from the urls
    url1 = re.sub("[;,/?:@&=+$-_.!~*'()#]","",url1)
    url2 = re.sub("[;,/?:@&=+$-_.!~*'()#]","",url2)

    # find the longest series of characters
    match = SequenceMatcher(None, url1, url2).find_longest_match()
    matchString = url1[match.a:match.a + match.size]
    return matchString

def mostMatching(url1, url2): # returns number of matching domains, array of what they are
    # remove anything after a "/" in the url
    index = url1.find("/")
    if index != -1:
        url1 = url1[:index]

    index = url2.find("/")
    if index != -1:
        url2 = url2[:index]

    # split the arrays based on the . character
    url1Array = url1.split(".")
    url2Array = url2.split(".")

    # reverse the arrays so highest level domains are first
    url1Array.reverse()
    url2Array.reverse()
    print(url1Array)
    print(url2Array)

    # compare the arrays in a loop until they are not the same or the array is done.
    matches = []

    for i in range(len(url1Array)-1):
        if url1Array[i] != url2Array[i]:
            break
        if url1Array[i] == url2Array[i]:
            matchCount = matchCount + 1
            matches.append(url1Array[i])

    return matchCount, matches

''' Test Code
str1 = "www.hilton.hotels.com/search"
str2 = "www.laquinta.hotels.com"

common_part = urlComp(str1, str2)
for element in common_part:
    print(element)

longestCharacters = longestStr(str1, str2)
print(longestCharacters)

domainMatches = mostMatching(str1, str2)
print(domainMatches)
'''