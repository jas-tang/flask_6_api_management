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

![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/flask1.JPG)

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

Running the function locally, I saw this image. 
![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/functionsup.JPG)

Thinking that it was working, I proceeded. 

Next, I created a new resource group. 
```
az group create --name AzureFunctionsQuickstart-rg --location eastus
```
I also created another storage account. 
```
az storage account create --name jasonflaskazure504 --location eastus --resource-group AzureFunctionsQuickstart-rg --sku Standard_LRS
```

I then created the function app in Azure
```
az functionapp create --resource-group AzureFunctionsQuickstart-rg --consumption-plan-location eastus --runtime python --runtime-version 3.9 --functions-version 4 --name flaskapp504 --os-type linux --storage-account jasonflaskazure504
```

Finally, I deployed my app on Azure
```
func azure functionapp publish flaskapp504
```

![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/igiveup2.JPG)

I was able to see my app on the "Function App" section of Azure.
![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/igiveup.JPG)

However, upon clicking on the app, it just brings up the same image as before. Changing the endpoint does not do anything either. This led me to beleive my function wasn't working.
So I went back and changed the function in Function_app.py to a test function provided by Microsoft.
```
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="HttpExample")
@app.route(route="hello")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("HttpExample function processed a request!")
```
However, upon running the function locally with func start, I saw the same message as before. 
![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/functionsup.JPG)
Changing the endpoints does nothing. 

This was where my attempt ended, despite being able to launch the app onto Azure. I am unsure as to which step went wrong. 

## OpenAPI with Swagger/Flasgger

I was able to build my function as an app, including Swagger.
```
def hello_get():
    """
    This is a test

    :param req: The HTTP request with the parameter "price".
    :type req: func.HttpRequest
    :return: The JSON response containing the tip percentages.
    :rtype: func.HttpResponse
    """
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


if __name__ == '__main__':
    app.run(debug=True)
```

However, when trying to run Flasgger, I was met with no functions. I searched online and found that I have no defined any operations or endpoints in the Swagger documentation.
To add operation definition, I had to use swag_from provided by flasgger to specify the input and the output of my parameters. 
```
@swag_from({
    'parameters': [
        {
            'name': 'price',
            'in': 'query',
            'type': 'number',
            'required': True,
            'description': 'The base price for calculating tip percentages.'
        }
    ],
    'responses': {
        200: {
            'description': 'Success',
            'schema': {
                'base_price': 'number',
                'fifteen_percent': 'number',
                'eighteen_percent': 'number',
                'twenty_percent': 'number',
                'twentyfive_percent': 'number'
            }
        }
    }
})
```

I was then able to run python swagger.py. I then changed the endpoint to anidocs so we could see the Swagger results.
![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/flasgger.JPG)
![](https://github.com/jas-tang/flask_6_api_management/blob/main/images/flasgger2.JPG)
