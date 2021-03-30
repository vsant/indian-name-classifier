#!/usr/bin/env python3
# 
# Indian Name Classifier
# Vivek Sant
# 2015-06-02
# 

from bs4 import BeautifulSoup
from inflection import singularize
import urllib.request, urllib.error, urllib.parse
import re
import os

# Import corpora of Indian last names, first names (male/female/unisex),
# and common english words that are not Indian names
script_dir         = os.path.dirname(__file__)
names_last         = [l.strip().title() for l in open(os.path.join(script_dir, "names.last.txt"))]
names_first_male   = [l.strip().title() for l in open(os.path.join(script_dir, "names.first.male.txt"))]
names_first_female = [l.strip().title() for l in open(os.path.join(script_dir, "names.first.female.txt"))]
names_first_unisex = [l.strip().title() for l in open(os.path.join(script_dir, "names.first.unisex.txt"))]
en_words           = [l.strip().title() for l in open(os.path.join(script_dir, "en_words.txt"))]

# From an array of consecutive words, create unique potential two-word names
def create_bigrams(input_list):
  bigrams = []
  for i in range(len(input_list)-1):
    bigrams.append((input_list[i].title(), input_list[i+1].title()))
  return list(set(bigrams))

def main(args):
    # Usage
    if len(args) != 2:
      print("%s <URL or filename>" % args[0])
      return -1

    # Input HTML file or URL
    if os.path.isfile(args[1]):
      html = open(args[1]).read()
    else:
      # Provide a User-Agent
      req = urllib.request.Request(args[1], headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0' })
      html = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(html, 'html.parser')

    # Remove Javascript/CSS
    for s in soup(["script", "style"]):
      s.extract()

    # Remove HTML
    text = " ".join(soup.strings)

    # Remove all non-alpha/space, convert all whitespace to single space
    text = text.replace("\n", " ")
    regex = re.compile('[^a-zA-Z ]')
    text = re.sub('\s+', ' ', regex.sub('', text)).strip()

    # Remove 1-letter words (now rather than after creating bigrams accounts
    # for middle initials)
    text = [i for i in text.split() if len(i) > 1]
    text = ' '.join(text)

    # Create bigrams (potential 2-word names) from text
    bigrams = create_bigrams(text.split())

    # Iterate over bigrams
    # If fn/ln within corpora, add to results with score for Indianness/gender
    # Decrease Indianness score if fn/ln is an ordinary English word
    indian_names = []
    for name in bigrams:
      ln, fn_m, fn_f, fn_u = 0, 0, 0, 0
      en_word, indianness, gender = 0, 0, 0
      if name[1] in names_last:
        ln = 1
      if name[0] in names_first_male:
        fn_m = 1
      if name[0] in names_first_female:
        fn_f = 1
      if name[0] in names_first_unisex:
        fn_u = 1
      
      indianness = ln + fn_m + fn_f + fn_u
      gender = fn_m - fn_f

      if indianness:
        if name[0] in en_words:
          en_word += 1
        if name[1] in en_words:
          en_word += 1

        # Check depluralized word
        singular_fn, singular_ln = singularize(name[0]), singularize(name[1])
        if singular_fn != name[0] and singular_fn in en_words:
          en_word += 1
        if singular_ln != name[1] and singular_ln in en_words:
          en_word += 1

        indianness -= en_word

      if indianness > 0:
        indian_names.append(("%s %s" % name, indianness, gender))

    # Sort first by -indianness, +gender, +alpha
    indian_names = sorted(indian_names, key=lambda x: (-x[1], x[2], x[0]))

    # Display the classified Indian names, with indicators for Indianness
    for i in indian_names:
      if i[1] > 1:
      	print("+", end=' ')
      else:
      	print("-", end=' ')
      print("%s (%d, %d)" % i)

if __name__ == "__main__":
  import sys 
  sys.exit(main(sys.argv))
