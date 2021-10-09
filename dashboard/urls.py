from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name = "home"),
    path('note',views.notes, name = "notes"),
    path('delete_note/<int:pk>',views.delete_note, name = "delete-notes"),
    # path('notes_detail/<int:pk>',views.NotesDetailView.as_view(), name = "notes-detail"),


    
#homework


    path('homework',views.homework,name="homework"),

]