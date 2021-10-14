from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name = "home"),
    path('note',views.notes, name = "notes"),
    path('delete_note/<int:pk>',views.delete_note, name = "delete-notes"),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(), name = "notes-detail"),


    
#homework


    path('homework',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update-homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete-homework"),


]