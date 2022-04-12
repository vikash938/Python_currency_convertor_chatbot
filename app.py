from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':f"{amount} {source_currency} is {final_amount} {target_currency}"
    }
    return jsonify(response)
# Fetching data through the Currencyconverter API 
def fetch_conversion_factor(source,target):

    url = f"https://free.currconv.com/api/v7/convert?q={source}_{target}&compact=ultra&apiKey=febac1b8eeda64611df4"

    response = requests.get(url)
    response = response.json()

    return response[f'{source}_{target}']


if __name__ == "__main__":
    app.run(debug=True)