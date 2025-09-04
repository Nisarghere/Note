from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "timestamp", "is_archived", "is_pinned", "last_updated" )
    list_editable = ("is_pinned","is_archived")  
    search_fields = ("title", "content")
    list_filter = ("owner", "timestamp")   
    ordering = ("-timestamp",)       
    readonly_fields = ("timestamp",)  
    
    
    fieldsets=(
        ("Note details", {"fields": ("title", "content", "is_archived", "is_pinned")}),
        ("Ownership", {"fields":("owner",)}),
        ("TimeStamp", {"fields":("timestamp",)}),
    )  

     
    actions = ["mark_as_archived","mark_as_unarchived","mark_as_pinned", "mark_as_unpinned"]
    
    def mark_as_archived(self, request, queryset):
        queryset.update(is_archived=True)
        self.message_user(request, "The selected Note has been archived")
    
    def mark_as_unarchived(self, request, queryset):
        queryset.update(is_archived=False)
        self.message_user(request, "The selected Note has been Unarchived")
        
    def mark_as_pinned(self, request, queryset):
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f"{updated} note(s) pinned.")

    def mark_as_unpinned(self, request, queryset):
        updated = queryset.update(is_pinned=False)
        self.message_user(request, f"{updated} note(s) unpinned.")
        
        
admin.site.register(Note, NoteAdmin)
