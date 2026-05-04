from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, Transaction
from accounts.models import User
from trottinette.models import TrottinetteBooking
import uuid


class CreateInvoiceView(APIView):
    def post(self, request):
        print(request.data)
        user_id = request.data.get("user")
        booking_id = request.data.get("trottinette_booking")
        amount = request.data.get("amount")
        print(user_id,booking_id,amount)
        user = User.objects.get(id=user_id)
        trottinetteBooking = TrottinetteBooking.objects.get(id=booking_id)
        print("TrottinetteBooking",trottinetteBooking)
        try:
            user = User.objects.get(id=user_id)
            TrottinetteBooking = TrottinetteBooking.objects.get(id=booking_id)
            print("TrottinetteBooking",TrottinetteBooking)
        except:
            return Response({"error": "User ou Booking introuvable"}, status=404)
        invoice = Invoice.objects.create(
            invoice_number=str(uuid.uuid4())[:8],
            user=user,
            booking=booking,
            amount=amount
        )

        return Response({
            "message": "Facture créée",
            "invoice_id": invoice.id,
            "amount": invoice.amount
        })


class PayInvoiceView(APIView):

    def post(self, request):
        invoice_id = request.data.get("invoice_id")
        payment_method = request.data.get("payment_method")
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice introuvable"}, status=404)

        transaction = Transaction.objects.create(
            transaction_id=str(uuid.uuid4()),
            user=invoice.user,
            invoice=invoice,
            amount=invoice.amount,
            payment_method=payment_method,
            status="success"
        )

        invoice.status = "payée"
        invoice.save()

        return Response({
            "message": "Paiement effectué",
            "transaction_id": transaction.transaction_id
        })


class ListInvoicesView(APIView):

    def get(self, request):
        invoices = Invoice.objects.all()
        data = []
        for i in invoices:
            data.append({
                "id": i.id,
                "invoice_number": i.invoice_number,
                "user": i.user.id,
                "amount": i.amount,
                "status": i.status
            })

        return Response(data)

# Create your views here.
