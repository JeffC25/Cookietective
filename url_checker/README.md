# Info
The purpose of the URL scanner is come up with a confidence score if URLS are related. This is accomplished by scanning through the URLS and determining if there are strings in common and how many strings there are.

## Function Explanation
#### urlComp(url1, url2)
This function returns an array that includes all common words in the domain, separated by any non-alphanumeric character.
```
str1 = "www.hilton.hotels.com/search"
str2 = "www.laquinta.hotels.com"

common = urlComp(str1, str2)
print(common)

{'www', 'hotels', 'com'}
```
#### longestStr(url1, url2)
This function returns a string of the longest set of alpha-numeric characters that are the same, ignoring any non-alphanumeric characters.
```
str1 = "www.hilton-hotels.com/search"
str2 = "hiltonhotels.com"

longestCharacters = longestStr(str1, str2)
print(longestCharacters)

hiltonhotelscom
```

#### mostMatching(url1, url2)
This function analyzes a URLs TLD, domain, and subdomain(s) to see how many match. It will then return the number of matches it finds, starting at the bottom level and ending when there is a mismatch. It returns an array containing the number of matches found and the actual strings that match.
```
str1 = "www.hilton.hotels.com/search"
str2 = "www.laquinta.hotels.com"

domainMatches = mostMatching(str1, str2)
print(domainMatches)

(2, ['com', 'hotels'])
```

### Scanner update
The scanner that is currently implemented is great for checking if the domains have a common top-level domain, but is not effective for finding if different top-level domains belong to the same owner. I would like to update the scanner to be more robust, for example:
```
*Update to scan strings for longest sequence of letters in common
    "www.hilton.com" and "www.hilton-hotels.com" would catch 'hilton' as being the longest sequence of letters in common
*Update to find multiple of these "long letter sequences"
    "www.hotels.hilton.com" and "www.hiltonhotels.com" would catch 'hilton' and 'hotel' as both being mentioned in the URL.
```

## Implementation
Domains that belong to the same website will share the same top level domain and domain name. The mostMatching() function can be used to see if two URLs have at least 2 matches, then they share the same root domain and are very likely owned by the same entity.\
If domains do not have the same root domain, they still may be related and owned by the same person. We are using additional URL scans to determine if domains share a similar enough name to be considered related. 