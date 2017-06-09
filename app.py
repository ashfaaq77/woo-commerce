from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response
from woocommerce import API

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#need to change this one
def processRequest(req):

	
    if req.get("result").get("action") != "retrieveProduct":
        return {}
	
    data = makeJson(req)
    res = makeWebhookResult(data)
    return res


def makeJson(req):
	result = req.get("result")
	parameters = result.get("parameters")
	goods = parameters.get("goods")
	
	if goods is None:
		return{}
		
	wcapi = API(
	url = "https://dev.i-spy360.mu/woocommerce-chatbot/",
	consumer_key = "ck_b1d5aede2d327d994f3abac95945de0d3881fd9e",
	consumer_secret = "cs_980d7219d925bbd2ed75faafbd74ec59695153ed",
	wp_api = True,
	version = "wc/v2"
	)
		
	data = wcapi.get("products/3719").json()   
	
	return data
	
def makeWebhookResult(data):
    name = data.get("name")
    if name is None:
        return {}

    permalink = data.get("permalink")
    if permalink is None:
        return {}

    price = data.get("price")
    if price is None:
        return {}
	
	stock = data.get("in_stock")
	if price is None:
		return {}
	

	speech = "We have " + name + " \nThe link to it is " + permalink + " \nThe price is " + price + " \nWe have stock"
	
	
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-woocommerce"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
