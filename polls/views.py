from typing import Any
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (Not including those
        set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice",
            },
            )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after 
        # succesfully dealing with POST data.
        # This prevents data from being posted twice if a
        # user hits the back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


"""
The render()
function takes the request object as its first argument,
a template name as its second argument and
a dictionary as its optional third argument.

It returns an HttpResponse object
of the given template rendered with the given context.
"""

"""
get_object_or_404()
Parameters
model: Takes a Django model (Class)
**kwargs (keyword arguments): Specifi which model are you looking for.

Return Value:
Object Found: If the function successfully finds the object you're looking for based on the provided details, it returns that object. This means you get the actual piece of fruit (or whatever you were looking for) that matches your criteria.
Object Not Found: If the function can't find the object you're looking for, it doesn't return an empty result. Instead, it raises an error. This error is a special kind of error that says "404 Not Found." In programming, a "404" error usually means that the thing you were looking for (in this case, the object) couldn't be found. This is similar to the "Sorry, couldn't find that fruit!" response we talked about earlier.
"""

