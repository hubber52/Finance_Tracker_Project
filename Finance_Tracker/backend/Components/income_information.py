from ..Models.income_information import IncomeModel
from ..Serials.income_serializer import IncomeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..Auth.is_owner_read_write import IsOwnerOrDeny
from rest_framework_simplejwt.authentication import JWTAuthentication

#Returns all budget objects accessable by current User
class IncomeGetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    #Returns all objects in the model
    def get(self, request):
        data = IncomeModel.objects.filter(user=request.user)
        serializer = IncomeSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IncomeCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the new object, assigning the owner to the current user
        serializer.save(user=self.request.user)

    def post(self, request):
        serializer = IncomeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class IncomeUpdateDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]

    #Returns single object corresponding to the primary key requested by client
    def get(self,request, pk):
        try:
            dbItem = IncomeModel.objects.get(id = pk)
        except:
            return Response({"Error":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = IncomeSerializer(dbItem)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            dbItem = IncomeModel.objects.get(id = pk)
        except:
            return Response({"Error":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IncomeSerializer(dbItem, request.data)
        if serializer.is_valid():
            if self.request.user == serializer.instance.user:
                serializer.save(user = self.request.user)
            else:
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try:
            dbItem = IncomeModel.objects.get(id = pk)
            if self.request.user == dbItem.user:
                dbItem.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class IncomeTotalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    def get(self, response):
        try:
            total = IncomeModel.customObject.get_total("income", response.user, "_amount")
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(total, status=status.HTTP_200_OK)

