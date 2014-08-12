from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
#from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Choice, Poll

#generic
class IndexView(generic.ListView):
    template_name = 'polls/index.html' #not self, global??
    context_object_name = 'latest_poll_list' # to override autogen var: poll_list

    def get_queryset(self):
        '''return the last five published polls. not including future'''
        return Poll.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]
        #return Poll.objects.order_by('-pub_date')[:5]
            
class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        '''do not return future polls'''
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

#def index(request):
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #context = {'latest_poll_list':latest_poll_list}
    #return render(request, 'polls/index.html', context)

#def index(request):
    ##return HttpResponse('hello, world! you are at the poll index')
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, {
        #'latest_poll_list':latest_poll_list,
        #})
    ##output = ', '.join([p.question for p in latest_poll_list])
    #return HttpResponse(template.render(context))

#def detail(request, poll_id):
    ##try:
        ##poll = Poll.objects.get(pk=poll_id)
    ##except Poll.DoesNotExist:
        ##raise Http404
    #poll = get_object_or_404(Poll, pk=poll_id)
    #return render(request, 'polls/detail.html', {'poll':poll})



#def results(request, poll_id):
    ##return HttpResponse('you are looking at the results of poll %s' % poll_id)
    #poll = get_object_or_404(Poll, pk=poll_id)
    #return render(request, 'polls/results.html', {'poll':poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try: 
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html',
                {'poll': p,
                'error_message': 'you did not select a choice.',})
    else:
        selected_choice.votes += 1
        selected_choice.save()
 #avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

    #return HttpResponse('you are voting on poll %s' % poll_id)
