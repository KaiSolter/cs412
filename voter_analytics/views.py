# voter_analytics/views.py
# Kai Solter 2026-03-20
 
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

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
    
class GraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    #note this is reused from the voter search
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
        from django.db.models import Count
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

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

        context['birth_year_chart'] = self._generate_birth_year_histogram(queryset)
        context['party_chart'] = self._generate_party_pie_chart(queryset)
        context['election_chart'] = self._generate_election_histogram(queryset)

        return context

    def _generate_birth_year_histogram(self, queryset):
        """Histogram of voter distribution by year of birth."""
        # Exclude voters without birth dates
        voters_with_dates = queryset.exclude(DateOfBirth__isnull=True)
        year_counts = voters_with_dates.values('DateOfBirth__year').annotate(
            count=__import__('django.db.models', fromlist=['Count']).Count('id')
        ).order_by('DateOfBirth__year')
        
        years = [item['DateOfBirth__year'] for item in year_counts]
        counts = [item['count'] for item in year_counts]
        
        fig = go.Figure(data=[go.Bar(x=years, y=counts, marker=dict(color='rgb(65, 105, 225)'))])
        fig.update_layout(
            title=f'Voter distribution by Year of Birth (n={voters_with_dates.count()})',
            xaxis_title='Year of Birth',
            yaxis_title='Count',
            hovermode='x unified'
        )
        return fig.to_html(div_id='birth_year_chart', include_plotlyjs=False)

    def _generate_party_pie_chart(self, queryset):
        """Pie chart of voter distribution by party affiliation."""
        party_counts = queryset.values('PartyAffiliation').annotate(
            count=__import__('django.db.models', fromlist=['Count']).Count('id')
        ).exclude(PartyAffiliation='').order_by('-count')
        
        parties = [item['PartyAffiliation'] for item in party_counts]
        counts = [item['count'] for item in party_counts]
        
        fig = go.Figure(data=[go.Pie(labels=parties, values=counts)])
        fig.update_layout(title=f'Voter distribution by Party Affiliation (n={queryset.exclude(PartyAffiliation="").count()})')
        return fig.to_html(div_id='party_chart', include_plotlyjs=False)

    def _generate_election_histogram(self, queryset):
        """Histogram of voter participation in each election."""
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        counts = []
        for election in elections:
            count = queryset.filter(**{election: True}).count()
            counts.append(count)
        
        fig = go.Figure(data=[go.Bar(x=elections, y=counts, marker=dict(color='rgb(75, 0, 130)'))])
        fig.update_layout(
            title=f'Vote Count by Election (n={queryset.count()})',
            xaxis_title='Election',
            yaxis_title='Voters'
        )
        return fig.to_html(div_id='election_chart', include_plotlyjs=False)