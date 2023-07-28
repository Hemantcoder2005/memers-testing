from celery import shared_task
from nltk.stem.porter import PorterStemmer
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer as count
from sklearn.metrics.pairwise import cosine_similarity 
import cv2
import pytesseract
from pytesseract import Output
ps=PorterStemmer()

myconfig=r"--psm 11 --oem 3"

def stem(text):
    y=[]
    for i in text.split():
        i=i.lower()
        y.append(ps.stem(i))
    return " ".join(y)

@shared_task(bind=True)
#ML Algorithm.
def train(request,ids=0,image=None,what_uploaded=""):
    print('MEMES Training started')
    extracted_image=image[image.find('media'):]
    img=cv2.imread(extracted_image)
    data=pytesseract.image_to_data(img,config=myconfig,output_type=Output.DICT)
    boxes=len(data['text'])
    img_data=''
    for i in range(boxes):
        if float(data['conf'][i]) >80:
            img_data=img_data+" "+data['text'][i]
    img_data=img_data+str(what_uploaded)

    # #Saving Data into organised way
    what_uploaded=stem(str(img_data))
    memes=pd.read_csv('ML\\RawIn.csv')
    memes=memes.append({'tags':what_uploaded,'ids':ids},ignore_index=True)
    memes.to_csv('ML\\RawIn.csv',index=False)

    memes=pd.read_csv('ML\\RawIn.csv')
    np.save('ML\\ids.npy',memes['ids'])
    #Vectorizing Data
    memes['tags'] = memes['tags'].fillna('')
    cv=count(max_features=7000,stop_words='english')
    vectors=cv.fit_transform(memes['tags']).toarray()
    sv=cosine_similarity(vectors)
    np.save('ML\\trained_data.npy', sv)
    return 'MEMES Trained!'

