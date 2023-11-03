import json
from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__)
Swagger(app)

@app.route('/hello', methods=['GET'])

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