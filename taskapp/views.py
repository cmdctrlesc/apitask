import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def shopify_api(request):

    query = '{products(first:40) {edges {node { title description createdAt }}}}'

    url = 'https://upsquaresandbox.myshopify.com/api/graphql'
    json = {'query': query}
    access_token = "your token here!"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": access_token
    }

    apirequest = requests.post(url=url, json=json, headers=headers)
    if apirequest.status_code == 200:
        apiresponse = apirequest.json()
        nodes = apiresponse['data']['products']['edges']
        paginator = Paginator(nodes, 10)
        page = request.GET.get('page')

        try:
            result = paginator.page(page)
            objects = result.object_list

        except PageNotAnInteger:
            result = paginator.page(1)
            objects = result.object_list
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
            objects = result.object_list

    else:

        raise APIException("GraphQL query failed to run by returning code of {}. {}".format(
            apirequest.status_code, query))

    return Response(objects)
