from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def search(request):
    if request.method == "POST":
        query = request.POST["q"] 
        html_content = convert_md_to_html(query)
        all_entries = util.list_entries() 
        similar_entries=[]   
        if html_content != None:   
            return render(request, "encyclopedia/entries.html", {
                "content" : html_content ,
                "title": query
            })
        else:
            for entry in all_entries:
                if query.lower() in entry.lower():
                    similar_entries.append(entry)

            if similar_entries:
                return render(request, "encyclopedia/similar_entries.html", {
                    "similar_entries" : similar_entries
                })    

            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No pages match your search."
                })    



def create(request):
    if request.method == "POST":
        name=request.POST["name"]
        content = request.POST["description"]
        title = util.get_entry(name)
        if not name:
            return render(request, "encyclopedia/error.html", {
                    "message": "Should provide name of the article."
                }) 
        elif not content:
            return render(request, "encyclopedia/error.html", {
                    "message": "Page cannot be empty."
                })
        elif title != None:
            return render(request, "encyclopedia/error.html", {
                    "message": "Page already exists."
                })
        
        else:   
            util.save_entry(name, content)
            content = convert_md_to_html(name)
            return render(request, "encyclopedia/success.html", {
                "content" : util.get_entry(name),
                "title": name
            })

    return render(request, "encyclopedia/create.html")

def entry(request, title):
    html_content = convert_md_to_html(title)

    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist"
        })
    
    else:
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": html_content
        })

def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST["name"]
        content = request.POST["description"]
        util.save_entry(title, content)
        content = convert_md_to_html(title)
        return render(request, "encyclopedia/success.html", {
            "content" : util.get_entry(title),
            "title": title
        })
    
def random_page(request):
    all_entries=util.list_entries()
    guess = random.randrange(0, len(all_entries))
    title = all_entries[guess]
    content = util.get_entry(title)
    return render(request, "encyclopedia/entries.html", {
        "title":  title,
        "content": content
    })

