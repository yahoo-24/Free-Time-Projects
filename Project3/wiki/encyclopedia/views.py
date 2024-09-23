from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
from random import choice


def index(request):
    if request.method == "POST":
        form = request.POST['q']
        entries = util.list_entries()
        if form in entries:
            return redirect('Entry', Title=form)
        else:
            PossibleEntries = []
            for entry in entries:
                if form in entry:
                    PossibleEntries.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": PossibleEntries
            })
    
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def Entry(request, Title):
    markdowner = Markdown()
    if util.get_entry(Title) != None:
        Content = markdowner.convert(util.get_entry(Title))
        return render(request, "encyclopedia/entry.html", {
            "Content": Content,
            "Title": Title
        })
    else:
        return render(request, "encyclopedia/error.html")

def Random(request):
    Entries = util.list_entries()
    Topic = choice(Entries)
    return redirect('Entry', Title=Topic)

def NewPage(request):
    if request.method == "POST":
        Title = request.POST['Title']
        Content = request.POST['Contents']
        Entries = util.list_entries()
        Entries = [entry.upper() for entry in Entries]
        if Title.upper() not in Entries:
            util.save_entry(Title, Content)
            return redirect('Entry', Title=Title)
        else:
            return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/NewPage.html")
    
def EditPage(request, Title):
    if request.method == "POST":
        Content = request.POST['Contents']
        util.save_entry(Title, Content)
        return redirect('Entry', Title=Title)
    
    else:
        Content = util.get_entry(Title)
        if Content != None:
            return render(request, "encyclopedia/EditPage.html", {
                "Title": Title,
                "Content": Content
            })
        else:
            return render(request, "encyclopedia/error.html")