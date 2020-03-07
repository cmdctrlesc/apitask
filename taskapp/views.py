from django.shortcuts import render
import requests
import json


def consume_api(request):

    query = '{products(first:40) {edges {node { title }}}}'

    url = 'https://upsquaresandbox.myshopify.com/api/graphql'
    json = {'query': query}
    access_token = "put your token here!"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": access_token
    }

    apirequest = requests.post(url=url, json=json, headers=headers)
    if apirequest.status_code == 200:
        results = apirequest.json()
        nodes = results['data']['products']['edges']
        titles = [(node['node']['title']) for node in nodes]
        context = {'titles': titles}
    else:

        raise Exception("Query failed to run by returning code of {}. {}".format(
            apirequest.status_code, query))

    return render(request, "taskapp/products.html", context)
