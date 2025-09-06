import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_email


class ListingViewSet(viewsets.ModelViewSet):
    """CRUD operations for Listings"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """CRUD operations for Bookings + async email notifications"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        # Trigger Celery async email
        send_booking_email.delay(self.request.user.email, booking.id)


class InitiatePaymentView(generics.GenericAPIView):
    """Initiate a payment with Chapa API"""
    def post(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)

        # Create a payment record
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
            "callback_url": request.build_absolute_uri(
                f"/api/payments/verify/{payment.id}/"
            ),
            "return_url": "https://your-frontend.com/payment-success",
            "customization": {
                "title": "Booking Payment",
                "description": f"Payment for booking {booking.id}"
            }
        }

        try:
            response = requests.post(
                f"{settings.CHAPA_BASE_URL}/transaction/initialize",
                json=payload,
                headers=headers,
                timeout=10
            )
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                payment.transaction_id = data["data"]["tx_ref"]
                payment.save()
                return Response({"checkout_url": data["data"]["checkout_url"]}, status=status.HTTP_200_OK)

            return Response({"error": data.get("message", "Payment initiation failed")}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Payment service unavailable: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class VerifyPaymentView(generics.GenericAPIView):
    """Verify payment status with Chapa API"""
    def get(self, request, payment_id, *args, **kwargs):
        payment = get_object_or_404(Payment, id=payment_id)

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }

        try:
            response = requests.get(
                f"{settings.CHAPA_BASE_URL}/transaction/verify/{payment.transaction_id}",
                headers=headers,
                timeout=10
            )
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                chapa_status = data["data"]["status"]

                if chapa_status == "success":
                    payment.status = "Completed"
                    payment.save()
                    return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)

                payment.status = "Failed"
                payment.save()
                return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": data.get("message", "Verification failed")}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Verification service unavailable: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
