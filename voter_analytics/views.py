# voter_analytics/views.py
# Kai Solter 2026-03-20
 
from django.views.generic import ListView, DetailView
from .models import Voter

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all().order_by('LastName', 'FirstName')
        params = self.request.GET

        party = params.get('party', '')
        if party:
            queryset = queryset.filter(PartyAffiliation=party)

        min_year = params.get('min_year', '')
        if min_year:
            queryset = queryset.filter(DateOfBirth__year__gte=min_year)

        max_year = params.get('max_year', '')
        if max_year:
            queryset = queryset.filter(DateOfBirth__year__lte=max_year)

        voter_score = params.get('voter_score', '')
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for field_name in election_fields:
            if params.get(field_name):
                queryset = queryset.filter(**{field_name: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        years = [
            dt.year for dt in
            Voter.objects.exclude(DateOfBirth__isnull=True)
            .dates('DateOfBirth', 'year', order='ASC')
        ]
        parties = list(
            Voter.objects.exclude(PartyAffiliation='')
            .values_list('PartyAffiliation', flat=True)
            .distinct()
            .order_by('PartyAffiliation')
        )
        voter_scores = list(
            Voter.objects.exclude(voter_score__isnull=True)
            .values_list('voter_score', flat=True)
            .distinct()
            .order_by('voter_score')
        )

        context['years'] = years
        context['parties'] = parties
        context['voter_scores'] = voter_scores
        context['selected'] = {
            'party': self.request.GET.get('party', ''),
            'min_year': self.request.GET.get('min_year', ''),
            'max_year': self.request.GET.get('max_year', ''),
            'voter_score': self.request.GET.get('voter_score', ''),
            'v20state': self.request.GET.get('v20state', ''),
            'v21town': self.request.GET.get('v21town', ''),
            'v21primary': self.request.GET.get('v21primary', ''),
            'v22general': self.request.GET.get('v22general', ''),
            'v23town': self.request.GET.get('v23town', ''),
        }
        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'