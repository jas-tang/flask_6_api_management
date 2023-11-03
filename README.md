# flask_6_api_management
This is a repository for Assignment 6 in HHA504, API Development. 

## Flask-based RESTful API:

My flask app takes an input of a price and calculates the tip percentage and adds it back to the originial amount. The percentages are 10%, 15%, 18% and 20%. 

```
from flask import escape
import functions_framework
import json
import pandas as pd 

@functions_framework.http
def hello_http(request):

    # price, this will be the base price
    # idea: we will calculate the tip percentage based on a base price


    request_args = request.args

    if request_args and "price" in request_args:
        base_price = request_args["price"]
    else:
        base_price = 0


    # Step 1 convert everything to numbers 
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
```

It uses the functions framework to create an HTML function. The requested argument is set to 'price'. We created and if else statement so that if there isn't an argument, the base price will remain 0. 
We then specified the function itself, then returned the result in a json format. 

Run this in the terminal to run the application. 
```
functions-framework-python --target hello_http --debug
```

![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/flasgger.JPG)

This error occurred when I tried to input a decimal in the requested argument. As you know, money comes with cents, so that is why I changed the code to accomodate floats.

![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/flask1error.JPG)

This was the result after inputting 87.63 as the requested argument. 
![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/flask1pricefloatfix.JPG)

## Azure API deployment (attempt) 

I struggled to get any function to work while trying to deploy it on Azure. Nonetheless, these are the steps I took. 

First, I installed Azure CLI with the following. 
```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
Then I logged in with the following.
```
az login --use-device-code
```
I also ran this following. 
```
sudo apt-get install azure-functions-core-tools-4
```
Then I ran the func init command to create a functions project named LocalFunctionProj to create a test app. Within the LocalFunctionProj folder, there is a function_app.py which should hold the function to my app. 
I placed my function in there. Next, I opened the local.settings.json project file to see if AzureWebJobsFeatureFlags has the value of EnableWorkerIndexing. 
I then updates the AzureWebJobsStorage to the following setting: 
```
"AzureWebJobsStorage": "UseDevelopmentStorage=true",
```

Runnig th

