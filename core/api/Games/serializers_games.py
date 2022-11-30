from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.homepage.models import *
from core.user.models import User
from core.erp.models import *

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameFootball
        fields = "__all__"

    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'referee_id':instance.referee.id if instance.referee is not None else "",
            'refereeNameCenter' : instance.referee.user.get_full_name() if instance.referee is not None else "",
            'refereeAssistantOne_id':instance.refereeAssistantOne.id if instance.refereeAssistantOne is not None else "",
            'refereeAssistantOneNameCenter' : instance.refereeAssistantOne.user.get_full_name() if instance.refereeAssistantOne is not None else "",
            'refereeAssistantTwo_id':instance.refereeAssistantTwo.id if instance.refereeAssistantTwo is not None else "",
            'refereeAssistantOneNameCenter' : instance.refereeAssistantTwo.user.get_full_name() if instance.refereeAssistantTwo is not None else "",
            'teamLocal':instance.teamLocal.id if instance.teamLocal is not None else "",
            'teamLocalName': instance.teamLocal.name if instance.teamLocal is not None else "",
            "teamLocalImage": instance.teamLocal.get_image() if instance.teamLocal is not None else "",
            'teamVisitor':instance.teamVisitor.id if instance.teamVisitor is not None else "",
            'teamVisitorName': instance.teamVisitor.name if instance.teamVisitor is not None else "",
            'teamVisitorImage': instance.teamVisitor.get_image() if instance.teamVisitor is not None else "",
            'stadium':instance.stadium.id if instance.stadium is not None else "",
            'stadiumName':instance.stadium.name if instance.stadium is not None else "",
            'latitud': instance.stadium.coordinates.split(',')[0].replace(',', '.') if instance.stadium is not None else "",
            'longitud': instance.stadium.coordinates.split(',')[1].replace(',', '.') if instance.stadium is not None else "",
            'dateGame': instance.dateGame if instance.dateGame is not None else "",
            'hourGame': instance.hourGame.strftime('%H:%M') if instance.hourGame is not None else "",
            'desc': instance.desc if instance.desc is not None else "",
            'price': instance.price if instance.price is not None else "",
        }

