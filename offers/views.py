from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response

from offers.models import Offer
from offers.serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    #def get_queryset(self):
        #return Offer.objects.filter(item_given__owner=self.request.user)
