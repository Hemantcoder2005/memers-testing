from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import memes
import numpy as np
from random import choice
from .models import memes,Tags


#remove
import pandas as pd

#Useful functions
def fetching_memes(select):
    '''This will fetch memes'''
    memes_data=[]
    for which in select:
        getmeme=memes.objects.get(id=which)
        memes_data.append({'id':getmeme.id,'image':getmeme.meme,'tags':getmeme.tagged,'memed_by':getmeme.author,'comments':getmeme.comments,'memed_on':getmeme.created_on})
    return memes_data
def load_memes():
    TrainedMemes=np.load('ML\\trained_data.npy')
    ids=list(np.load('ML\\ids.npy'))
    select=[]
    for i in range(5):
        select.append(choice(ids))
    return fetching_memes(select)



# Create your views here.
@login_required
def home(request):
    parms={}
    memes=load_memes()
    parms['memes']=memes
    return render(request,'home/home.html',parms)
