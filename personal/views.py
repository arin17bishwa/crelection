from operator import attrgetter
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from account.models import User,Candidate


def home_view(request):
    context={}
    user=request.user
    if not request.user.is_authenticated:return redirect('account:must_authenticate')
    if user.voted:return redirect('personal:results')
    context['message'] = 'HELLO EVERYONE'
    if request.POST:
        data=request.POST
        #print(data['sold'])
        voted_for=data.get('sold')
        candidate=get_object_or_404(Candidate,registration_no=voted_for)
        user.voted=True
        candidate.voter=user
        candidate.votes+=1
        user.save()
        candidate.save()
        return redirect('personal:results')

    return render(request, 'personal/home.html', context=context)

def results_view(request):
    context = {}
    context['message'] = 'WELCOME EVERYONE'
    candidates=Candidate.objects.all()
    total_votes=sum(map(lambda x: x.get('votes'),list(candidates.values('votes'))))
    #print(total_votes)
    context['candidates']=candidates
    context['total_votes']=total_votes
    return render(request, 'personal/welcome.html', context=context)
