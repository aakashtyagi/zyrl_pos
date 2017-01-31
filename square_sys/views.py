from django.shortcuts import render
from django.http import HttpResponse
import requests, json, httplib
from .models import SquareCustomer
import datetime
from datetime import datetime
# Create your views here.


# Your application's ID and secret, available from your application dashboard.
application_id = 'sq0idp-YfSO-wAkst7PEsfWwtrpfQ'
application_secret = 'sq0csp-XDBB_ErAVFKsy4oF-yNFR4eDlPOQKiB1XJSm_nqk5lg'

# Headers to provide to OAuth API endpoints
oauth_request_headers = { 'Authorization': 'Client ' + application_secret,
                          'Accept': 'application/json',
                          'Content-Type': 'application/json'}

def adminIndex(request):
  customers = SquareCustomer.objects.all()
  context_dict = {}
  context_dict['customers'] = customers
  return render(request, "zyrl-admin.html", context_dict)

def customer_details(request, uid):
  try:
    customer = SquareCustomer.objects.get(id=uid)
  except Exception, e:
    return HttpResponse("Shit. Try re-loading the page.")

  if customer:
    r = requests.get("https://connect.squareup.com/v1/"+customer.location+"/payments?order=DESC", headers={'Authorization': 'Bearer ' + customer.access_token,
                   'Accept': 'application/json',
                   'Content-Type': 'application/json'})

    zyrl_sales_count = 0
    zyrl_sales_dollars = 0
    date = []
    total_money = []
    zyrl_money = []

    if r.status_code == 200:
      for data in r.json():
        
        items = data['itemizations']
        print "==============================================================="
        print data['created_at']
        date.append(data['created_at'])
        print float(data['tender'][0]['total_money']['amount'])/100
        total_money.append(float(data['tender'][0]['total_money']['amount'])/100)
        for item in items:
          if "zyrl" in item['name'].lower():
            print item['name'], item['quantity'], item['total_money']['amount']
            zyrl_sales_count += 1
            zyrl_sales_dollars += item['total_money']['amount']
            # zyrl_money.append(item['name'])
          else:
            # zyrl_money.append("not a zyrl sale")
            pass
        # print "============================"
        print "Total ZYRL Count and Sales: ", zyrl_sales_count, zyrl_sales_dollars
    else:
      return HttpResponse("shit.")
  context_dict = {}
  context_dict['date'] = date
  context_dict['total_money'] = total_money
  context_dict['zyrl_money'] = zyrl_money
  return render(request, "info.html", context_dict)
  # return HttpResponse("it works!")


def index(request):
	url = '''<a href="https://connect.squareup.com/oauth2/authorize?client_id={0}">Click here</a> to authorize the application.'''.format(application_id)
	return HttpResponse(url)


def callback(request):

  authorization_code = request.GET['code']
  print authorization_code

	# Extract the returned authorization code from the URL
  # authorization_code = request.query.get('code')
  if authorization_code:

    # Provide the code in a request to the Obtain Token endpoint
    oauth_request_body = {
      'client_id': application_id,
      'client_secret': application_secret,
      'code': authorization_code,
      'scope': 'MERCHANT_PROFILE_READ PAYMENTS_READ SETTLEMENTS_READ ORDERS_READ'
    }

    # r = requests.post("https://connect.squareup.com/oauth2/token", data=[oauth_request_headers, oauth_request_body])
    # print r.json()
    # print r.text

    connection = httplib.HTTPSConnection('connect.squareup.com')
    connection.request('POST', '/oauth2/token', json.dumps(oauth_request_body), oauth_request_headers)

    # Extract the returned access token from the response body
    oauth_response_body = json.loads(connection.getresponse().read())
    if oauth_response_body['access_token']:

      # Here, instead of printing the access token, your application server should store it securely
      # and use it in subsequent requests to the Connect API on behalf of the merchant.
      # print 'Access token: ' + oauth_response_body['access_token']
      access_token = oauth_response_body['access_token']
      # print 'Expires at: ' + oauth_response_body['expires_at']
      expiry_date = oauth_response_body['expires_at']
      expiry_date = expiry_date.split('T')[0]
      expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')

      r = requests.get("https://connect.squareup.com/v1/me/locations", headers={'Authorization': 'Bearer ' + oauth_response_body['access_token'],
                          'Accept': 'application/json',})
      # print r.json()
      if r.status_code == 200:
        for data in r.json():
          # print "Location: " + data['id']
          location = data['id']
          # print "Name: " + data['business_name']
          name = data['business_name']
          try:
            customer = SquareCustomer.objects.get(location=location)
            print "customer already exists, bitch."
          except Exception, e:
            SquareCustomer.objects.create(name=name, location=location, access_token=access_token, expiry_date=expiry_date.date())
          
      else:
        return HttpResponse("Something went wrong. Try again.")


      return HttpResponse('Authorization succeeded!')

    # The response from the Obtain Token endpoint did not include an access token. Something went wrong.
    else:
      return HttpResponse('Code exchange failed!')

  # The request to the Redirect URL did not include an authorization code. Something went wrong.
  else:
    return HttpResponse('Authorization failed!')