from django.contrib import admin
from .models import Book,ReaderAccount,ReadingRecords,contacts,Shelves,shelves_Readers_Books,booksuggest,follow,liked_post
# Register your models here.

# Register your models here.
admin.site.register(Book)
admin.site.register(ReaderAccount)
admin.site.register(ReadingRecords)
admin.site.register(contacts)
admin.site.register(Shelves)
admin.site.register(shelves_Readers_Books)
admin.site.register(booksuggest)
admin.site.register(follow)
admin.site.register(liked_post)
