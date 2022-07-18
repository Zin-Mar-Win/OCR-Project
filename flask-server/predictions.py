#!/usr/bin/env python
# coding: utf-8
#model_ner = spacy.load('flask-server\model-best')

#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import cv2
import pytesseract
from glob import glob
import spacy
import re
import string
import warnings
warnings.filterwarnings('ignore')

### Load NER model
model_ner = spacy.load('flask-server\model-best')


def cleanText(txt):
    whitespace = string.whitespace
    punctuation = "!#%&\¢'()*+:;<=>?[\\]^`{|}~"
    tableWhitespace = str.maketrans('','',whitespace)
    tablePunctuation = str.maketrans('','',punctuation)
    text = str(txt)
    text = text.lower()
    removewhitespace = text.translate(tableWhitespace)
    removepunctuation = removewhitespace.translate(tablePunctuation)
    
    return str(removepunctuation)


# group the label
class groupgen():
    def __init__(self):
        self.id = 0
        self.text = ''
        
    def getgroup(self,text):
        if self.text == text:
            return self.id
        else:
            self.id +=1
            self.text = text
            return self.id

#Parser


def parser(text,label):
    if label == 'NAME':
        text = text.lower()
        text = re.sub(r'[^a-z ]','',text)
        text = text.title()
        
    elif label == 'DATE':
        text = text.lower()        
        str_InvoiceDate=re.findall('(?i)[invoice|date|date:]\s*?(\d{1,2}\/[A-Za-z]{3,10}\/\d{2,4}|[A-Za-z]{3,10}\s*\d{1,2}\s*[A-Za-z]{3,10}\s*\d{2,4}|\d{1,2}\s*[A-Za-z]{3,10}\s*\d{2,4}|\d{1,2}[-]\d{1,2}[-]\d{2,4}|\d{1,2}\/\d{1,2}\/\d{2,4}|\d{1,2}[.]\d{1,2}[.]\d{2,4}|[A-Za-z]{3,10}\s*\d{1,2}[,]\s*\d{2,4}|[A-Za-z]{3,10}\s*\d{2}[A-Za-z]{2}[,]\s*\d{2,4})',text)
        #print(str_InvoiceDate) 
        #print("....................")## [('alice', 'google.com'), ('bob', 'abc.com')]
        #print(len(str_InvoiceDate))
        #print("....................")
        text = text.lower()
        for x in str_InvoiceDate:
            #print(x)  ## username
            text = re.sub(r''+ x,'',text)    

        text =text.title()  
        #print("....................")
        #print(text)
        #print("....................")
        
        
    elif label == 'TOTAL':
        print(".........Total...........")
        text = text.lower()
        str_InvoiceTotal=re.findall('(?i)[invoice|Invoice|lnvoice|total|balance|grand|amount|quote|gross]\s*?[invoice|tota1|total|payable|due|balance|grand|amount|value|due(cad)|to pay|quote|gross]\s*?[value|due|amount|total|payable|quote|pay|invoice|to pay]\s([$|EUR|GBP]\s?\d{1,10}[,]?\d{1,3}[.]\d{0,2}|[$|EUR|GBP]\s?\d{1,10}[,]?\d{1,3}|\d{1,10}[,]?\d{1,3}[.]\d{0,2})',text)
        #print(str_InvoiceTotal) 
        #print("....................")## [('alice', 'google.com'), ('bob', 'abc.com')]
        #print(len(str_InvoiceTotal))
        #print("....................")
        maximum = 0
        if len(str_InvoiceTotal)>0:
                    maximum = str_InvoiceTotal[0]

                    for i in str_InvoiceTotal:

                        if i > maximum:

                            maximum = i
                        #         i=str(i)[:-1]+']'
                        #         amount = i
                    #print('arr ', str_InvoiceTotal)

        #print(maximum)
        text = text.lower()
        #text = re.sub(r''+ str(maximum),'',text)   
        #text = re.sub(str(maximum),'',text)    
        text = text.title()
        #print(text)
        #print("....................")
        
        
    elif label == 'NUMBER':
        text = text.lower()
        text = re.sub(r'[^[0-9]+$]','',text)
        text = text.title()
        
    
        
    return text
        
    
        
    

grp_gen = groupgen()

def getPredictions(image):
    # extract data using Pytesseract 
    tessData = pytesseract.image_to_data(image)
    print("img to string ", pytesseract.image_to_data(image))
    print("tessData111 ")
    print(tessData)
    print("finished ..... ")
    # convert into dataframe
    tessList = list(map(lambda x:x.split('\t'), tessData.split('\n')))
    df = pd.DataFrame(tessList[1:],columns=tessList[0])
    df.dropna(inplace=True) # drop missing values
    df['text'] = df['text'].apply(cleanText)

    # convet data into content
    df_clean = df.query('text != "" ')
    content = " ".join([w for w in df_clean['text']])
    print("Content ......")
    print(content)
    print("finished ..... ")
    # get prediction from NER model
    doc = model_ner(content)

    #converting data to json
    docjson = doc.to_json()
    print("docjson ent......")
    print(len(docjson['ents']))
    print("docjson ent..... ")
    entities = dict(NAME=[],DATE=[],NUMBER=[],TOTAL=[])
    img_bb = image.copy()
    if len(docjson['ents']) > 0 :
        doc_text = docjson['text']
        
        #creating tokens
        datafram_tokens = pd.DataFrame(docjson['tokens'])
        print(datafram_tokens)
        datafram_tokens['token'] = datafram_tokens[['start','end']].apply(
            lambda x:doc_text[x[0]:x[1]] , axis = 1)

        datafram_tokens.drop(datafram_tokens[datafram_tokens['token'] == '$'].index, inplace = True)
        datafram_tokens.drop(datafram_tokens[datafram_tokens['token'] == 'date'].index, inplace = True)

        right_table = pd.DataFrame(docjson['ents'])[['start','end','label']]
        datafram_tokens = pd.merge(datafram_tokens,right_table,how='inner',on='end')
        datafram_tokens.fillna('O',inplace=True)
        datafram_tokens['start']=datafram_tokens['start_y']

        # join lable to df_clean dataframe
        df_clean['end'] = df_clean['text'].apply(lambda x: len(x)+1).cumsum() - 1 
        df_clean['start'] = df_clean[['text','end']].apply(lambda x: x[1] - len(x[0]),axis=1)

        # inner join with start 
        dataframe_info = pd.merge(df_clean,datafram_tokens[['start','token','label']],how='inner',on='start')

        #bounding box

        bb_df = dataframe_info.query("label != 'O' ")

        bb_df['label'] = bb_df['label'].apply(lambda x: x[2:])

        bb_df['group'] = bb_df['label'].apply(grp_gen.getgroup)

        # right and bottom of bounding box
        bb_df[['left','top','width','height']] = bb_df[['left','top','width','height']].astype(int)
        bb_df['right'] = bb_df['left'] + bb_df['width']
        bb_df['bottom'] = bb_df['top'] + bb_df['height']

        # tagging: groupby group
        col_group = ['left','top','right','bottom','label','token','group']
        group_tag_img = bb_df[col_group].groupby(by='group')

        img_tagging = group_tag_img.agg({

            'left':min,
            'right':max,
            'top':min,
            'bottom':max,
            'label':np.unique,
            'token':lambda x: " ".join(x)

        })

        print(img_tagging)
        print("img_bb ", img_bb)
        # for l,r,t,b,label,token in img_tagging.values:
        #     cv2.rectangle(img_bb,(l,t),(r,b),(0,255,0),2)

        #     cv2.putText(img_bb,str(label),(l,t),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255))

        #Entities

        info_array = dataframe_info[['token','label']].values
        
        previous = 'O'

        for token, label in info_array:
            bio_tag = label[0]
            label_tag = label[2:]

            # step -1 parse the token
            text = parser(token,label_tag)
            print("text is ", text)

            if bio_tag in ('B','I'):

                if previous != label_tag:
                    entities[label_tag].append(text)

                else:
                    if bio_tag == "B":
                        entities[label_tag].append(text)

                    else:
                        if label_tag in ("NAME"):
                            entities[label_tag][-1] = entities[label_tag][-1] + " " + text

                        else:
                            entities[label_tag][-1] = entities[label_tag][-1] + text



            previous = label_tag
        print("entities ", entities)    
        return img_bb, entities
    else:
        entities = dict(NAME=['NULL'],DATE=['NULL'],NUMBER=['NULL'],TOTAL=['NULL'])
        print("Cannot OCR  ", entities)    
        return img_bb, entities

