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


def search(request, title):
    