from django.shortcuts import render,redirect,get_object_or_404
from home import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .task import train

MemesModel=models.memes
MemesTags=models.Tags
User=get_user_model()

@login_required
def upload(request):
    user=User.objects.get(username=request.user.username)
    if request.method=='POST':
        #Collect useful data
        collect_data=request.POST.get
        title=collect_data('title')
        tagged=collect_data('tagged').split(',')
        meme=request.FILES.get('meme')
        #Creates Tags if is not in database
        for tag in tagged: 
            tag=tag.lower()
            tags_exist=list(MemesTags.objects.filter(name=tag))
            if tags_exist ==[]:
                create_tag=MemesTags(name=tag,created_by=user,meme_tagged=1)
                create_tag.save()
            else:
                update_tag=get_object_or_404(MemesTags, name=tag)
                update_tag.meme_tagged+=1
                update_tag.save()
        
        #saves Meme
        save_meme=MemesModel.objects.create(title=title,author=user,meme=meme)
        filter_tagged=MemesTags.objects.filter(name__in=tagged)
        save_meme.tagged.set(filter_tagged)
        save_meme.save()
        ids=save_meme.id
        image=save_meme.meme.path

        train.delay(what_uploaded=f'{collect_data("tagged")}',ids=ids,image=image)
            
    return render(request,'upload.html')