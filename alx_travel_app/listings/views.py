import requests
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer 

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save()  # You can add custom logic here if needed

class InitiatePaymentView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)

        # Create Payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            currency="ETB"
        )

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "amount": str(payment.amount),
            "currency": payment.currency,
            "tx_ref": f"TRX-{payment.id}",
            "callback_url": request.build_absolute_uri(f"/api/payments/verify/{payment.id}/"),
            "return_url": "https://your-frontend.com/payment-success",
            "customization": {
                "title": "Booking Payment",
                "description": f"Payment for booking {booking.id}"
            }
        }

        chapa_response = requests.post(
            f"{settings.CHAPA_BASE_URL}/transaction/initialize",
            json=payload,
            headers=headers
        )

        if chapa_response.status_code == 200:
            data = chapa_response.json()
            if data.get("status") == "success":
                payment.transaction_id = data["data"]["tx_ref"]
                payment.save()
                return Response({"checkout_url": data["data"]["checkout_url"]}, status=status.HTTP_200_OK)

        return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(generics.GenericAPIView):
    def get(self, request, payment_id, *args, **kwargs):
        payment = get_object_or_404(Payment, id=payment_id)
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }

        response = requests.get(
            f"{settings.CHAPA_BASE_URL}/transaction/verify/{payment.transaction_id}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data["data"]["status"] == "success":
                payment.status = "Completed"
                payment.save()
                return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
            else:
                payment.status = "Failed"
                payment.save()
                return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

from .tasks import send_booking_email

class BookingViewSet(viewsets.ModelViewSet):
    # your queryset, serializer, etc.

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        # Trigger Celery task (async)
        send_booking_email.delay(self.request.user.email, booking.id)
