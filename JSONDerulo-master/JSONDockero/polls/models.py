# Create your models here.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Election(models.Model):
    type = models.CharField(max_length = 20)
    id = models.CharField(max_length =10, primary_key=True)
        
    def __str__(self):
        return self.type

    def as_json(self):
        return dict(
            id = self.id,
            type = self.type)

class Ballot(models.Model):
    question_text = models.CharField(max_length=200, default="Default question")
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question_text

class Candidate(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    party = models.CharField(max_length=20)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    number_of_votes = models.IntegerField()
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Voter(models.Model):
    voter_number = models.CharField(max_length=50)
    voter_status = models.CharField(max_length=50)
    date_registered = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=10)
    zip = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    precinct = models.CharField(max_length=20)
    precinct_id = models.CharField(max_length=20)
    def __str__(self):
        return self.first_name + " " + self.last_name
    def as_json(self):
        return dict(
            voter_number = self.voter_number,
            voter_status = self.voter_status,
            date_registered = self.date_registered,
            last_name = self.last_name,
            first_name = self.first_name,
            street_address = self.street_address,
            city = self.city,
            state = self.state,
            zip = self.zip,
            locality = self.locality,
            precinct = self.precinct,
            precinct_id = self.precinct_id)

class Vote(models.Model):
	date = models.DateTimeField('date voted')
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
	voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
	vote_id = models.AutoField(primary_key=True)
	def __str__(self):
		return str(self.vote_id)

class PollWorker(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	polling_location = models.CharField(max_length=100)