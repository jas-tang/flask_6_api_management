from flask import escape
import functions_framework
import json
import pandas as pd 
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def hello_http(request):

    # price, this will be the base price
    # idea: we will calculate the tip percentage based on a base price


    request_args = request.args

    if request_args and "price" in request_args:
        base_price = request_args["price"]
    else:
        base_price = 0


    # Step 1 convert everything to float 
    price_num = float(base_price)


    # Step 2 we now some them all together 
    fifteen_percent = (price_num * .15) + price_num
    eighteen_percent = (price_num * .18) + price_num
    twenty_percent = (price_num * .2) + price_num
    twentyfive_percent = (price_num * .25) + price_num

    # Step 3 create a json object to return to the user 
    output = json.dumps(
        {
            "base_price" : base_price, 
            "fifteen_percent": fifteen_percent, 
            "eighteen_percent": eighteen_percent, 
            "twenty_percent": twenty_percent, 
            "twentyfive_percent": twentyfive_percent            

        }
    )

    return output

# to run app
# functions-framework-python --target hello_http --debug

#az functionapp create --resource-group Jason504 --consumption-plan-location eastus --runtime python --runtime-version 3.9 --functions-version 4 --name costpercentapp --storage-account jason504storage