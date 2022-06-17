from django.shortcuts import  render
from modbus.models import Digital ,  Analog
from EasyModbusPy.easymodbus.modbusClient import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DigitalSerializer ,  AnalogSerializer
# Create your views here.

modbus_client=ModbusClient('192.168.0.60',502)
modbus_client.parity = Parity.even #짝수 패리티
modbus_client.unitidentifier = 1 #slave id 
modbus_client.baudrate = 9600  #전송속도 보오 레이트
modbus_client.stopbits = Stopbits.one #정지 비트  데이터 송출 종료 알림

modbus_client.connect()

Digital.objects.all().delete()
Analog.objects.all().delete()

coils = modbus_client.read_coils(0, 10)
for i in range(len(coils)): # Digital에 coil_value 저장
    Digital.objects.create(id=i,coil_value=coils[i])

holding_registers=modbus_client.read_holdingregisters(0,10)
for i in range (len(holding_registers)): #Analog에 register_value 저장
    Analog.objects.create(id=i,register_value=holding_registers[i])



def index(request):
    coils = modbus_client.read_coils(0, 10)
    indexCoils = dict(enumerate(coils)) # iterable 형태로 바꾼후 딕셔너리로 변환

    holding_registers=modbus_client.read_holdingregisters(0,10)
    indexRegisters =dict(enumerate(holding_registers))
    
    discrete_inputs = modbus_client.read_discreteinputs(0, 10)	
    input_registers = modbus_client.read_inputregisters(0, 10)  
    
    context={'coils': indexCoils ,'registers': indexRegisters,'discrete_inputs': discrete_inputs,'input_register': input_registers }
    return render(request,'modbus/list.html',context)

def writeCoil(request,index):
    
    coils[index] = not coils[index] # coils[index]값에 반대값 저장
    modbus_client.write_single_coil(index, coils[index])
    
    if coils[index] == False:
        item =Digital.objects.get(id=index)
        item.coil_value = False
        item.save()
    else:
        item= Digital.objects.get(id=index)
        item.coil_value = True
        item.save()
        
    print(Digital.objects.values_list('id','coil_value'))
    
    context={'changedcoil': coils}
    return render(request, 'modbus/coils.html',context)


def writeRegister(request, register_index, register_value):
    
    if request.method == 'POST':
        register_value=request.POST.get('number') # Post로 전달된 number 변수 값 저장
        modbus_client.write_single_register(register_index,  int(register_value))
        
        item= Analog.objects.get(id=register_index)
        item.register_value = int(register_value)
        item.save()
    else:
        print("method is get")
    
    print(Analog.objects.values_list('id','register_value'))
    
    context= {'register_index': register_index, 'register_value': register_value }
    
    return render(request,'modbus/register.html', context)

class DigitalRestAPI(APIView):
    
    def get(self, request, **coil_id): 
        if (coil_id.get('id') is None): #coil id 존재하지 않을시
            queryset= Digital.objects.all()
            serializer = DigitalSerializer(queryset,many = True) # 모든 queryset = True로 지정
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            digital_id=coil_id.get('id')
            serializer=DigitalSerializer(Digital.objects.get(id=digital_id))
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DigitalSerializer(data=request.data)
        if serializer.is_valid(): #유효하면 201 리턴 아니면 400 리턴
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, **coil_id):
        if coil_id.get('id') is None: #id 입력 x 시
            return Response("move to detail coil_id page ", status=status.HTTP_400_BAD_REQUEST)
        else:
            digital_id = coil_id.get('id')
            digital_object = Digital.objects.get(id=digital_id)
            changed_serializer = DigitalSerializer(digital_object, data=request.data)
            modbus_client.write_single_coil(digital_id,request.data.get('coil_value'))
            if changed_serializer.is_valid():
                changed_serializer.save()
                return Response(changed_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("changed_serializer not exist. ", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, **coil_id):
        if coil_id.get('id') is None: #id url 입력받지 못했을 시
            return Response("move to detail coil_id page ", status=status.HTTP_400_BAD_REQUEST)
        else:
            digital_id = coil_id.get('id')
            digital_object = Digital.objects.get(id=digital_id)
            digital_object.delete()
            return Response("delete ok", status=status.HTTP_200_OK)
        
        
class AnalogRestAPI(APIView):
    def get(self, request, **register_id):
        if (register_id.get('id') is None):
            queryset= Analog.objects.all()
            serializer = AnalogSerializer(queryset,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            analog_id=register_id.get('id')
            serializer=AnalogSerializer(Analog.objects.get(id=analog_id))
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AnalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, **register_id):
        if register_id.get('id') is None:
            return Response("move to detail register_id page ", status=status.HTTP_400_BAD_REQUEST)
        else:
            analog_id = register_id.get('id')
            Analog_object = Analog.objects.get(id=analog_id)
            changed_serializer = AnalogSerializer(Analog_object, data=request.data)
            modbus_client.write_single_register(analog_id,request.data.get('register_value'))
            if changed_serializer.is_valid():
                changed_serializer.save()
                return Response(changed_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("changed_serializer not exist. ", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, **register_id):
        if register_id.get('id') is None:
            return Response("move to detail register_id page", status=status.HTTP_400_BAD_REQUEST)
        else:
            analog_id = register_id.get('id')
            Analog_object = Analog.objects.get(id=analog_id)
            Analog_object.delete()
            return Response("register is deleted", status=status.HTTP_200_OK)
        