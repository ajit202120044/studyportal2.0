from django.shortcuts import render
from . forms import *
from django.contrib import messages
from django.views import generic
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from youtubesearchpython import VideosSearch

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if  form.is_valid():
            notes = Notes(user= request.user,title = request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")
        # messages.success(request, 'Profile details updated.')
    else:

        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
  
    return render(request, 'dashboard/note.html', {'notes': notes,'form':form})
#deleting notes

def delete_note(request,pk=None):
    Notes.objects.get(id = pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes    

    # homework


def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
          
            homeworks = Homework(
                    user = request.user,
                    subject = request.POST['subject'],
                    title = request.POST['title'],
                    description = request.POST['description'],
                    due = request.POST['due'],
                    is_finished = finished
              
            )    
            homeworks.save()
            messages.success(request,f"homework Added from {request.user.username} Successfully")  
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
        
    return render(request,'dashboard/homework.html', {'homeworks':homework, 'homework_done': homework_done,'form':form})

# upadting homework
def update_homework(request,pk = None):
    homework = Homework.objects.get(id =pk)
    if homework.is_finished == True:
        homework.is_finished =False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


# delete homework
def delete_homework(request,pk= None):
     Homework.objects.get(id =pk).delete()
     return redirect("homework")


#youtube section 


def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video= VideosSearch(text,limit=20)
        result_list = []
        for i in video.result()['result']:

            result_dict ={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if  i['descriptionSnippet']:
                for  j in i['descriptionSnippet']:
                    desc  += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        return render(request,'dashboard/youtube.html',{'form': form,'results':result_list})
      
    else:
        form = DashboardForm()
    return render(request,'dashboard/youtube.html',{'form': form})
