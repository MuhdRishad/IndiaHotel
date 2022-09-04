from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from hotel.models import Dishes,Review
from hotel.serializers import DishSerializer,DishModelSerializer,UserSerialization,ReviewSerializer
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# Create your views here.

        #  NORMAL SERIALIZER
class DishesView(APIView):
    def get(self,request,*args,**kwargs):
        all_dishes = Dishes.objects.all()   # ORM QUERY FOR COLLECT ALL DISHES FROM DATABASE
        serializer = DishSerializer(all_dishes,many=True)  # DESERIALIZING , MANY=TRUE STANDS FOR DESERIALIZE MORE THAN ONE OBJECT
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer = DishSerializer(data=request.data)    # SERIALIZING DATA
        if serializer.is_valid():    # CHECKING SERILIZER IS VALID
            name = serializer.validated_data.get("name")   # TAKING DATA ONE BY ONE
            category = serializer.validated_data.get("category")
            price = serializer.validated_data.get("price")
            Dishes.objects.create(name=name,          #ORM QUERY FOR CREATE(SAVE) DATA TO DATABASE
                                  category=category,
                                  price=price
                                  )
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class DishDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        serializer = DishSerializer(dish)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")  # TAKING DATA ONE BY ONE
            category = serializer.validated_data.get("category")
            price = serializer.validated_data.get("price")
            instance.name = name
            instance.category = category
            instance.price = price
            instance.save()
            return Response(data=serializer.data)

    def delete(self,request,*args,**kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        dish.delete()
        return Response({"msg":"deleted"})









#  MODEL SERIALIZER

class SignUpView(APIView):
    serialzer_class = UserSerialization

    def get(self,request,*args,**kwargs):
        all_user = User.objects.all()
        serialzer = self.serialzer_class(all_user,many=True)
        return Response(data=serialzer.data)
    def post(self,request,*args,**kwargs):
        serializer = self.serialzer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class MenuItemsView(APIView):
    serializer_class = DishModelSerializer

    def get(self,request,*args,**kwargs):
        all_dishes = Dishes.objects.all()
        serializer = self.serializer_class(all_dishes,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class MenuItemDetailView(APIView):
    serializer_class = DishModelSerializer

    def get(self,request,*args,**kwargs):
        dish_id = kwargs.get("id")
        try:
            dish = Dishes.objects.get(id=dish_id)
            serializer = self.serializer_class(dish)
            return Response(data=serializer.data)
        except:
            return Response({"msg":"invalid"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):
        dish_id = kwargs.get("id")
        instance = Dishes.objects.get(id=dish_id)
        serializer = self.serializer_class(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def delete(self,request,*args,**kwargs):
        dish_id = kwargs.get("id")
        try:
            dish = Dishes.objects.get(id=dish_id)
            dish.delete()
            return Response(data=request.data)
        except:
            return Response({"msg":"deleted"},status=status.HTTP_400_BAD_REQUEST)




# USING VIEWSET CLASS
class DishViewsetsView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs = Dishes.objects.all()
        if "category" in request.query_params:
            category = request.query_params.get("category")
            qs = qs.filter(category=category)
        if "price_lt" in request.query_params:
            price = request.query_params.get("price_lt")
            qs = qs.filter(price__lte=price)
        serializer = DishModelSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kwargs):
        serializer = DishModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        dish_id = kwargs.get("pk")
        qs = Dishes.objects.get(id=dish_id)
        serializer = DishModelSerializer(qs)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        dish_id = kwargs.get("pk")
        instance = Dishes.objects.get(id=dish_id)
        serializer = DishModelSerializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        dish_id = kwargs.get("pk")
        qs = Dishes.objects.get(id=dish_id)
        qs.delete()
        return Response({"msg":"deleted"})





#USING MODELVIEWSET
class DishModelViewSetView(viewsets.ModelViewSet):
    serializer_class = DishModelSerializer
    queryset = Dishes.objects.all()
    model = Dishes

            #BASIC AUTHENTICATION
    # authentication_classes = [authentication.BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

            #TOKEN AUTHENTICATION
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True,methods=["get"])
    def get_reviews(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        dish = Dishes.objects.get(id=id)
        qs = Review.objects.filter(dish=dish)
        serializer = ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)


    @action(detail=True,methods=['post'])
    def add_review(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        dish = Dishes.objects.get(id=id)
        user = request.user
        serializer = ReviewSerializer(data=request.data , context={"user":user , "dish":dish})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


