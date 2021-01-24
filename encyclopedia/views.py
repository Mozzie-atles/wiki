from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown2 import markdown
import random
import json
import os
p = """<form action="{% url 'wikip:edit' %}" method="GET">
    {% csrf_token %}
    <div style = " margin-top: 50px;">
    <input type="text" value="{{ name }}" hidden name="pretitle">
    <input type="submit" value="Edit" class="btn btn-dark">
    </div>
</form>"""
p1 = "{{ name }}"


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),

    })


def title(request, title):
    f = util.get_entry(title)
    if f != None:
        return render(request, f"entrieshtml/{title}.html", {
            "title": util.get_entry(title),
            "name": title,

        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_text": f"There is no such entries as {title}",

        })


def search(request):
    f = util.list_entries()
    title = request.GET.get('q')
    count = 0
    if request.method == "GET":
        for entry in f:
            if entry.upper() == title.upper():
                return render(request, f"entrieshtml/{title}.html", {
                    "title": util.get_entry(entry),
                    "name": entry,

                })
            else:
                for keyword in title:
                    for enter in f:
                        for key in enter:
                            if keyword.upper() == key.upper():
                                return render(request, "encyclopedia/keyword_match.html", {
                                    "name": enter
                                })
                                count += 1
                            else:
                                break
                    if count == 0:
                        return render(request, "encyclopedia/error.html", {
                            "error_text": f"no such entry as {title}",

                        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_text": f"Error 403 invalid method",

        })


def newtab(request, method=["POST"]):
    ''' i did't use util.save_entry, i actually forgot it was there orignaly, i found it after i wrote this code of my own, hope its okay '''

    if request.method == "POST":
        titles = request.POST.get('entry_name')
        content = request.POST.get('content')

        if os.path.exists(f'C:/Users/erfan/Desktop/Mozzie-atles/encyclopedia/templates/entrieshtml/{titles}.html'):
            return render(request, "encyclopedia/newtab.html", {
                "xin": 1
            })
        else:
            ali = f"\n{content}"
            with open(f'entries/{titles}.md', 'w') as f:
                f.write(ali)

            filepath = os.path.join(
                'C:/Users/erfan/Desktop/Mozzie-atles/encyclopedia/templates/entrieshtml', f'{titles}.html')

            with open(filepath, 'w') as f:
                x = markdown(ali)
                cheat = ["{% extends 'encyclopedia/layout.html' %}",
                         "{% block title %}", "{% endblock %}", "{% block body %}", p, p1]
                f.write(cheat[0])
                f.write(cheat[1])
                f.write(titles)
                f.write(cheat[2])
                f.write(cheat[3])
                f.write(x)
                f.write(p)
                f.write(cheat[2])

                """ for import layout.html in to the new file """
            return render(request, f"entrieshtml/{titles}.html")
    return render(request, "encyclopedia/newtab.html")


def ranpage(request):
    lists = []
    for f in util.list_entries():
        lists.append(f)
    page = random.choice(lists)
    return render(request, f"entrieshtml/{page}.html", {
        "title": page
    })


def edit(request):
    titles = request.POST.get('titles')
    content = request.POST.get('content')
    pretitle = request.GET.get('pretitle')
    if request.method == "GET":
        with open(f"entries/{pretitle}.md", 'r') as f:
            if f.mode == 'r':
                precontent = f.read()

    if request.method == "POST":
        with open(f'entries/{titles}.md', 'w') as f:
            f.write(content)

        filepath = os.path.join(
            'C:/Users/erfan/Desktop/Mozzie-atles/encyclopedia/templates/entrieshtml', f'{titles}.html')
        with open(filepath, 'w') as f:
            x = markdown(content)
            cheat = ["{% extends 'encyclopedia/layout.html' %}",
                     "{% block title %}", "{% endblock %}", "{% block body %}", p, p1]
            f.write(cheat[0])
            f.write(cheat[1])
            f.write(p1)
            f.write(cheat[2])
            f.write(cheat[3])
            f.write(x)
            f.write(p)
            f.write(cheat[2])

            """ for import layout.html in to the new file """
        return render(request, f"entrieshtml/{titles}.html", {
            "name": titles
        })
    return render(request, "encyclopedia/edit.html", {
        "precontent": precontent,
        "pretitle": pretitle
    })
