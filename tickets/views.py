from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count
from .models import Enterprise, Place, Ticket, In_Place, Logs
from .serializers import EnterpriseSerializer, PlaceSerializer, TicketSerializer, InPlaceSerializer, LogsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import send_ticket_email


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

    def perform_create(self, serializer):
        ticket = serializer.save()
        send_ticket_email(ticket)


class LogsListCreateView(generics.ListCreateAPIView):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    permission_classes = [IsAuthenticated]


class VerifyTicketView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_number = request.data.get('id_number')
        try:
            ticket = Ticket.objects.get(id_number=id_number)
            in_place = In_Place.objects.filter(
                ticket=ticket).order_by('-created_at').first()
            ticket_serializer = TicketSerializer(ticket)
            if in_place and in_place.state:
                return Response({
                    'ticket': ticket_serializer.data,
                    'message': f'Esta dentro en {in_place.place.name} y entro a las {in_place.created_at}'
                }, status=status.HTTP_401_UNAUTHORIZED)
            elif in_place and not in_place.state:

                return Response({
                    'ticket': ticket_serializer.data,
                    'message': f'Esta fuera y salio a las {in_place.out_at}'
                }, status=status.HTTP_200_OK)

            else:

                return Response({
                    'ticket': ticket_serializer.data,
                    'message': "Ticket valido"}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            print(f'Ticket {id_number} no existe')
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)


class EnterTicketView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_number = request.data.get('id_number')
        try:
            ticket = Ticket.objects.get(id_number=id_number)
            in_place = In_Place.objects.filter(
                ticket=ticket, state=True).order_by('-created_at').first()
            if in_place:
                if in_place.state:
                    return Response({'error': 'El ticket ya está en dentro'}, status=status.HTTP_400_BAD_REQUEST)

                in_place.state = True
                in_place.save()
                return Response(status=status.HTTP_200_OK)

            else:
                new_in_place = In_Place.objects.create(
                    ticket=ticket, place=ticket.destination, state=True)
                serializer = InPlaceSerializer(new_in_place)
                new_log = Logs.objects.create(
                    ticket=ticket, place=ticket.destination, action='Entrada')
                new_log.save()

                return Response({'message': 'Ticket ingresado correctamente'}, status=status.HTTP_200_OK)
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
                new_log = Logs.objects.create(
                    ticket=ticket, place=in_place.place, action='Salida')
                new_log.save()
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


class InPlaceNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        in_place_counts = In_Place.objects.filter(state=True).values(
            'place__name').annotate(count=Count('id'))

        place_counts = {item['place__name']: item['count']
                        for item in in_place_counts}

        return Response(place_counts, status=status.HTTP_200_OK)
