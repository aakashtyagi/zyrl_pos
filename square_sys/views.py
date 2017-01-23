from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


# Your application's ID and secret, available from your application dashboard.
application_id = 'sq0idp-YfSO-wAkst7PEsfWwtrpfQ'
application_secret = 'sq0csp-XDBB_ErAVFKsy4oF-yNFR4eDlPOQKiB1XJSm_nqk5lg'

# Headers to provide to OAuth API endpoints
oauth_request_headers = { 'Authorization': 'Client ' + application_secret,
                          'Accept': 'application/json',
                          'Content-Type': 'application/json'}

def index(request):
