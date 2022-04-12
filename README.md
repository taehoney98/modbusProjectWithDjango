# modbusProjectWithDjango

![structureOfDjango](./structureOfDjango.png)

Django를 활용한 modbusTCP 실습

## ModbusClient 연결 설정
```python
modbus_client=ModbusClient('192.168.0.60',502)
modbus_client.parity = Parity.even #짝수 패리티
modbus_client.unitidentifier = 1 # slave id 
modbus_client.baudrate = 9600  #전송속도 보오 레이트
modbus_client.stopbits = Stopbits.one #정지 비트  데이터 송출 종료 알림

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

```
웹 페이지 작동시 해당 IP,Port번호로 설정 후 connect한 후, 초기 coils 값과 holding_registers 값을 읽어 각각 Digital과 Analog 모델 값으로 DB에 추가 한다.
## views.py
### index 합수
```python

def index(request):
    
    coils = modbus_client.read_coils(0, 10)
    indexCoils = dict(enumerate(coils))

    holding_registers=modbus_client.read_holdingregisters(0,10)
    indexRegisters =dict(enumerate(holding_registers))
    
    discrete_inputs = modbus_client.read_discreteinputs(0, 10)	
    input_registers = modbus_client.read_inputregisters(0, 10)  

    context={'coils': indexCoils ,'registers': indexRegisters,'discrete_inputs': discrete_inputs,'input_register': input_registers }
    return render(request,'modbus/list.html',context)
```
초기페이지에서  coil, holdingregister, discrete_inputs, input_registers 값을 읽어 modbus/list.html로 전달한다.

### writeCoil 함수
``` python

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
```
현재의 coil 값에 not을 붙여 write_single_coil을 통해 변경한 후, Digital Model 의 해당 index 값을 coils[index]값으로 변경한다.




### writeRegister 함수
```  python

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

```
list.html에서 전달받은 방식이 POST면, number에 해당하는 값을 register_value에 저장하고 write_single_register를 통해 변경한다.
Analog Model의 해당 index 값을 register_value로 변경한다.
## urls.py 

```python 
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index , name='index'),    
    path('coil/<int:index>/',views.writeCoil,name='writeCoil'),
    path('register/<int:register_index>/<int:register_value>', views.writeRegister, name='writeRegister'),
    
]

```
url.py의 path에서 해당하는 view.py 의 해당하는 함수 명으로 이동한다.


## models.py

```python
from django.db import models
from EasyModbusPy.easymodbus.modbusClient import *

# Create your models here.
class Digital (models.Model):
    coil_value =models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.coil_value)
    
    
class Analog (models.Model):
    register_value =models.IntegerField(default=0)

    def __str__(self):
        return str(self.register_value)
    
```
boolean 값의 coil_value를 갖는 Digital 클래스와 integer 값의 register_value를 갖는 Analog 클래스가 존재한다. 
