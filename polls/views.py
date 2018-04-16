from __future__ import unicode_literals
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from polls.forms import *
from django.forms.models import model_to_dict
import urllib.request
import json

key = "1234"

#def show_candidate_vote_count(request, ballot_id):
#    candidates = Candidate.objects.filter(ballot=ballot_id)
#    return render(request, 'view_candidates.html', {'candidates': candidates})

def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    return render(request, 'detail.html', {
        'election': election
    })

def show_confirmation_page(request, election_id):
    #ballot = get_object_or_404(Ballot, id=ballot_id)
    election = get_object_or_404(Election, id=election_id)
    ballots = election.ballot_set.all()
    
    #candidates = ""
    candidates = []
    count = 0
    candidate_ids = ""
    
    
    for ballot in ballots:
    
        try:
            
            candidate = ballot.candidate_set.get(pk=request.POST['candidate'+str(count)])
             
            
        except (KeyError, Candidate.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'election': election,
                'error_message': "You didn't select a choice.",
            })
        else:
            if count is not 0:
                candidate_ids += ","
            candidate_ids += str(candidate.id)
            candidates.append(candidate)
            count +=1
            
    return render(request, 'confirmation.html', {'election_id': election_id, 'candidates': candidates, "candidate_ids":candidate_ids})


def submit_vote(request, election_id):
    candidates = request.POST['candidates']
    candidates = candidates.split(",")
    for candidate_id in candidates:
        candidate = Candidate.objects.get(pk=int(candidate_id))
        candidate.number_of_votes = candidate.number_of_votes + 1
        candidate.save()
            
    return redirect("scan_qr", election_id=election_id)
            
    


def scan_qr(request, election_id):
    if request.method == 'POST':
        form = ScanQRForm(request.POST)
        if form.is_valid():
            # Build the participant fields
            qr_code = form.cleaned_data.get('qr_code')
            # Check to see if valid

            return redirect('vote', election_id=election_id)

            #return redirect('index')
        else: 
            return render(request, 'scan_qr.html', {
                'form': form,
                'message': "Please enter valid data!"
            })
    else:
        form = ScanQRForm()
        return render(request, 'scan_qr.html', {'form': form})
    
def verified_voter(request):
    return render(request, 'verified_voter.html')

def check_in(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CheckInForm(request.POST)
            if form.is_valid():
                # Build the participant fields
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                street_address = form.cleaned_data.get('street_address')
                city = form.cleaned_data.get('city')
                zip_code = form.cleaned_data.get('zip_code')

                
                # Replace with real url
                url = "http://www.people.virginia.edu/~mss2x/allvotersva.txt"
                with urllib.request.urlopen(url) as url:
                    #data now contains json
                    data = json.loads(url.read().decode())
                    
                    
                # Get the precinct ID of poll worker associated with user logged in     
                poll_worker = PollWorker.objects.get(user=request.user)
                print(poll_worker)
                
                ##Put try catch around this
                poll_worker_id = poll_worker.polling_location
                    
                # Temporary data to use
                temp_data = { 
    "status" : "200",
    "voters" : [
        {
            "voter_number" : "020342357",
            "voter_status" : "active",
            "date_registered" : "2007-08-20",
            "last_name" : "Garcia",
            "first_name" : "Juan",
            "street_address" : "123 Main Street",
            "city" : "Charlottesville",
            "state" : "VA",
            "zip" : "22902",
            "locality" : "ALBEMARLE COUNTY",
            "precinct" : "405-CALE",
            "precinct_id" : "0405"
        },
        {
            "voter_number" : "020342357",
            "voter_status" : "active",
            "date_registered" : "2007-08-20",
            "last_name" : "Voter2",
            "first_name" : "Voter1",
            "street_address" : "123 Main Street",
            "city" : "Charlottesville",
            "state" : "VA",
            "zip" : "22902",
            "locality" : "ALBEMARLE COUNTY",
            "precinct" : "405-CALE",
            "precinct_id" : "0405"
        },
        {
            "voter_number" : "020342357",
            "voter_status" : "active",
            "date_registered" : "2007-08-20",
            "last_name" : "Garcidsda",
            "first_name" : "Juanlosa",
            "street_address" : "123 Main Street",
            "city" : "Charlottesville",
            "state" : "VA",
            "zip" : "22902",
            "locality" : "ALBEMARLE COUNTY",
            "precinct" : "405-CALE",
            "precinct_id" : "0409"
        },
        {
            "voter_number" : "020342357",
            "voter_status" : "active",
            "date_registered" : "2007-08-20",
            "last_name" : "Garciawr",
            "first_name" : "Juangf",
            "street_address" : "123 Main Street",
            "city" : "Charlottesville",
            "state" : "VA",
            "zip" : "22902",
            "locality" : "ALBEMARLE COUNTY",
            "precinct" : "405-CALE",
            "precinct_id" : "0411"
        },
        {
            "voter_number" : "020342357",
            "voter_status" : "active",
            "date_registered" : "2007-08-20",
            "last_name" : "Garciarwe",
            "first_name" : "Juancdsds",
            "street_address" : "123 Main Street",
            "city" : "Charlottesville",
            "state" : "VA",
            "zip" : "22902",
            "locality" : "ALBEMARLE COUNTY",
            "precinct" : "405-CALE",
            "precinct_id" : "0415"
            
        }
    ]
}
                #query voter database with "begins with"
                voter_exists = False
                for voter in data['voters']:
                    if voter["first_name"] == first_name and voter["last_name"] == last_name and voter["street_address"] == street_address and voter["city"] == city and voter["zip"] == zip_code:
                        print("good")
                    #   :
                        if voter["precinct_id"] == poll_worker_id:
                            voter_exists = True
                            #The voter is at the right place
                            print("Voter is verified")
                            #Print voters receipt 
                            # Return to 
                            return redirect('verified_voter')
                        else: 
                            # Voter is registered but is at the wrong precinct
                            # Return to check-in page
                            return render(request, 'check_in.html', {
                                'form': form,
                                'message': "Voter is in the wrong precinct!"
                                    })
                
                
                # The voter is not registered, throw error and don't print
                return render(request, 'check_in.html', {
                    'form': form,
                    'message': "Voter is not registered!"
                })

                
            else:
                return render(request, 'check_in.html', {
                    'form': form,
                    'message': "Please enter valid data!"
                })
        else:
            form = CheckInForm
            return render(request, 'check_in.html', {'form': form})
    else:
        return redirect('index')
    
    

def index(request):
    # return HttpResponse("Welcome to the voting application! <a href='/scan_qr/2018-11'> QR Code </a>")
    return render(request, 'index.html')

######################
#APIs 

def get_elections(request):
    if request.method != "GET":
        return JsonResponse({'error': 'Should be a GET request'}, safe=False)
    data = Election.objects.all()
    elections = [obj.as_json() for obj in data]
    return JsonResponse({'elections': elections}, safe=False)

def get_voters_for_polling_site(request, PRECINCT_ID):
    if request.method != "GET":
        return JsonResponse({'error': 'Should be a GET request'}, safe=False)
    API_KEY = request.GET.get('key', '')
    if API_KEY != key:
        return JsonResponse({'status': '404', 'status_message': 'Invalid API Key Provided'}, safe=False)
    data = Voter.objects.filter(precinct_id=PRECINCT_ID)
    voters = [obj.as_json() for obj in data]
    return JsonResponse({'status':'200','voters': voters}, safe=False)


def get_voter(request, voter_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        voter_object = Voter.objects.get(id=voter_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"Voter not found"}), status=404)
    user_json = json.dumps(model_to_dict(voter_object))
    return HttpResponse(user_json, status=200)


def get_voters(request):
    if request.method != "GET":
        return JsonResponse({'error': 'Should be a GET request'}, safe=False)
    API_KEY = request.GET.get('key', '')
    if API_KEY != key:
        return JsonResponse({'status': '404', 'status_message': 'Invalid API Key Provided'}, safe=False)
    data = Voter.objects.all()
    voters = [obj.as_json() for obj in data]
    return JsonResponse({'status':'200','voters': voters}, safe=False)


def get_election(request, election_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        election_object = Election.objects.get(id=election_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"Election not found"}), status=404)
    return_list = []
    return_list.append(model_to_dict(election_object))
    try:
        candidate_object = Candidate.objects.get(id=election_id)
        for candidate in candidate_object:
            return_list.append(model_to_dict(candidate))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"Candidate not found"}), status=404)
    return HttpResponse(json.dumps(return_list), status = 200)