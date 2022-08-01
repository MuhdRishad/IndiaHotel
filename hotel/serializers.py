from rest_framework import serializers
from hotel.models import Dishes
from django.contrib.auth.models import User

            #NORMAL SERIALIZER
class DishSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()



        #MODEL SERIALIZER
class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DishModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"

    def validate(self,data):
        amount = data.get("price")
        if amount < 0:
            raise serializers.ValidationError('Negative price is not allowed')
        return data
