# groovehook

Groovehook is a small webapp built in flask that allows you to pull recent customer information from your Shopify store and render it alongside customer tickets.

## Requirements
A Shopify Store and a Groove (https://groovehq.com/) ticketing system

You'll need an API Key and Password from Shopify as well

## Environmental Variables
There are 4 required environmental variables to set

  * SHOPIFY_STORE - *the url base of your shopify store (URL.myshopify.com)*
  * SHOPIFY_API_KEY
  * SHOPIFY_API_PASS
  * GROOVE_API_TOKEN - *you can find this on the Custom Profile App page of your Groove instance (/groove_client/apps/custom-profile)*

## Setup
  * Clone the repo and deploy to a new Heroku instance (or the host of your choice)
  * Add Shopify store information, API Auth, and Groove API auth information to environmental Variables
  * Configure your Groove Custom Profile App (there is a suggested Template in [groove_template.liquid](groove_template.liquid))
  * Enjoy!
