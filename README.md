# Using NLP to Analyze Rap/Hip-Hop Lyrics from Nas
#### The notebook for everything explained below can be found [here](Nas_Lyrics_EDA.ipynb). 
After taking the CodeCademy course on Natural Language Processing I was inspired by their [Taylor Swift Analysis](https://www.codecademy.com/article/the-machine-learning-process-taylor-swift) to perform a similar type of analysis on the rap artist Nas. Nas is widely regarded as one of the best rappers and lyricsts so choosing him for this was study easy. The intent of this project was to use NLP to find common reoccuring words and groupings of words that create topics in songs and to see the frequency in which Nas used these topics throughout his career on different albums.
![alt text](https://github.com/Raatid-Dilly/Nas_Lyrics_NLP_Analysis/blob/main/images/nas_image.png?raw=true)

# Getting Albums and Lyrics
To begin the first step was to get the list of Nas' albums to later save the lyrics for songs from each album respectively. To do this Beatiful Soup and the Requests libraries were used to scrape the album names from the web. Next the lyrics for each album are saved using the LyricsGenius module which can be found [here](https://lyricsgenius.readthedocs.io/en/master/). Note to use this module an access token from [genius.com](https://docs.genius.com/#/getting-started-h1) is required. The downloaded album lyrics are all stored as .json files in the [All_Lyrics](https://github.com/Raatid-Dilly/Nas_Lyrics_NLP_Analysis/tree/main/All_Albums) folder. Each .json file has 12 keys, but for the purposes of this project the only ones of interest are 'name', 'release_date_components', and 'tracks'. The values for the 'tracks' key is a list of dictionaries with information about each track. [This is the script](https://github.com/Raatid-Dilly/Nas_Lyrics_NLP_Analysis/blob/main/music.py) to download the lyrics for each album and create a dataframe for analysis.

# Exploratory Data Analysis (EDA)
1. # Data Cleaning
To perform any type of natural language processing often times the first step is to clean the text and prepare it for analysis. Rap/Hip-Hop could be challenging due to the amount of slang words that are used.  being While there is more that can be done like stemming/lemmatizing text, for T removing unnecessary characters and formatting, tokenizing the text (), removing stop words etc.  

A snippet of the lyrics from the .json file is shown below:

```"lyrics": "Leaders Lyrics[Chorus: Stephen Marley]\nThis one's for all the leaders\nLeader\nLets all change the world\nChange\nThe world\nThis one's for all the leaders\nLeader\nLets all change the\nWorld\nChange the world\n[Verse 1: Nas]\nYeah!\nGot...\nChange the world\nThis one's for all the leaders\nLeader\nLets all change the world\nChange the world\nChange the world, change the world\nChange the world\nChange the world, change the world\nYou change the world5Embed"```

Function to clean lyrics:
```
def clean_lyrics_format(lyrics):
    """
    Cleans the text of the lyrics column
    """
    
    remove_exception = "'"
    lyrics = re.sub('^[^\n]*\n', '', lyrics)  # Removes the first line up until the new line char that is not lyric
    lyrics = re.sub('[0-9]{1,}Embed', '', lyrics) # Removes the last line few words that is not part of lyric
    lyrics = re.sub('\[.*?\]', '', lyrics) #Removes all character between brackets
    lyrics = re.sub(r"[^\w"+remove_exception+"]", ' ', lyrics) #removes all non-alpha characters except (')
    lyrics = re.sub(' +', ' ', lyrics).lower().strip() #removes whitespaces and lowercases text
    
    return str(lyrics)
```
2. # Text Analysis
  - **Word Count** - After the text is processed, next is performing analysis to find the albums with the highest word count and Nas' most used words. It was found that the albums of God's Son, Streets Disciples, and I Am contained the most words with well over 12,000 words. His most used word was the 'n-word'. These are visualized along with a wordcloud representation of words he frequently uses.
  
  * **Term Frequency Inverse Document Frequency (TFIDF)** - TFIDF is a numerical statistic used to indicate how important each word is to a document in a collection of documents. It consists of two components, term frequency and the inverse document frequency
    - Term frequency is the measure of how often a word appears in a document
    - Inverse Document frequency is the measure of how often a word appears across all corpus documents. More frequently appearing words are penalized as they give less insight into document meaning
    - TFIDF is calculated as the term frequency multiplied by the inverse document frequency
    
  * **Non-Negative Matrix Factorization (NMF)** - NMF is an algorithm that can be used to get a grouping of co-occuring words. Then using these list of words and our knowledge of Nas' music we can create topics that the words represent.
    - The NMF model n_components parameter will be set to 6 to generate 6 different topics
    - For each topic list argsort will be used to get the index positions of the 20 words with the highest scores to then use 'get_features_names_out()'  to narrow the topic list down to the 20 highest scoring words per topic.
    - From these generated topic list of words, I used my knowledge of Nas to make a guess as to the general subject matter or 'topic' of each list. The 6 topics I decided were:
      * Life/Normal
      * Empowerment
      * Violence
      * NY/Best Rapper
      * Political/Change
      * Sentimental/Family

* **Word2Vec and t-Distributed Stochastic Neighbor Embedding (TSNE)** - Word2vec is a statistical learning algorithm that develops word embeddings from a corpus of text. We will be able to see how similar certain words are to each other when used by Nas. It will create a 100 dimensional vector space where similar words will be mapped next to each other. The similarity of each word is calculated by the cosine similarity between the vectors. This is used along with TSNE which is a dimensionality reduction technique designed for visualizing higher dimensional data in a 2-D space to reduce the greater dimensional vector from the word2vec to a simple graph for visualization. TSNE created a map with the following word pairings:
  * new and york
  * one and love
  * rise and ghetto
  * world and mine
  * peace and everybody

Using knowledge of Nas' music we know that there are several songs with these words used together like 'One Love', 'The World is Yours', 'N.Y. State of Mind' and 'Every Ghetto'

* **Sentiment Analysis** - Finally VADER from the NLTK library is used to perform a sentiment Analysis of Nas' lyrics. Analyzing rap lyrics will be difficult as there are many slang words and often times a song may contain negative words but contain an overall positive message. Additionally VADER is trained on social media texts so the results are not expected to be ideal. VADER's polarity_scores() function returns a dictionary with values of negative, positive, neutral and compound scores respectively. We will use the compound score as it normalizes all the other scores and is the overall sentiment. The final results of this analysis showed that analyzing the sentiment of rap lyrics was not ideal and not recommended. Many of Nas' positive songs were incorrectly classified as negative.

The notebook of the EDA is [here](https://github.com/Raatid-Dilly/Nas_Lyrics_NLP_Analysis/blob/main/Nas_Lyrics_EDA.ipynb)
   
