from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import Markdown
from django import forms
import random

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "code": 404,
            "errorMassage": "The Page you are looking for doesn't exist."
        })

    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(content)
        })

def search(request):
    markdowner = Markdown()
    if request.method == "POST":
        entry_search = request.POST['q']
        if util.get_entry(entry_search) is not None:
            return render(request, "encyclopedia/entry.html", {
                "entry": markdowner.convert(util.get_entry(entry_search)),
                "title": entry_search
            })
        existingEntries = util.list_entries()
        substringList = []
        for entry in existingEntries:
            if entry_search.lower() in entry.lower():
                substringList.append(entry)
        return render(request, "encyclopedia/result.html", {
            "results": substringList
        })

def newEntry(request):
    markdowner = Markdown()
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            existingTitle = util.get_entry(title)

            if existingTitle is not None:
                return render(request, "encyclopedia/error.html", {
                    "code": 409,
                    "errorMassage": "Page Name Already Exists."
                })
            
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdowner.convert(content)
            })
        
        return render(request, "encyclopedia/error.html", {
            "code": 403,
            "errorMassage": "Invalid format or Fill both Title and Markdown content in."
        })
    
    return render(request, "encyclopedia/newpage.html")

def edit(request):
    markdowner = Markdown()
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": markdowner.convert(content)
        })
    
def save_edit(request):
    markdowner = Markdown()
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(content)
        })
    
def randomEntry(request):
    markdowner = Markdown()
    existingEntries = util.list_entries()
    title = random.choice(existingEntries)
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdowner.convert(content)
    })

def deletePage(request, title):
    util.delete_entry(title)
    return HttpResponseRedirect(reverse("index",), {
        "entries": util.list_entries()
    })