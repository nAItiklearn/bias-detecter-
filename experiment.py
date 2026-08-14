# import regex as re
# text = '''Learning #Python and #MachineLearning
# while building #BiasDetector.
# #coding #100DaysOfCode'''

# has=re.search(r'#\w+', text)
# print(has.span())
# print(has)

# text=''' my phone pass is 123'''
# result=re.sub(r'\d+', 'XXX', text)
# print(result)


# text="""
# This SHOCKING decision is absolutely TERRIBLE!
# It will DESTROY everything. People ALWAYS suffer.
# """
# # cap=re.findall(r'\b\w+[A-Z]+\w+[A-Z]+\w+[A-Z]+\w+[A-Z]+\b', text)
# # capitalized = re.findall(r'[A-Z]{6,8}', text)
# # print(capitalized)

# # print(cap)
# # ly=re.findall(r'b\w*ly\w*\b',text, re.IGNORECASE)
              
# # print(ly)
# # su=re.sub(r'!','.', text)
# # print(su) 

# ###DATA CLEANING###

# #tokenization
# import nltk 

# # nltk.download("punkt")
# from nltk.tokenize import word_tokenize, sent_tokenize
# texts=["im writing this this because free will",
#       "the point of writing _this_ this is to learn #datacleaning #simpe LMAO" ,
#       "YOU are a a a dirty dirty #bitch!!"
#       ]


# ttext = [word_tokenize(text) for text in texts]
# # print("tokenized docs:", ttext)

# #sentence
# # stext = [sent_tokenize(text) for text in texts]
# # print("tokenized sentnce:",stext)


# ##punctuation removal##

# import re 
# import string
# regex=re.compile("[%s]"% re.escape(string.punctuation))
# cleaned_raw=[]

# for review in ttext:
#     new_review=[]
#     for token in review:
#         new_token=regex.sub("", token)
#         if new_token!="":
#             new_review.append(new_token)
            
    
#     cleaned_raw.append(new_review)

# # print(cleaned_raw)
# import nltk
# #remove stopwords
# from nltk.corpus import stopwords
# from collections import Counter
# # nltk.download("stopwords")
# stopwordss=[]
# for doc in cleaned_raw:
#     new_term=[]
#     for word in doc:
#         if not word.lower() in stopwords.words('english'):
#             new_term.append(word)
#     stopwordss.append(new_term)
# frequency = Counter(new_term)
# # print(stopwordss)
# # print(frequency)
# print(frequency["dirty"])
            
##learning sentiment analysis with vader

# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia
# sa= sia()
# sp=sa.polarity_scores("im the worst")
#{'neg': 0.672, 'neu': 0.328, 'pos': 0.0, 'compound': -0.629} 
#compund here means a undimensional single value that gives an overview of the overall sentiment of the text , range[1,1]
import pandas as pd
from nrclex import NRCLex
df=pd.read_excel("", sheet_name="sheet1")

def get_nrc_sentiment(text):
    emotion=NRCLex(str(text))
    return emotion.raw_emotion_scores

df["nrc_sentiment"]=df["processed_comments"].astype(str).apply(get_nrc_sentiment)

print(df)[["processed_comments", "nrc_sentiments"]]
