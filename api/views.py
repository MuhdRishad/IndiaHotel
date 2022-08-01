from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import menu_items

# Create your views here.


class DishesView(APIView):
    def get(self,request,*args,**kwargs):
        all_items = menu_items
        if "category" in request.query_params:
            category = request.query_params.get("category")
            all_items = [item for item in all_items if item["category"] == category]
        if "limit" in request.query_params:
            limit = int(request.query_params.get("limit"))
            all_items = all_items[0:limit]
        if "price_lt" in request.query_params:
            price_lt = int(request.query_params.get("price_lt"))
            all_items = [ item for item in all_items if item.get("price") <= price_lt]
        return Response(data=all_items)

    def post(self, request, *args, **kwargs):
        item = request.data
        menu_items.append(item)
        return Response(data=item)

class DishDetailView(APIView):
    def get(self,request,*args,**kwargs):
        code = kwargs.get('dcode')
        item = [item for item in menu_items if item['code'] == code].pop()
        return Response(data=item)

    def put(self,request,*args,**kwargs):
        code = kwargs.get('dcode')
        item = [item for item in menu_items if item['code'] == code].pop()
        data = request.data
        item.update(data)
        return Response(data=data)

    def delete(self,request,*args,**kwargs):
        code = kwargs.get('dcode')
        item = [item for item in menu_items if item['code'] == code].pop()
        menu_items.remove(item)
        return Response(data=item)

