# coding:utf-8
from rest_framework import serializers

from boai.apps.boai_model.models import AppSocials


class SocialSerializer(serializers.ModelSerializer):
    socialbase_min = serializers.FloatField()
    socialbase_max = serializers.FloatField()
    housingfundbase_min = serializers.FloatField()
    housingfundbase_max = serializers.FloatField()
    endowment = serializers.FloatField()
    medical = serializers.FloatField()
    unemployment = serializers.FloatField()
    employment = serializers.FloatField()
    maternity = serializers.FloatField()
    disability = serializers.FloatField()
    housingfund = serializers.FloatField()

    class Meta:
        model = AppSocials
