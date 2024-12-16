from django.urls import path
from .views import EnterpriseListCreateView, PlaceListCreateView, TicketListCreateView, VerifyTicketView, ExitTicketView, AddPhotoView

urlpatterns = [
    path('enterprises/', EnterpriseListCreateView.as_view(),
         name='enterprise_list_create'),
    path('places/', PlaceListCreateView.as_view(), name='place_list_create'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket_list_create'),
    path('verify-ticket/', VerifyTicketView.as_view(), name='verify_ticket'),
    path('exit-ticket/', ExitTicketView.as_view(), name='exit_ticket'),
    path('add-photo/', AddPhotoView.as_view(), name='add_photo'),

]
