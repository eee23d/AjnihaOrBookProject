
from django.shortcuts import render,redirect
import requests
# Create your views here.
from datetime import datetime, timedelta
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Book,ReaderAccount,ReadingRecords,contacts,Shelves,shelves_Readers_Books,booksuggest,liked_post
from django.core import files
from io import BytesIO

#index page
def index(request):
    return render(request,['AJNIHA/indexa.html'])

#notes page
@login_required(login_url='loginPage')
def notes(request):
    user = request.user
    nav1 = request.POST.get("typeTrack")
    myNotes = ReadingRecords.objects.filter(book_shelf_user__reader__username=user)
    liskedNotes= liked_post.objects.filter(liked_by__username__username__exact=user)
    shelves = Shelves.objects.filter(Reader__username__exact=user)
    shelf_reader_books = shelves_Readers_Books.objects.filter(reader__username__exact=user)
    shelf_books = Book.objects.filter(id__in=shelf_reader_books)
    error=""
    if request.method == "POST":
        if "AddNote" in request.POST:
            title= request.POST.get('title')
            note = request.POST.get('note')
            fromP =request.POST.get('fromP')
            toP = request.POST.get('toP')
            date = datetime.now()
            private= request.POST.get('private')
            if private=="on":
                private=True
            else:
                private=False
            bookSelect= request.POST.get("shelfSelect")
            book_shelf_user = shelves_Readers_Books.objects.filter(reader__username__exact=user,book__bookTitle__exact=bookSelect)
            record = ReadingRecords(book_shelf_user=book_shelf_user.first(),note_title=title,date=date,fromPage=fromP,toPage=toP,note=note,private=private)
            record.save()
            return niv(request,"myNotes","succA")
        elif "AddNoteEdit" in request.POST:
            title = request.POST.get('titleEdit')
            note = request.POST.get('noteEdit')
            fromP = request.POST.get('fromPEdit')
            toP = request.POST.get('toPEdit')
            noteId = request.POST.get("noteSelected")
            private = request.POST.get('privateEdit')
            nav1="myNotes"
            if private == "on":
                private = True
            else:
                private = False
            bookSelect = request.POST.get("shelfSelectEdit")
            book_shelf_user = shelves_Readers_Books.objects.filter(reader__username__exact=user,
                                                               book__bookTitle__exact=bookSelect)

            Record = ReadingRecords.objects.filter(id__exact=noteId).first()
            Record.book_shelf_user=book_shelf_user.first()
            Record.note_title=title
            Record.fromPage=fromP
            Record.toPage=toP
            Record.note=note
            Record.private=private
            Record.save()
            return niv(request, "myNotes", "succE")
        elif "noteToDelete" in request.POST:
            nav1 = request.POST.get("type")
            noteId= request.POST.get("noteDelete")
            noteId =ReadingRecords.objects.filter(id__exact=noteId)
            noteId.delete()
            return niv(request, "myNotes", "succD")
        elif "FavA" in request.POST:
            noteId = request.POST.get("txt")
            nav1= request.POST.get("t")
            noteId = ReadingRecords.objects.filter(id__exact=noteId).first()
            Reader = ReaderAccount.objects.filter(username__username__exact= user).first()
            var_com = liked_post(note_id=noteId,liked_by=Reader)
            try:
                var_com.save()
            except:
                var_com = liked_post.objects.filter(note_id=noteId,liked_by=Reader).first()
                var_com.delete()
            return niv(request, nav1,"succL")
        elif "search" in request.POST:
            typeOfNotes = request.POST.get("t")
            filterKey = request.POST.get("search-boc")
            return filterNotes(request,typeOfNotes,filterKey)

        else:
           return niv(request,nav1,"")
    else:
        return niv(request, "myNotes","")


#for navigation in note page, it will return the page with required variable
def niv(request,nav1,msg):
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    user = request.user
    allNotes = ReadingRecords.objects.filter(private__exact=False) | ReadingRecords.objects.filter(
        book_shelf_user__reader__username=user)
    myNotes = ReadingRecords.objects.filter(book_shelf_user__reader__username=user)
    liskedNotes = liked_post.objects.filter(liked_by__username__username__exact=user)
    shelves = Shelves.objects.filter(Reader__username__exact=user)
    shelf_reader_books = shelves_Readers_Books.objects.filter(reader__username__exact=user)
    shelf_books = Book.objects.filter(id__in=shelf_reader_books)
    if nav1 == "myNotes":
        return render(request, ['AJNIHA/notes.html'],
                      {'notes': myNotes, "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                       'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes,'reader': reader})
    elif nav1 == "glob":
        return render(request, ['AJNIHA/notes.html'],
                      {'notes': allNotes, "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                       'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes,'reader': reader})
    elif nav1 == "liked":
        return render(request, ['AJNIHA/notes.html'],
                      {'notes': liskedNotes, "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                       'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes,'reader': reader})

    return render(request, ['AJNIHA/notes.html'],
                  {'notes': "", "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                   'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes,'reader': reader})


#for note searching
def filterNotes(request,nav1,filterKey):
    user = request.user
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    msg=""
    shelves = Shelves.objects.filter(Reader__username__exact=user)
    shelf_reader_books = shelves_Readers_Books.objects.filter(reader__username__exact=user)
    shelf_books = Book.objects.filter(id__in=shelf_reader_books)

    liskedNotes = liked_post.objects.filter(liked_by__username__username__exact=user,note_id__note__contains=filterKey) \
                  |liked_post.objects.filter(liked_by__username__username__exact=user,note_id__note_title__contains=filterKey)
    if nav1 == "myNotes":
        myNotes = ReadingRecords.objects.filter(book_shelf_user__reader__username=user, note__contains=filterKey)\
                  |ReadingRecords.objects.filter(book_shelf_user__reader__username=user, note_title__contains=filterKey)
        if not myNotes:
            msg="no results"
        return render(request, ['AJNIHA/notes.html'],
                      {'notes': myNotes, "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                       'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes})
    elif nav1 == "glob":

        allNotes = ReadingRecords.objects.filter(private__exact=False,
                                                 note__contains=filterKey) | ReadingRecords.objects.filter(
            book_shelf_user__reader__username=user, note__contains=filterKey)|ReadingRecords.objects.filter(
            book_shelf_user__reader__username=user, note_title__contains=filterKey) |ReadingRecords.objects.filter(
            private__exact=False, note_title__contains=filterKey)
        if not allNotes:
            msg="no results"
        return render(request, ['AJNIHA/notes.html'],
                      {'notes': allNotes, "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                       'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes})
    elif nav1 == "liked":
        if not liskedNotes:
            msg="no results"
        return render(request, ['AJNIHA/notes.html'],
                      {'notes': liskedNotes, "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                       'bookForShelf': shelf_reader_books, 'message': msg, 'fav': liskedNotes})

    return render(request, ['AJNIHA/notes.html'],
                  {'notes': "", "nav": nav1, 'shelves': shelves, 'shelf_books': shelf_books,
                   'bookForShelf': shelf_reader_books, 'message': "error", 'fav': liskedNotes})


#contact page (Send message)
@login_required(login_url='loginPage')
def contact(request):
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    if request.method=="POST":
        userName=request.POST.get('name')
        userEmail=request.POST.get('email')
        userSub=request.POST.get('subject')
        userMessage=request.POST.get('message')
        var_contact=contacts(name=userName,email=userEmail,title=userSub,message=userMessage)
        var_contact.save()
        return render(request,['AJNIHA/thanks.html'],{'reader': reader})
    else:
        return render(request,['AJNIHA/contact.html'],{'reader': reader})

#add book page
@login_required(login_url='loginPage')
def search(request):
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
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
                return render(request, ['AJNIHA/search.html'], {'response':response,'shelves': shelves,'searchType':searchSelect,'error':"",'reader': reader})
            else:
                books=Book.objects.filter(bookTitle__contains=search)
                if not books:
                    books="no results"
                return render(request, ['AJNIHA/search.html'], {'response':books,'shelves': shelves,'searchType':searchSelect,'error':"",'reader': reader})

        elif "addBookSearched" in request.POST:

            shelfselect = request.POST.get('shelfSelect')
            if not shelfselect:
                return render(request, ['AJNIHA/search.html'],{'response': "", 'shelves': shelves, 'searchType': "",'error':"notComplete",'reader': reader})
            shelf = Shelves.objects.filter(shelfName__exact=shelfselect,Reader__username__exact=request.user)
            searchSelect = request.POST.get('searchSelect')
            if searchSelect=="1":
                bookSelfUrl = request.POST.get('rGroup')
                if not bookSelfUrl:
                    return render(request, ['AJNIHA/search.html'],
                                  {'response': "", 'shelves': shelves, 'searchType': "", 'error': "notComplete",'reader': reader})
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
                        try:
                            imgurl=response["volumeInfo"]['imageLinks']['thumbnail']
                            resp = requests.get(imgurl)
                            if resp.status_code != requests.codes.ok:
                                return render(request, ['AJNIHA/search.html'],
                                              {'response': "", 'shelves': shelves, 'searchType': "",
                                               'error': "error in loading info :'(",'reader': reader})
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
                        except:
                            var_contact = Book(author=author, pageNo=pageNo, bookTitle=title, description=description,)
                            var_contact.save()
                            user_read = shelves_Readers_Books(reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=var_contact, shelf=shelf.first())
                            user_read.save()
                        return render(request, ['AJNIHA/search.html'],
                                    {'response': "", 'shelves': shelves, 'searchType': "", 'error': "success",'reader': reader})
                    else:
                        var_contact = Book.objects.filter(bookTitle__exact=title,author__exact=author)
                        user_read = shelves_Readers_Books(
                            reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=var_contact.first(),
                            shelf=shelf.first())
                        user_read.save()
                        return render(request, ['AJNIHA/search.html'],
                                      {'response': "", 'shelves': shelves, 'searchType': "", 'error': "success",'reader': reader})
            else:
                bookselected = request.POST.get('rGroup')
                book = Book.objects.filter(bookTitle__exact=bookselected).first()
                user_read = shelves_Readers_Books(
                    reader=ReaderAccount.objects.filter(username__exact=request.user).first(), book=book,
                    shelf=shelf.first())
                user_read.save()
                return render(request, ['AJNIHA/search.html'],
                              {'response': "", 'shelves': shelves, 'searchType': "1",'error':"",'reader': reader})

    else:
        return render(request,['AJNIHA/search.html'],{'response':"",'shelves': shelves,'error':"",'reader': reader})

#library page
@login_required(login_url='loginPage')
def library(request):
    user = request.user
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    if request.method == "POST":
        if "bookToDelete" in request.POST:
            book_id= request.POST.get("bookDelete")
            bookToDel=shelves_Readers_Books.objects.filter(id__exact=book_id).first()
            bookToDel.delete()
        else:
            sheldName= request.POST.get("addShelf")
            shelf= Shelves(Reader= ReaderAccount.objects.filter(username__exact=request.user).first(),shelfName=sheldName,shelfType="3")
            shelf.save()
    shelves = Shelves.objects.filter(Reader__username__exact=user)
    shelf_reader_books = shelves_Readers_Books.objects.filter(reader__username__exact=user)
    shelf_books = Book.objects.filter(id__in=shelf_reader_books)
    return render(request,['AJNIHA/library1.html'],{'shelves': shelves,'shelf_books':shelf_books,'bookForShelf':shelf_reader_books,'reader': reader})

#go to note page if user account is valid
@login_required(login_url='loginPage')
def userHome(request):
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        reader.prof_pic=myfile
        reader.save()
    return render(request, ['AJNIHA/notes.html'], {'reader': reader})

#register account
def register(request):

    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account was created for '+form.cleaned_data.get('username'))
            return redirect('loginPage')
    context={'form':form}
    return render(request,'AJNIHA/register.html',context)



#login
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('notes')
    else:
        if request.method=='POST':
            #taking thr value of these fields
            username=request.POST.get('username')
            password=request.POST.get('password')
            user =authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                reader = ReaderAccount.objects.filter(username__username__exact= user).first()
                return render(request,['AJNIHA/notes.html'],{'reader':reader})
            else:
                messages.info(request,'username or password is incorrect')

        context={}
        return render(request,['AJNIHA/login.html'],context)


#change profile page
def setting(request):
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            reader.prof_pic = myfile
            reader.save()
        except:
            pass
    return render(request, ['AJNIHA/setting.html'], {'reader': reader})

#reading statistic page
@login_required(login_url='loginPage')
def stat(request):
    one_week_ago = datetime.today() - timedelta(days=7)
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    completedBooks= shelves_Readers_Books.objects.filter(reader = ReaderAccount.objects.filter(username__username__exact=request.user).first(),shelf__shelfType__exact=4).count()
    daily = ReadingRecords.objects.filter( book_shelf_user__reader = ReaderAccount.objects.filter(username__username__exact=request.user).first(),date__day=datetime.now().day,date__month=datetime.now().month,date__year=datetime.now().year)
    weekly = ReadingRecords.objects.filter( book_shelf_user__reader = ReaderAccount.objects.filter(username__username__exact=request.user).first(),date__gte=one_week_ago,date__month=datetime.now().month,date__year=datetime.now().year)
    monthly = ReadingRecords.objects.filter( book_shelf_user__reader = ReaderAccount.objects.filter(username__username__exact=request.user).first(),date__month=datetime.now().month,date__year=datetime.now().year)
    yearly = ReadingRecords.objects.filter( book_shelf_user__reader = ReaderAccount.objects.filter(username__username__exact=request.user).first(),date__year=datetime.now().year)

    pagenumDaily = 0
    pageWeekly=0
    pagenumonthly = 0
    pageYearly =0
    for read in daily:
        pagenumDaily += int(read.toPage) - int(read.fromPage) +1
    for read in weekly:
        pageWeekly += int(read.toPage) - int(read.fromPage) +1
    for read in monthly:
        pagenumonthly += int(read.toPage) - int(read.fromPage) +1
    for read in yearly:
        pageYearly += int(read.toPage) - int(read.fromPage) +1

    return render(request,['AJNIHA/stat.html'],{'reader': reader,'bookNum':completedBooks,'pagenumDaily':pagenumDaily,'pageWeekly':pageWeekly,'pagenumonthly':pagenumonthly,'pageYearly':pageYearly })

#page to choose contact mwthod
def contactUs(request):
    reader = ReaderAccount.objects.filter(username__username__exact=request.user).first()
    return render(request,['AJNIHA/contactUs.html'],{'reader':reader})

#suggest book page
def suggest(request):
    if request.method == "POST":
        booktitle = request.POST.get('bookTitle')
        bookDescription = request.POST.get('description')
        var_suggestion = booksuggest(accountUser=ReaderAccount.objects.filter(username__exact=request.user).first(),
                                     book_Title=booktitle, book_description=bookDescription)
        var_suggestion.save()
        return render(request, ['AJNIHA/thanks.html'])
    else:
        return render(request, ['AJNIHA/suggest.html'])

#thank page after contact
def thanks(request):
    return render(request,['AJNIHA/thanks.html'])

#logout account and end session
def logoutUser(request):
    logout(request)
    return redirect('loginPage')