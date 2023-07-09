# Sentiment Analysis
Methodology

Data collection(web scraping) ---> Data Pre-processing(removing stop words,punctuations..) ---> Sentiment Analysis(finding positive score,negative score, polarity index, fog index..)

## Description

In this project I have used web scarping for collecting text data from multiple websites of same domain and performed sentiment analysis. I completed
this project as a case study given from a company Black coffer. 

### Following Paramaters have been used to analyse the sentiments of each text article. 
I converted the text into a list of tokens using the nltk tokenize module and use these tokens to calculate the 4 variables described below:
#### Scores
* Positive Score: This score is calculated by assigning the value of +1 for each word if found in the Positive Dictionary and then adding up all the values.
* Negative Score: This score is calculated by assigning the value of -1 for each word if found in the Negative Dictionary and then adding up all the values. We multiply the score with -1 so that the score is a positive number.
* Polarity Score: This is the score that determines if a given text is positive or negative in nature. It is calculated by using the formula: 
  Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
  Range is from -1 to +1
* Subjectivity Score: This is the score that determines if a given text is objective or subjective. It is calculated by using the formula: 
  Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
  Range is from 0 to +1

#### Analysis of Readability
Analysis of Readability is calculated using the Gunning Fox index formula described below.
Average Sentence Length = the number of words / the number of sentences
Percentage of Complex words = the number of complex words / the number of words 
Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

#### Average Number of Words Per Sentence
The formula for calculating is:
Average Number of Words Per Sentence = the total number of words / the total number of sentences

#### Complex Word Count
Complex words are words in the text that contain more than two syllables.

#### Word Count
We count the total cleaned words present in the text by 
1.	removing the stop words (using stopwords class of nltk package).
2.	removing any punctuations like ? ! , . from the word before counting.

#### Syllable Count Per Word
We count the number of Syllables in each word of the text by counting the vowels present in each word. We also handle some exceptions like words ending with "es","ed" by not counting them as a syllable.

#### Personal Pronouns
To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken so that the country name US is not included in the list.

#### Average Word Length
Average Word Length is calculated by the formula:
Sum of the total number of characters in each word/Total number of words



## Output
![image](https://user-images.githubusercontent.com/81084807/208061935-1057b3f5-f321-48fa-a7a2-0ed762511f3b.png)

### Live link
https://colab.research.google.com/drive/1inZXxZg6uWeTh8_1IUmp5ipgeCEM5il6?usp=sharing



