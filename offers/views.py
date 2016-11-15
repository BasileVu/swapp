from rest_framework import viewsets

from offers.models import Offer
from offers.serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'PUT' or request.method == "PATCH" or request.method == "DELETE":
            return view.owner == request.user
        if request.method == 'POST':
            return request.user.is_authenticated()
