from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from polls.models import Poll, Choice

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'polls/index.html'
        context_object_name = 'latest_poll_list'
        def get_queryset(self):
            return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Poll

class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Poll

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
            selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))