# indian-name-classifier

Usage: `find-indian-names.py <URL or filename>`
- Eg: `find-indian-names.py "http://www.indiatimes.com/"`

Input: URL/file with data (eg list of names, raw HTML page with names scattered throughout)

Output: list of names classified as Indian ("Indianness" score, gender score)

Limitations:
- Classifies only based on accompanying corpora of Indian first/last names
- Only works for 2-word names (first/last name)

Module dependencies
- Beautiful Soup 4 (included)
- Inflection (included)
