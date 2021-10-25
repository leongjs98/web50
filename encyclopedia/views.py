from django.shortcuts import render
from markdown2 import markdown

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