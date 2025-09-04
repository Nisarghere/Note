from django.urls import path
from . import views
from .views import NoteListView, NoteCreate , NoteSearchView   # 👈 import the class
from .views import NoteUpdateView, NoteDelete, PinView, UpdateProfile, ShareNoteView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path("note/<int:pk>/pin/", PinView.as_view(), name="pin_view"),
    path('create/', NoteCreate.as_view(), name='create_note'),
    path('edit/<int:pk>/', NoteUpdateView.as_view(), name='edit_note'),
    path('delete/<int:pk>/', NoteDelete.as_view(), name='delete_note'),
    path('profile/edit/', UpdateProfile.as_view(), name='update_profile'),
    path("share/<int:pk>/", ShareNoteView.as_view(), name="share_note"),
    path("ajax/search/", NoteSearchView.as_view(), name="note-search"),

    
 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)