from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, User
# from django.contrib.sessions import
from django.contrib.auth import authenticate  # , login


# from django.template.loader import render_to_string


class LoginView(generic.ListView):
    model = User
    template_name = 'polls/login.html'


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class HistoryView(generic.ListView):
    model = Question
    template_name = 'polls/history.html'


def login(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=uname, password=pwd)
    if user is not None:
        return HttpResponse('ok')
    else:
        return HttpResponse('Wrong Credentials')


def register(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=uname, password=pwd)
    if user is None:
        ur = User(username=uname)
        ur.set_password(pwd)
        ur.save()
        return HttpResponse('registered')
    else:
        return HttpResponse('User exists!')


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        if request.is_ajax():
            return HttpResponse('You didn\'t select a choice.')
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        tf = False
        squests = request.session.get("squests")
        if squests is None:
            squests = [{
                "Question": question.question_text,
                "Choice": selected_choice.choice_text,
                "Votes": 0
            }]
            request.session["squests"] = squests

        for i in squests:
            if i["Choice"] == selected_choice.choice_text:
                i["Votes"] += 1
                tf = True

        if tf is False:
            newquest = {"Question": question.question_text,
                        "Choice": selected_choice.choice_text,
                        "Votes": 1
                        }
            squests.append(newquest)
        request.session["squests"] = squests

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def serverhistory(request):
    return render(request, 'polls/serverhistory.html')
