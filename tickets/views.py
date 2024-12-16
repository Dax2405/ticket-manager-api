from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Enterprise, Place, Ticket, In_Place
from .serializers import EnterpriseSerializer, PlaceSerializer, TicketSerializer, InPlaceSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class EnterpriseListCreateView(generics.ListCreateAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    permission_classes = [IsAuthenticated]


class PlaceListCreateView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]


class VerifyTicketView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_number = request.data.get('id_number')
        try:
            ticket = Ticket.objects.get(id_number=id_number)
            in_place = In_Place.objects.filter(
                ticket=ticket).order_by('-created_at').first()
            if in_place and in_place.state:
                return Response({
                    'message': f'Esta dentro en {in_place.place.name} y entro a las {in_place.created_at}'
                }, status=status.HTTP_401_UNAUTHORIZED)
            elif in_place and not in_place.state:
                return Response({
                    'message': f'Esta fuera y salio a las {in_place.out_at}'
                }, status=status.HTTP_200_OK)
            else:
                new_in_place = In_Place.objects.create(
                    ticket=ticket, place=ticket.destination, state=True)
                serializer = InPlaceSerializer(new_in_place)
                ticket = TicketSerializer(ticket)
                return Response(ticket.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)


class ExitTicketView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_number = request.data.get('id_number')
        try:
            ticket = Ticket.objects.get(id_number=id_number)
            in_place = In_Place.objects.filter(
                ticket=ticket, state=True).order_by('-created_at').first()
            if in_place:
                in_place.state = False
                in_place.out_at = timezone.now()
                in_place.save()
                return Response({
                    'message': f'Salio a las {in_place.out_at}'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'El ticket no está actualmente en In_Place'}, status=status.HTTP_404_NOT_FOUND)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)


class AddPhotoView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        id_number = request.data.get('id_number')
        photo = request.FILES.get('photo')
        if not id_number or not photo:
            return Response({'error': 'id_number and photo are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticket.objects.get(id_number=id_number)
            ticket.image = photo
            ticket.save()
            return Response({'message': 'Photo uploaded successfully'}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
