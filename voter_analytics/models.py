# File: voter_analytics/models.py
# Author: Kai Solter (ksolter@bu.edu), 3/20/2026 
# Description: Models for voter_analytics app 
import csv
import datetime

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Voter(models.Model):
    '''
    Voter Model
    '''
    FirstName = models.TextField(blank=True)
    LastName = models.TextField(blank=True)
    StreetNumber = models.IntegerField(blank=True)
    StreetName = models.TextField(blank=True)
    AppartmentNumber = models.CharField(max_length=20, blank=True)
    ZipCode = models.TextField(blank=True)
    DateOfBirth = models.DateField(blank=True, null=True)
    DateOfRegistration = models.DateField(blank=True, null=True)
    PartyAffiliation = models.CharField(max_length=2, blank=True)
    PrecinctNumber = models.CharField(max_length=10, blank=True)

    v20state = models.BooleanField(blank=True, null=True)
    v21town = models.BooleanField(blank=True, null=True)
    v21primary = models.BooleanField(blank=True, null=True)
    v22general = models.BooleanField(blank=True, null=True)
    v23town = models.BooleanField(blank=True, null=True)
    voter_score = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        '''
        Docstring for __str__
        :param self: Description
        '''
        return f'{self.FirstName} {self.LastName} in Precinct {self.PrecinctNumber}. Voter Score: {self.voter_score}'
    
    def load_data():
        '''Load data from the Newton voter CSV file into the database.'''
        filename='C:/Users/kaiso/OneDrive/Desktop/newton_voters.csv'
        
        #helpers to parse the CSV
        def parse_int(value):
            value = (value or '').strip()
            return int(value) if value else None

        def parse_bool(value):
            value = (value or '').strip().lower()
            if value in ('1', 'true', 't', 'yes', 'y'):
                return True
            if value in ('0', 'false', 'f', 'no', 'n'):
                return False
            return None

        def parse_date(value):
            value = (value or '').strip()
            if not value:
                return None
            try:
                return datetime.date.fromisoformat(value)
            except ValueError:
                return None

        #process the CSV
        with open(filename, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                voter = Voter(
                    FirstName=(row.get('First Name') or '').strip(),
                    LastName=(row.get('Last Name') or '').strip(),
                    StreetNumber=parse_int(row.get('Residential Address - Street Number')),
                    StreetName=(row.get('Residential Address - Street Name') or '').strip(),
                    AppartmentNumber=(row.get('Residential Address - Apartment Number') or '').strip(),
                    ZipCode=(row.get('Residential Address - Zip Code') or '').strip(),
                    DateOfBirth=parse_date(row.get('Date of Birth')),
                    DateOfRegistration=parse_date(row.get('Date of Registration')),
                    PartyAffiliation=(row.get('Party Affiliation') or '').strip()[:2],
                    PrecinctNumber=(row.get('Precinct Number') or '').strip(),
                    v20state=parse_bool(row.get('v20state')),
                    v21town=parse_bool(row.get('v21town')),
                    v21primary=parse_bool(row.get('v21primary')),
                    v22general=parse_bool(row.get('v22general')),
                    v23town=parse_bool(row.get('v23town')),
                    voter_score=parse_int(row.get('voter_score')),
                )
                voter.save()