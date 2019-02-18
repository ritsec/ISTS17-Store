# API Calls
All the API endpoints that are in the application

# Backend
## `/dosh-get-balance`, methods=['POST']
Route for white team APIs to get balance of other teams

## `/dosh-add-credits`, methods=['POST']
Route for white team to add credits to a specific team

## `/dosh-remove-credits`, methods=['POST']
Route for white team to remove credits to a specific team

## `/dosh-set-credits`, methods=['POST']
Route for white team to set credits for a team

## `/get-balance`, methods=['POST']
Gets the balance of a team

## `/buy`, methods=['POST']
Buys a item from the white team store

## `/transactions`, methods=['POST']
Get a list of transactions made by the team

## `/transfer`, methods=['POST']
Transfer money from one teams account to another

## `/items`, methods=['POST']
Items and their price from the white team store

# Frontend
## `/static/js/<path:path>`
Serve our js files`

## `/static/css/<path:path>`
Serve our css files`

## `/assets/<path:path>`
Serve our css files`

## `/`, methods=['GET']
Main page, redirect to login if theres no authenticated session,

## `/search`, methods=['POST']
Allows users to filter the items by certain key words

## `/login`, methods=['GET`, 'POST']
Tries to log into backend API

## `/logout`, methods=['GET']
Log our user out, expire session in backend`

## `/update-password`, methods=['GET`, 'POST']
Update the users password

## `/shop`, methods=['GET`, 'POST']
List of items able to be boughten from the white team store

## `/account`, methods=['GET']
Get the info for a teams account, the balance, transactions etc.`

## `/transfer`, methods=['GET`, 'POST']
Transfer money from one teams account to another
