from django.shortcuts import render
from . forms import *
from django.contrib import messages
from django.views import generic
from django.shortcuts import redirect

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
    #context = {}
    return render(request, 'dashboard/note.html', {'notes': notes,'form':form})

def delete_note(request,pk=None):
    Notes.objects.get(id = pk).delete()
    return redirect("notes")

# class  NotesDetailView(generic . DetailView):
#     model = Notes    

    # homework


def homework(request):

    
    return render(request,'dashboard/homework.html', {'dests':dests})
