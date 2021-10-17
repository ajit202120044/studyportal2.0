from django.shortcuts import render
from . forms import *
from django.contrib import messages
from django.views import generic
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')
@login_required
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
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id = pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes    

    # homework

@login_required
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
@login_required
def update_homework(request,pk = None):
    homework = Homework.objects.get(id =pk)
    if homework.is_finished == True:
        homework.is_finished =False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


# delete homework
@login_required
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


    # todo 
@login_required
def todo (request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if  form .is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            ) 
            todos.save()
            messages.success(request,f"Todo added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo =Todo.objects.filter(user=request.user)
    if len(todo)== 0:
        todo_done = True
    else:
        todo_done = False


    return render (request,"dashboard/todo.html", {'todos':todo,'form':form,'todo_done':todo_done})


    #update todo
@login_required
def update_todo(request,pk= None):
    todo = Todo.objects.get(id =pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')
@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')






#registartion
def register(request):
    if request.method  == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            messages.success(request,f" Congratulations!! Account Created for {username}!!!")
            #redirect to login
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request,"dashboard/register.html",{'form':form})



    #profile
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished= False, user = request.user)
    todos = Todo.objects.filter(is_finished= False, user = request.user)
    if len(homeworks)== 0:
        homework_done = True
    else:
        homework_done = False

    if len(todos)== 0:
        todo_done = True
    else:
        todo_done = False

    return render(request,"dashboard/profile.html",{'homeworks':homeworks,
    'todos':todos,
    'homework_done':homework_done,
    'todo_done':todo_done})
