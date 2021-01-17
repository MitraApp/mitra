
class PlaidConfig:
    # Get your Plaid API keys from the dashboard: https://dashboard.plaid.com/account/keys
    PLAID_CLIENT_ID="5fea42cd354a870014624131" 
    PLAID_SECRET="22e2c6eb9bc22466c8364ef6a00c1f" #sandbox
    #PLAID_SECRET=c72a5b4a825276f8c9915379a9e391 #dev
    # Use 'sandbox' to test with fake credentials in Plaid's Sandbox environment
    # Use 'development' to test with real credentials while developing
    # Use 'production' to go live with real users
    PLAID_ENV="sandbox"
    # PLAID_PRODUCTS is a comma-separated list of products to use when
    # initializing Link, e.g. PLAID_PRODUCTS=auth,transactions.
    # see https://plaid.com/docs/api/tokens/#create-a-link_token for a complete list
    PLAID_PRODUCTS=["transactions"]
    # PLAID_COUNTRY_CODES is a comma-separated list of countries to use when
    # initializing Link, e.g. PLAID_COUNTRY_CODES=US,CA.
    # see https://plaid.com/docs/api/tokens/#create-a-link_token for a complete list
    PLAID_COUNTRY_CODES=["US"]
    # Only required for Oauth:
    # Set PLAID_REDIRECT_URI to 'http://localhost:8000/oauth-response.html'
    # The OAuth redirect flow requires an endpoint on the developer's website
    # that the bank website should redirect to. You will need to configure
    # this redirect URI for your client ID through the Plaid developer dashboard
    # at https://dashboard.plaid.com/team/api.
    PLAID_REDIRECT_URI=""
