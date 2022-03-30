
from django.shortcuts import  render
from .models import *
from modbus.models import Digital
from modbus.models import Analog
from EasyModbusPy.easymodbus.modbusClient import *
from EasyModbusPy.easymodbus import modbusClient

# Create your views here.

modbus_client=ModbusClient('192.168.0.60',502)
modbusClient.parity = Parity.even
modbusClient.unitidentifier = 2
modbusClient.baudrate = 9600
modbusClient.stopbits = Stopbits.one
modbus_client.connect()

Digital.objects.all().delete()
Analog.objects.all().delete()

coils = modbus_client.read_coils(0, 10)
for i in range(len(coils)):
    Digital.objects.create(id=i,coil_value=coils[i])

holding_registers=modbus_client.read_holdingregisters(0,10)
for i in range (len(holding_registers)):
    Analog.objects.create(id=i,register_value=holding_registers[i])

print(Analog.objects.values_list('id','register_value'))
print(Digital.objects.values_list('id','coil_value'))    

def index(request):
    
    coils = modbus_client.read_coils(0, 10)
    indexCoils = dict(enumerate(coils))

    holding_registers=modbus_client.read_holdingregisters(0,10)
    indexRegisters =dict(enumerate(holding_registers))
    
    discrete_inputs = modbus_client.read_discreteinputs(0, 10)	
    input_registers = modbus_client.read_inputregisters(0, 10)  

    context={'coils': indexCoils ,'registers': indexRegisters,'discrete_inputs': discrete_inputs,'input_register': input_registers }
    return render(request,'modbus/list.html',context)

def writeCoil(request,index):
    
    coils[index] = not coils[index]
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
        register_value=request.POST.get('number')    
        modbus_client.write_single_register(register_index,  int(register_value))
        
        item= Analog.objects.get(id=register_index)
        item.register_value = int(register_value)
        item.save()
    else:
        print("method is get")
    
    print(Analog.objects.values_list('id','register_value'))
    
    context= {'register_index': register_index, 'register_value': register_value }
    
    return render(request,'modbus/register.html', context)
