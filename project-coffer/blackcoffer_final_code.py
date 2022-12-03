# -*- coding: utf-8 -*-
"""BlackCoffer-Final Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PW4nwUgEqd4au8Z2FGIf8Nq47sLhrFbq
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests as r
import pandas as pd
import numpy as np
import re
import requests

def read_stop_words():
  stop_files_list = ['StopWords_Auditor.txt','StopWords_Currencies.txt','StopWords_DatesandNumbers.txt','StopWords_Generic.txt','StopWords_GenericLong.txt','StopWords_Geographic.txt','StopWords_Names.txt']
  stop_words = []

  for i in stop_files_list:
    with open(i, encoding = "ISO-8859-1") as file:
      for line in file:
        if '|' in line:
          line = line.split('|')
          stop_words.append([x.strip() for x in line])
        else:
          stop_words.append(line.strip())
  
  #Checking for lists in the list of stop_words created above
  word_lists = []
  for i,value in enumerate(stop_words):
    if isinstance(value, list):
      word_list = stop_words.pop(i)
      #Assumption - Removing all the words with more than 30 characters
      word_lists.append([x for x in word_list if len(x) < 30])
  word_lists =  [item for sublist in word_lists for item in sublist]
  final_stop_words = stop_words + word_lists
  return final_stop_words

def read_positive_words():
  with open('positive-words.txt', encoding = "ISO-8859-1") as file:
    positive_words = [line.rstrip() for line in file]
  return positive_words

def read_negative_words():
  with open('negative-words.txt', encoding = "ISO-8859-1") as file:
    negative_words = [line.rstrip() for line in file]
  return negative_words

def list_of_words(url):
  req = Request(url)
  response = requests.get(url, headers={"User-Agent": "XY"})
  if response.status_code == 200:
    req.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    html = urlopen(req).read()
      #rawpage
      #html=urlopen(url)

    soup=BeautifulSoup(html, "html.parser")
      #type(soup)
    title = soup.find('title')
    all_links=soup.findAll('div',{'class':'td-post-content'})
    str_cells=str(all_links)
      #print(str_cells)
    clear_text=BeautifulSoup(str_cells,'html.parser').get_text()
    clear_text = clear_text[1:-1] #removing the appending and leading brackets
    list_of_words = clear_text.split()
    new_list = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in list_of_words]
    return title.string, clear_text, new_list
  else:
    return 'bad_response', 'bad_response', []

def words_wo_stop_words(new_list):
  final_stop_words = read_stop_words()
  words_without_stop=[]
  for i in new_list:
    if i not in final_stop_words:
      words_without_stop.append(i)
  return words_without_stop

words = words_wo_stop_words(list_of_words('https://insights.blackcoffer.com/ai-in-healthcare-to-improve-patient-outcomes/')[1])
len(words)

def pos_score(words):
  pos_count = 0
  pos_words = read_positive_words()
  for i in words:
    if i in pos_words:
      pos_count +=1 
  return pos_count

def neg_score(words):
  neg_count = 0
  neg_words = read_negative_words()
  for i in words:
    if i in neg_words:
      neg_count +=1 
  return neg_count

def polarity_Score(Positive_score, Negative_score):
  return (Positive_score-Negative_score)/((Positive_score+Negative_score)+0.000001)

def subjectivity_score(Positive_score, Negative_score, words):
  return (Positive_score+Negative_score)/(len(words)+0.000001)

def sentence_count(clear_text):
  import nltk
  nltk.download('punkt')
  from nltk.tokenize import sent_tokenize
  number_of_sentences = sent_tokenize(clear_text)
  return len(number_of_sentences)

def avg_sentence_len(words, number_of_sentences):
  return len(words)/number_of_sentences

def complex_word_count(words):
  w_sb_dict = {}
  complex_word_count = 0
  for word in words:
    count = 0
    if word.lower()[-2:] != 'es' or word.lower()[-2:] != 'ed':
      for char in word:
          if char.lower() in 'aeiou':
              count += 1
      #Checking count for each word - having vowels greater than 2
      if count > 2:
        complex_word_count +=1
      w_sb_dict[word] = count
  avg_syllable_per_word = sum(w_sb_dict.values()) / len(w_sb_dict)
  return avg_syllable_per_word, complex_word_count

def percentage_complex_words(complex_word_count, words):
  return complex_word_count/len(words)

def fog_index(avg_sent_len, percent_complex_words):
  return 0.4 * (avg_sent_len + percent_complex_words)

def avg_words_per_sentence(words, nSentences):
  return len(words)/nSentences

def personal_pronouns(words):
  pp = ['i', 'we', 'my', 'ours', 'us']
  count = 0
  for word in words:
    if word != 'US':
      if word.lower() in pp:
        count +=1
  return count

def avg_word_length(words):
  sum_char = 0.0
  for word in words:
    sum_char += len(word)
  return sum_char/len(words)

def main():
  data = pd.read_excel('Input.xlsx')

if __name__=="__main__":
  main()

def generate_scores_list(url):
  title, text, new_list = list_of_words(url)
  if title != 'bad_response':
    stop_words = read_stop_words()
    positive_words = read_positive_words()
    negative_words = read_negative_words()
    words_without_stop = words_wo_stop_words(new_list)
    positive_score = pos_score(words_without_stop)
    negative_score = neg_score(words_without_stop)
    polarity_score = polarity_Score(positive_score, negative_score)
    sub_score = subjectivity_score(positive_score, negative_score, words_without_stop)
    nSentences = sentence_count(text)
    avg_sent_len = avg_sentence_len(words_without_stop, nSentences)
    avg_syllable_per_word, comp_wc = complex_word_count(words_without_stop)
    p_cw = percentage_complex_words(comp_wc, words_without_stop)
    fg = fog_index(avg_sent_len, p_cw)
    avg_w_per_s = avg_words_per_sentence(new_list, nSentences)
    word_count = len(words_without_stop)
    pp = personal_pronouns(new_list)  #Using total words here as some pronouns are stop words like 'we'
    wl = avg_word_length(words_without_stop)
    scores_list = [positive_score, negative_score, polarity_score, sub_score, avg_sent_len, p_cw, fg, avg_w_per_s, comp_wc, word_count, avg_syllable_per_word, pp, wl]
  else: 
    scores_list = [0]*13
  return scores_list

if __name__ == "__main__":
  data = pd.read_excel('Input.xlsx')
  scores_list = []
  for url in data['URL']:
    scores_list.append(generate_scores_list(url))
  f_list = [['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']]
  combined_list = f_list + scores_list
  df = pd.DataFrame(scores_list, columns =['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'] )
  final_data_frame = pd.concat([data, df], axis=1)
  final_data_frame.to_csv("Output_final", sep='\t')
