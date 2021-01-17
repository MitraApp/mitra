import plaid 
import json
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from plaid_config import PlaidConfig

plaid_conf = PlaidConfig()

client = plaid.Client(client_id=plaid_conf.PLAID_CLIENT_ID,
                      secret=plaid_conf.PLAID_SECRET,
                      environment=plaid_conf.PLAID_ENV)

@login_required
def index(request):
    return render(request, 'financials/financials.html', {})

def info(request):
  access_token = request.user.plaidkey.access_token
  item_id = request.user.plaidkey.item_id
  
  return JsonResponse({
    'item_id': item_id,
    'access_token': access_token,
    'products': plaid_conf.PLAID_PRODUCTS
  })

# Retrieve ACH or ETF account numbers for an Item
# https://plaid.com/docs/#auth
def get_auth(request):
  access_token = request.user.plaidkey.access_token
  try:
    auth_response = client.Auth.get(access_token)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
  #pretty_print_response(auth_response)
  return JsonResponse(auth_response)

# Retrieve Transactions for an Item
# https://plaid.com/docs/#transactions
def get_transactions(request):
  access_token = request.user.plaidkey.access_token  
  
  # Pull transactions for the last 30 days
  start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
  end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
  try:
    transactions_response = client.Transactions.get(access_token, start_date, end_date)
  except plaid.errors.PlaidError as e:
    return JsonResponse(format_error(e))
  
  #pretty_print_response(transactions_response)
  return JsonResponse(transactions_response)

# Retrieve Identity data for an Item
# https://plaid.com/docs/#identity
def get_identity(request):
  access_token = request.user.plaidkey.access_token  
  try:
    identity_response = client.Identity.get(access_token)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
  
  #pretty_print_response(identity_response)
  return JsonResponse({'error': None, 'identity': identity_response['accounts']})

# Retrieve real-time balance data for each of an Item's accounts
# https://plaid.com/docs/#balance
def get_balance(request):
  access_token = request.user.plaidkey.access_token  
  
  try:
    balance_response = client.Accounts.balance.get(access_token)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
  
  #pretty_print_response(balance_response)
  return JsonResponse(balance_response)

# Retrieve an Item's accounts
# https://plaid.com/docs/#accounts
def get_accounts(request):
  access_token = request.user.plaidkey.access_token  

  try:
    accounts_response = client.Accounts.get(access_token)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
  
  #pretty_print_response(accounts_response)
  return JsonResponse(accounts_response)

# Create and then retrieve an Asset Report for one or more Items. Note that an
# Asset Report can contain up to 100 items, but for simplicity we're only
# including one Item here.
# https://plaid.com/docs/#assets
def get_assets(request):
  access_token = request.user.plaidkey.access_token  

  try:
    asset_report_create_response = client.AssetReport.create([access_token], 10)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
  #pretty_print_response(asset_report_create_response)

  asset_report_token = asset_report_create_response['asset_report_token']

  # Poll for the completion of the Asset Report.
  num_retries_remaining = 20
  asset_report_json = None
  while num_retries_remaining > 0:
    try:
      asset_report_get_response = client.AssetReport.get(asset_report_token)
      asset_report_json = asset_report_get_response['report']
      break
    except plaid.errors.PlaidError as e:
      if e.code == 'PRODUCT_NOT_READY':
        num_retries_remaining -= 1
        time.sleep(1)
        continue
      return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })

  if asset_report_json == None:
    return JsonResponse({'error': {'display_message': 'Timed out when polling for Asset Report', 'error_code': '', 'error_type': '' } })

  asset_report_pdf = None
  try:
    asset_report_pdf = client.AssetReport.get_pdf(asset_report_token)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })

  return JsonResponse({
    'error': None,
    'json': asset_report_json,
    'pdf': base64.b64encode(asset_report_pdf).decode('utf-8'),
  })

# Retrieve investment holdings data for an Item
# https://plaid.com/docs/#investments
def get_holdings(request):
  access_token = request.user.plaidkey.access_token  

  try:
    holdings_response = client.Holdings.get(access_token)
  except plaid.errors.PlaidError as e:
    return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
  
  #pretty_print_response(holdings_response)
  return JsonResponse({'error': None, 'holdings': holdings_response})

# Retrieve Investment Transactions for an Item
# https://plaid.com/docs/#investments
def get_investment_transactions(request):
  access_token = request.user.plaidkey.access_token  

  # Pull transactions for the last 30 days
  start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
  end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
  try:
    investment_transactions_response = client.InvestmentTransactions.get(access_token,
                                                                         start_date,
                                                                         end_date)
  except plaid.errors.PlaidError as e:
    return JsonResponse(format_error(e))
  
  #pretty_print_response(investment_transactions_response)
  return JsonResponse({'error': None, 'investment_transactions': investment_transactions_response})

# # This functionality is only relevant for the UK Payment Initiation product.
# # Retrieve Payment for a specified Payment ID
# @app.route('/api/payment', methods=['GET'])
# def payment():
#   global payment_id
#   payment_get_response = client.PaymentInitiation.get_payment(payment_id)
#   pretty_print_response(payment_get_response)
#   return JsonResponse({'error': None, 'payment': payment_get_response})

# Retrieve high-level information about an Item
# https://plaid.com/docs/#retrieve-item
def item(request):
  access_token = request.user.plaidkey.access_token  

  item_response = client.Item.get(access_token)
  institution_response = client.Institutions.get_by_id(item_response['item']['institution_id'])
  #pretty_print_response(item_response)
  #pretty_print_response(institution_response)
  return JsonResponse({'error': None, 'item': item_response['item'], 'institution': institution_response['institution']})

def pretty_print_response(response):
  print(json.dumps(response, indent=2, sort_keys=True))

