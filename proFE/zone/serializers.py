from rest_framework import serializers
from .models import Zone
from trottinette.models import Trottinette 

class TrottinetteMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trottinette
        fields = "__all__"
class ZoneSerializer(serializers.ModelSerializer):
    trottinettes = TrottinetteMiniSerializer(many=True, read_only=True)
    nombre_trottinette = serializers.SerializerMethodField()
    nombre_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        fields = [
            "id",
            "nom",
            "latitude",
            "longitude",
            "trottinettes",
            "nombre_trottinette",
            "nombre_disponibles"
        ]

    def get_nombre_trottinette(self, obj):
        return obj.trottinette.count()

    def get_nombre_disponibles(self, obj):
        return obj.trottinette.filter(status='disponible').count()