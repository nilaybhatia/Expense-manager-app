from .models import Income, Savings, Expenditure
from .serializers import IncomeSerializer, SavingsSerializer, ExpenditureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class IncomeAPIView(APIView):
    def get(self, request):
        incomes = Income.objects.all()
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)