from django.urls import path
from .views import EnterpriseListCreateView, PlaceListCreateView, TicketListCreateView, LogsListCreateView, VerifyTicketView, ExitTicketView, AddPhotoView, EnterTicketView, InPlaceNumberView

urlpatterns = [
    path('enterprises', EnterpriseListCreateView.as_view(),
         name='enterprise_list_create'),
    path('places', PlaceListCreateView.as_view(), name='place_list_create'),
    path('ticket', TicketListCreateView.as_view(), name='ticket_list_create'),
    path('verify-ticket', VerifyTicketView.as_view(), name='verify_ticket'),
    path('exit-ticket', ExitTicketView.as_view(), name='exit_ticket'),
    path('add-photo', AddPhotoView.as_view(), name='add_photo'),
    path('enter-ticket', EnterTicketView.as_view(), name='enter_ticket'),
    path('logs', LogsListCreateView.as_view(), name='logs_list_create'),
    path('in-place-number', InPlaceNumberView.as_view(), name='in_place_number'),

]
