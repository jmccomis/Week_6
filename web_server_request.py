import requests
from time import sleep



resp = requests.get('http://192.168.1.15:5000/Temperature')
print(resp.text)

x=str(input('would you like the Temperature only? if so type yes----> '))

if x=='yes':
    print('the temperature is ' + str(resp.json()['temperature']))
else:
    print("okay")
y= str(input('would you like to change the setppoint value? if so type yes-----> '))
z=str('hello')
if y=='yes':
    setpoint=str(input('enter the new setpoint here: '))
    resp= requests.put('http://192.168.1.15:5000/Temperature/Setpoint/' + str(setpoint))
    resp = requests.get('http://192.168.1.15:5000/Temperature')
    print(resp.text)
else:
    print('have a nice day')




