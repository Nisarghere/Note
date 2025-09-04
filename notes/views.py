from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, UserProfile, NoteShare
from django.urls import reverse_lazy
from .forms import Noteform, Userprofileform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView , CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class NoteSearchView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get("q", "").strip()

        notes = Note.objects.filter(
            Q(owner=request.user) | Q(shared_to=request.user)
        ).distinct().order_by("-is_pinned", "-timestamp")

        if q:
            notes = notes.filter(Q(title__icontains=q) | Q(content__icontains=q))

        notes = notes[:10]

        # ✅ Render each note using your existing card partial template
        html = render_to_string("notes/_note_cards.html", {"notes": notes, "query": q}, request)

        return JsonResponse({"html": html})
    
class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile 
    template_name = 'notes/updateprof.html'
    form_class = Userprofileform
    success_url = reverse_lazy("note_list")
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user = self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)   
        


class PinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        note.is_pinned = not note.is_pinned
        note.save()
        return redirect("note_list")
    

class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    template_name = "notes/create_note.html"
    form_class= Noteform
    success_url= reverse_lazy("note_list")
     
    
    
    def form_valid(self, form):
        form.instance.owner = self.request.user  # optional, just ensures ownership
        return super().form_valid(form)
    
    
        
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/notes_list.html"
    context_object_name= "notes"
    paginate_by = 3
    def  get_queryset(self):
        query = self.request.GET.get("q")
        notes = Note.objects.filter(
            Q(owner=self.request.user) | Q(shared_to=self.request.user)
            ).distinct().order_by("-is_pinned", "-timestamp")
        
        if query:
            notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return notes
    
    
    def get_context_data(self, **kwargs):
        profile = None
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")  # ✅ add query to context
        context["profile"] = UserProfile.objects.get(user = self.request.user)
        return context

class ShareNoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        username = request.POST.get('username')
        permission = request.POST.get("permission", "view")
        user_to_share = get_object_or_404(User,username=username)
        note.shared_to.add(user_to_share)
        
        NoteShare.objects.update_or_create(
            note=note,
            user=user_to_share,
            defaults={"permission": permission}
        )
        return redirect("note_list")
    
    
class NoteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Note
    template_name = 'notes/edit_note.html'
    form_class = Noteform
    success_url = reverse_lazy("note_list")  # 👈 redirect after update
    permission_required = 'notes.change_note'
    
    def get_queryset(self):
        """Allow access to notes the user owns OR has 'edit' permission for"""
        owned_notes = Note.objects.filter(owner=self.request.user)
        shared_notes = Note.objects.filter(
            noteshare__user=self.request.user,
            noteshare__permission="edit"
        )
        return (owned_notes | shared_notes).distinct()

    def get_object(self, queryset=None):
        note = super().get_object(queryset)

        # Owner can edit
        if note.owner == self.request.user:
            return note

        # Shared with permission
        share = NoteShare.objects.filter(note=note, user=self.request.user).first()
        if share and share.permission == "edit":
            return note

        raise PermissionDenied("You don’t have permission to edit this note.")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # optional, just ensures ownership
        return super().form_valid(form)
      
    

class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('note_list')
    def get_queryset(self):
        return Note.objects.filter(owner = self.request.user)
  
        