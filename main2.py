import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import streamlit as st

nltk.download('stopwords')
nltk.download('punkt')


st.title("SEO Analyzer")
url = st.text_input("Enter URL")

def seo_analysis(url):
    good = []
    bad = []

    if not url:
        st.error("Error: Please enter a valid URL")
        return

    if not url.startswith(('http://', 'https://')):
        st.error("Error: URL must start with http:// or https://")
        return

    response = requests.get(url)

    if response.status_code != 200:
        st.error("Error: Unable to access the website")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('title')
    description = soup.find('meta', attrs={'name':'description'})

    # checking if the title and description exist
    if title:
        good.append("Title Exists! Great!")
    else:
        bad.append("Title does not exist! Add a Title!")

    if description and 'content' in description.attrs:
        good.append("Description Exists! Great!")
    else:
        bad.append("Description does not exist! Add a description!")

    # Grabbing the headings
    hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    h_tags = []
    for h in soup.find_all(hs):
        good.append(f"{h.name} --> {h.text.strip()}")
        h_tags.append(h.name)

    if 'h1' not in h_tags:
        bad.append("h1 not found")

    # Extract the images without alt
    for i in soup.find_all('img', alt=''):
        bad.append(f"No Alt {i}")

    # Extract keywords and grab the text from html body
    bod = soup.find('body').text

    # Extract all the words in a body, lowercase them and store in a list
    words = [i.lower() for i in word_tokenize(bod)]

    # Extract the bigrams from the tokens
    bigrams = ngrams(words, 2)
    freq_bigrams = nltk.FreqDist(bigrams)
    bi_grams_freq = freq_bigrams.most_common(10)

    # grab a list of English stopwords
    sw = nltk.corpus.stopwords.words('english')
    new_words = []

    # Put the tokens that are not stopwords and are actual words in a list
    for i in words:
        if i not in sw and i.isalpha():
            new_words.append(i)

    # Extract the frequency of the words and get the 10 most common ones
    freq = nltk.FreqDist(new_words)
    keywords = freq.most_common(10)

    # Print the results
    tab1, tab2, tab3, tab4 = st.tabs(['Keywords', 'BiGrams', 'Good', 'Bad'])
    with tab1:
        for i in keywords:
            st.text(i)
    with tab2:
        for i in bi_grams_freq:
            st.text(i)
    with tab3:
        for i in good:
            st.success(i)
    with tab4:
        for i in bad:
            st.text(i)
    print("Keywords: ", keywords)
    print("The Good: ", good)
    print("The Bad: ", bad)

# Call the function to see the results
if url:
    seo_analysis(url)
