import azure.functions as func
import json

app = func.FunctionApp()
@app.function_name(name="testapp")
@app.route(route='hello')

def test_function(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the query parameter "price" from the HTTP request
        price = req.params.get('price')
        if price is None:
            return func.HttpResponse("Please provide a 'price' parameter in the query string.", status_code=400)

        # Convert the price to a float
        price_num = float(price)

        # Calculate tip percentages
        fifteen_percent = price_num * 0.15
        eighteen_percent = price_num * 0.18
        twenty_percent = price_num * 0.20
        twentyfive_percent = price_num * 0.25

        # Create a JSON response
        response = {
            "base_price": price_num,
            "fifteen_percent": fifteen_percent,
            "eighteen_percent": eighteen_percent,
            "twenty_percent": twenty_percent,
            "twentyfive_percent": twentyfive_percent
        }

        return func.HttpResponse(json.dumps(response), mimetype="application/json")
    except ValueError:
        return func.HttpResponse("Invalid 'price' parameter. Please provide a valid number.")

