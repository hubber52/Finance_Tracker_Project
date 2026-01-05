from ..Models.debt_information import InDebtModel
from ..Serials.debt_serializer import InDebtSerializer
from ..Serials.serializer import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .kafka_messages import KafkaMessageService


class InDebtCheck:
    def get_debt_flag(user, total, producer=None):
        try:
            user_serializer = CustomUserSerializer(user)
            primary_key = user_serializer.data['id']
            uuid = user_serializer.data['uuid']
            phone = user_serializer.data['phone']
            email = user_serializer.data['email']
            debtor = None
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        def helper(total, debtor_serializer, model_instance):
            try:
                in_debt = debtor_serializer.data['negative_debt']
                if total == 0 and in_debt == 1:
                    #Send kafka message, out of debt
                    model_instance.negative_debt = False
                    model_instance.save()
                    try:
                        message = producer or KafkaMessageService()
                        message.send_message([uuid, 
                                              model_instance.negative_debt, 
                                              phone, 
                                              email, 
                                              settings.SECRET_KEY])

                    except:
                        print("Failed to connect to Kafka")
                elif total > 0 and in_debt == 0:
                    #Send kafka message, in debt
                    model_instance.negative_debt = True
                    model_instance.save()
                    try:
                        message = KafkaMessageService(producer=producer)
                        message.send_message([uuid, 
                                              model_instance.negative_debt, 
                                              phone, 
                                              email, 
                                              settings.SECRET_KEY])
                    except:
                        print("Failed to connect to Kafka")
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        #If user exists, get the user instance
        try:
            debtor = InDebtModel.objects.get(user_id=primary_key)
        except:
            debtor = InDebtModel.objects.create(user=user, 
                                                negative_debt=0)
            debtor.save()
        #Check flag
        try:
            debtor_serializer = InDebtSerializer(debtor)
            helper(total, debtor_serializer, debtor)
            return True
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
