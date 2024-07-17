from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from utils.functional import transaction_history_graph


def index(request: HttpRequest):
    context = {}

    if request.user.is_anonymous:
        return render(request, "index.html")

    return render(request, "landing.html", context)


@login_required
def view_graph(request: HttpRequest):
    context = {"graph": None, "error_message": None}

    if request.GET.get("address"):
        transaction_graph = transaction_history_graph(request.GET.get("address"))
        context["graph"] = transaction_graph[0]
        context["error_message"] = transaction_graph[1]

    return render(request, "view-graph.html", context)
