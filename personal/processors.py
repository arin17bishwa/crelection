from django.conf import settings
from account.models import Candidate
def Candidature(request):
    kwargs={}
    candidates=Candidate.objects.all()
    kwargs['candidates']=candidates
    return kwargs
