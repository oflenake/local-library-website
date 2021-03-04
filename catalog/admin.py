"""
Minimal registration of Models.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)
"""

from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


admin.site.register(Genre)
admin.site.register(Language)


class BooksInline(admin.TabularInline):
    """
    Defines the format of the books inline.
    Occurs at insertion of books inline.
    Used in class: catalog.admin.AuthorAdmin.
    """
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Administration object for Author models.
    Defines:
     - Fields to be displayed in list view (list_display).
     - Orders fields in detail view (fields), grouping 
       the date fields horizontally.
     - Adds inline addition of books in author view (inlines).
    """
    list_display = ('surname', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'surname', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
    """
    Defines the format of the books instance inline.
    Occurs at insertion of books instance inline.
    Used in class: catalog.admin.BookAdmin.
    """
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    """
    Administration object for Book models.
    Defines:
     - Fields to be displayed in list view (list_display).
     - Adds inline addition of book instances in book view (inlines).
    """
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


admin.site.register(Book, BookAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """Administration object for BookInstance models.
    Defines:
     - Fields to be displayed in list view (list_display).
     - Filters that will be displayed in sidebar (list_filter).
     - Grouping of fields into sections (fieldsets).
    """
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
