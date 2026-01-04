from ..Serials.debt_serializer import DebtSerializer
from ..Models.debt_information import DebtModel
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..Auth.is_owner_read_write import IsOwnerOrDeny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .in_debt_flag import InDebtCheck


class DebtGetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    def get(self, request):
        try:
            dbItems = DebtModel.objects.filter(user=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DebtSerializer(dbItems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DebtCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Save the new object, assigning the owner to the current user
        serializer.save(user=self.request.user)

    def post(self, request):
        serializer = DebtSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DebtUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]

    def put(self, request, pk):
        try:
            dbItem = DebtModel.objects.get(id = pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if dbItem.user == request.user:
            serializer = DebtSerializer(dbItem, request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
class DebtDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    def delete(self, request, pk):
        try:
            dbItem = DebtModel.objects.get(id = pk)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        if request.user == dbItem.user:
            dbItem.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DebtTotalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    def get(self, request):
        total = 0
        try:
            total = DebtModel.customObject.get_total("debt", 
                                                     request.user, 
                                                     "_amount")
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Check to see if debt status changed. If so, send a message out via Twilio
        try:
            InDebtCheck.get_debt_flag(user=request.user, total=total['debt_amount'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(total, status=status.HTTP_200_OK)

class DebtPaymentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    def get(self, request):
        try:
            payment = DebtModel.customObject.get_total("debt", 
                                                       request.user, 
                                                       "_payment")
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        return Response(payment, status.HTTP_200_OK)