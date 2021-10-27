from django.shortcuts import render
from django.contrib import messages
from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    entry = util.get_entry(title)

    # If entry exists
    if entry:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": markdown(entry)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


def search(request):
    # Get the value from the search bar
    search = request.POST['q']

    entry = util.get_entry(search)

    # If the search is one of the entries
    if entry:
        return title(request, search)

    # If the search doesn't match all the entries
    else:
        all_entries = util.list_entries()
        similar_entries = []
        for entry in all_entries:
            if search.lower() in entry.lower(): # Make sure the cases match
                similar_entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            'entries': similar_entries
        })


def edit(request, title):
    content = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


# for edit only rn
def submit(request):
    content = request.POST.get("new_content")
    entry_title = request.POST.get("title")
    new_page = request.POST.get("new")

    entries = util.list_entries()
    util.save_entry(entry_title, content)

    if new_page == "True":
        if entry_title in entries:
            messages.info(request, f'The title, {entry_title} already exists.')
            return new(request)

    # Remove empty lines from the md file
    with open(f'entries/{entry_title}.md', 'r') as entry_file:
        lines = entry_file.readlines()
        
    with open(f'entries/{entry_title}.md', 'w') as new_entry_file:
        for line in lines:
            if not line.isspace():  # Only rewrite the non-empty lines
                new_entry_file.write(line)
    
    return title(request, entry_title)


def new(request):
    return render(request, 'encyclopedia/new.html')


def random(request):
    entries = util.list_entries()
    # Select a random entry from all entries via the "random" library
    entry = choice(entries)
    return title(request, entry)