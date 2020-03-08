from django.shortcuts import render
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def shopify_api(request):

    query = '{products(first:40) {edges {node { title description createdAt }}}}'

    url = 'https://upsquaresandbox.myshopify.com/api/graphql'
    json = {'query': query}
    access_token = "your token here"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": access_token
    }

    apirequest = requests.post(url=url, json=json, headers=headers)
    if apirequest.status_code == 200:
        results = apirequest.json()
        nodes = results['data']['products']['edges']
        paginator = Paginator(nodes, 10)
        page = request.GET.get('page')

        try:
            result = paginator.page(page)
            titles = result.object_list

        except PageNotAnInteger:
            result = paginator.page(1)
            titles = result.object_list
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
            titles = result.object_list

    else:

        raise Exception("Query failed to run by returning code of {}. {}".format(
            apirequest.status_code, query))

    return Response(titles)
