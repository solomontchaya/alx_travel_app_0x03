import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer

CHAPA_BASE_URL = "https://api.chapa.co/v1/transaction"

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@api_view(['POST'])
def initiate_payment(request):
    booking_reference = request.data.get("booking_reference")
    amount = request.data.get("amount")
    email = request.data.get("email")  # for payment notification
    currency = request.data.get("currency", "ETB")  # default currency
    
    # Create pending payment
    payment = Payment.objects.create(
        booking_reference=booking_reference,
        amount=amount,
        status=Payment.PENDING
    )
    
    payload = {
        "amount": amount,
        "currency": currency,
        "email": email,
        "first_name": request.data.get("first_name"),
        "last_name": request.data.get("last_name"),
        "tx_ref": payment.booking_reference,
        "callback_url": request.build_absolute_uri('/api/verify-payment/')
    }
    
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }
    
    response = requests.post(f"{CHAPA_BASE_URL}/initialize", json=payload, headers=headers)
    data = response.json()
    
    if data.get("status") == "success":
        payment.transaction_id = data["data"]["id"]
        payment.save()
        return Response({"payment_link": data["data"]["checkout_url"]})
    return Response({"error": "Payment initiation failed"}, status=400)

@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")
    payment = get_object_or_404(Payment, booking_reference=tx_ref)
    
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    response = requests.get(f"{CHAPA_BASE_URL}/verify/{payment.transaction_id}", headers=headers)
    data = response.json()
    
    if data.get("status") == "success":
        status = data["data"]["status"]
        if status.lower() == "success":
            payment.status = Payment.COMPLETED
            # Optionally trigger Celery email task here
        else:
            payment.status = Payment.FAILED
        payment.save()
        return Response({"status": payment.status})
    
    return Response({"error": "Verification failed"}, status=400)