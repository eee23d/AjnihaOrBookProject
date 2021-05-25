from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
import requests
#from .models import Contact, Blog, Course
# Create your views here.
#from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Book,ReaderAccount,ReadingRecords,contacts,Shelves,shelves_Readers_Books,booksuggest,follow,liked_post
import urllib.request
from django.core import files
from io import BytesIO

#string-->http response
#@login_required(login_url='loginPage')
def index(request):
    return render(request,['AJNIHA/indexa.html'])

def notes(request):
    return render(request,['AJNIHA/notes.html'])

def contact(request):
    return render(request,['AJNIHA/contact.html'])



def search(request):
    user = request.user
    shelves = Shelves.objects.filter(Reader__username__exact=user)
    if request.method == "POST":
        search = request.POST.get('search-box')
        if "search" in request.POST:
            searchSelect = request.POST.get('searchSelect')
            if searchSelect== "1":
                str(search).split("+")
                url = "https://www.googleapis.com/books/v1/volumes?q="+search
                response = requests.get(url).json()
                if search== "" or search == None:
                    response="no results"
                elif response['totalItems']==0:
                    response = "no results"
                else:
                    response = response['items']
                return render(request, ['AJNIHA/search.html'], {'response':response,'shelves': shelves,'searchType':searchSelect,'error':""})
            else:
                books=Book.objects.filter(bookTitle__contains=search)
                if not books:
                    books="no results"
                return render(request, ['AJNIHA/search.html'], {'response':books,'shelves': shelves,'searchType':searchSelect,'error':""})

        elif "addBookSearched" in request.POST:

            shelfselect = request.POST.get('shelfSelect')
            if not shelfselect:
                return render(request, ['AJNIHA/search.html'],{'response': "", 'shelves': shelves, 'searchType': "",'error':"notComplete"})
            shelf = Shelves.objects.filter(shelfName__exact=shelfselect,Reader__username__exact=request.user)
            searchSelect = request.POST.get('searchSelect')
            if searchSelect=="1":
                bookSelfUrl = request.POST.get('rGroup')
                if not bookSelfUrl:
                    return render(request, ['AJNIHA/search.html'],
                                  {'response': "", 'shelves': shelves, 'searchType': "", 'error': "notComplete"})
                response = requests.get(bookSelfUrl).json()
                if not response:
                    print("error no link")
                else:
                    try:
                        authors_ = response["volumeInfo"]["authors"]
                        author = ""
                        for a in authors_:
                            author += "," + a
                    except:
                        author = "None"
                    try:
                        title = str(response["volumeInfo"]["title"])
                    except:
                        title= "none"
                    try:
                        pageNo= str(response["volumeInfo"]["pageCount"])
                    except:
                        pageNo=None
                    try:
                        description=str( response["volumeInfo"]["description"])
                    except:
                        description="no description"
                    try:
                        isbn= response["volumeInfo"]["industryIdentifiers"][1]["identifier"]
                    except:
                        isbn= ""
                    bookTest = Book.objects.filter(bookTitle__exact=title,author__exact=author)
                    if not bookTest :
                        if response["volumeInfo"]['imageLinks']['thumbnail'] :
                            imgurl=response["volumeInfo"]['imageLinks']['thumbnail']
                            resp = requests.get(imgurl)
                            if resp.status_code != requests.codes.ok:
                                return render(request, ['AJNIHA/search.html'],
                                              {'response': "", 'shelves': shelves, 'searchType': "",
                                               'error': "error in loading info :'("})
                            fp = BytesIO()
                            fp.write(resp.content)
                            file_name=title+".jpg"
                            #urllib.request.urlretrieve(imgurl, title+".jpg")
                            var_contact = Book(author=author,  pageNo=pageNo,bookTitle=title,isbn=isbn, description=description,
                                                image="")
                            var_contact.image.save(file_name, files.File(fp))
                            var_contact.save()


                            user_read = shelves_Readers_Books(reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=var_contact, shelf=shelf.first())
                            user_read.save()
                            print("book added for user succ.")
                        else:
                            var_contact = Book(author=author, pageNo=pageNo, bookTitle=title, description=description,)
                            var_contact.save()
                            user_read = shelves_Readers_Books(reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=var_contact, shelf=shelf.first())
                            user_read.save()
                        return render(request, ['AJNIHA/search.html'],
                                    {'response': "", 'shelves': shelves, 'searchType': "", 'error': "success"})
                    else:
                        var_contact = Book.objects.filter(bookTitle__exact=title,author__exact=author)
                        user_read = shelves_Readers_Books(
                            reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=var_contact.first(),
                            shelf=shelf.first())
                        user_read.save()
                        return render(request, ['AJNIHA/search.html'],
                                      {'response': "", 'shelves': shelves, 'searchType': "", 'error': "success"})
            else:
                bookselected = request.POST.get('rGroup')
                book = Book.objects.filter(bookTitle__exact=bookselected).first()
                user_read = shelves_Readers_Books(
                    reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=book,
                    shelf=shelf.first())
                user_read.save()
                return render(request, ['AJNIHA/search.html'],
                              {'response': "", 'shelves': shelves, 'searchType': "1",'error':""})

    else:
        return render(request,['AJNIHA/search.html'],{'response':"",'shelves': shelves,'error':""})


def library(request):
    if request.method == "POST":
        pass
    else:
        user = request.user
        print(user)
        shelves = Shelves.objects.filter(Reader__username__exact= user)
        print(shelves)
        shelf_reader_books = shelves_Readers_Books.objects.filter(reader__username__exact=user)
        print(shelf_reader_books)
        shelf_books= Book.objects.filter(id__in=shelf_reader_books)

    return render(request,['AJNIHA/library1.html'],{'shelves': shelves,'shelf_books':shelf_books,'bookForShelf':shelf_reader_books})

@login_required(login_url='loginPage')
def userHome(request):
    Reader = ReaderAccount.objects.filter(username__exact=request.user)
    return render(request,['AJNIHA/userHomePage.html'],{'account':Reader})

def register(request):
    if request.user.is_authenticated:
        return redirect('userHome')
    if True:
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Account was created for '+form.cleaned_data.get('username'))
                return redirect('loginPage')
        context={'form':form}
        return render(request,'AJNIHA/register.html',context)




def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            #taking thr value of these fields
            username=request.POST.get('username')
            password=request.POST.get('password')
            print(username+" "+password)
            user =authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('userHome')
            else:
                messages.info(request,'username or password is incorrect')

        context={}
        return render(request,['AJNIHA/login.html'],context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')