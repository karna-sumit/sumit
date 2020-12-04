import json
import logging
import os
from flask import Flask, request, make_response

app = Flask(__name__)


# Returns the products with at least one unit available

@app.route('/', methods=['GET'])
def get_all_products():
    available_products = []
    for product in get_products():
        if(check_availabilty(product, 1)):
            available_products.append(product)
    return json.dumps(available_products)


# Checks availability and updates inventory

@app.route('/buy', methods=['POST'])
def buy_product():
    if "-1" not in request.form.get('product', "-1"):
        product_id = int(request.form.get('product'))
        if "-1" not in request.form.get('quantity', "-1"):
            quantity = int(request.form.get('quantity'))
            if not quantity > 0:
                error_msg = "Invalid quantity {}".format(quantity)
                return error_msg
            product = get_product(product_id)
            if product is not None:
                if check_availabilty(product, quantity):
                    update_inventory(product, quantity)
                    return make_response('OK', 200, {'content_type': 'application/json'})
                else:
                    error_msg = " Not enough inventory "
                    logging.error(error_msg)
                    return error_msg
            else:
                error_msg = " Product not found "
                logging.error(error_msg)
                return error_msg
        else:
            error_msg = " Bad request missing quantity "
            logging.error(error_msg)
            return error_msg
    else:
        error_msg = " Bad request missing product "
        logging.error(error_msg)
        return error_msg


# Returns a particular product

def get_product(product_id):
    for product in get_products():
        if product['id'] == product_id:
            return product


# Returns availability of the product in the inventory

def check_availabilty(product, quantity):
    isAvailable = True
    inventory_list = get_inventory()
    if product is not None:
        for article in product["contain_articles"]:
            if (aa_id := article.get("art_id", None)) is not None:
                for item in inventory_list:
                    item_id = item.get("art_id", None)
                    if aa_id == item_id:
                        if quantity * int(article.get('amount_of', 0)) > int(item.get('stock', 0)):
                            isAvailable = False
                            break
    return isAvailable


# Loads inventory

def get_inventory():
    inventory_file = open('localdata/inventory.json', 'r')
    inventory = json.load(inventory_file)['inventory']
    inventory_file.close()
    return inventory


# Loads products

def get_products():
    products_file = open('localdata/products.json', 'r')
    products = json.load(products_file)['products']
    products_file.close()
    return products


# Updates inventory

def update_inventory(product, quantity):
    inventory_list = get_inventory()
    for article in product["contain_articles"]:
        if (aa_id := article.get("art_id", None)) is not None:
            for item in inventory_list:
                item_id = item.get("art_id", None)
                if item_id == aa_id:
                    item['stock'] = int(item['stock']) - quantity * int(article.get('amount_of', 0))
    try:
        with open('/src/localdata/inventory.json', 'w') as inventory:
            json.dump({'inventory': inventory_list}, inventory)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
