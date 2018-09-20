import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import numpy as np
from Database_check import PostgresConnection
from datetime import datetime
from datetime import date
theta=[]
r1=[]
r2=[]
r3=[]
r4=[]
flag=0
w = 10
h = 10
d = 70
fig = plt.figure(figsize=(w, h), dpi=d)
ax = fig.add_subplot(111, polar=True)

today=date.today()
now= datetime.now()
# print("Date componets:",today.day,today.month,today.year)
# print(now.hour,now.minute,now.second)
database_name= 'radii_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
print(database_name)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("0 to 90 degree distance")
    client.subscribe("90 to 180 degree distance")
    client.subscribe("180 to 270 degree distance")
    client.subscribe("270 to 360 degree distance")
    # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global r1
    global r2
    global r3
    global r4
    global flag
    print(msg.topic+" "+str(msg.payload.decode('utf-8')))
    if msg.topic  == '0 to 90 degree distance':
        r1.append(int(msg.payload.decode('utf-8')))
    elif msg.topic == '90 to 180 degree distance':
        r2.append(int(msg.payload.decode('utf-8')))
    elif msg.topic == '180 to 270 degree distance':
        r3.append(int(msg.payload.decode('utf-8')))
    elif msg.topic == '270 to 360 degree distance':
        r4.append(int(msg.payload.decode('utf-8')))
    elif msg.topic == 'Number of times mapped':
        flag=1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("172.16.73.4", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
client.loop_start()
time.sleep(180)
client.disconnect()
client.loop_stop()

r=[]
r = r1+r2+r3+r4
for i in range(len(r)):
    if(r[i]>400):
        r[i]=300
theta=[i for i in range(len(r))]
theta1=[i*(np.pi/180) for i in theta]
print(theta,"    ",r)
ax.plot(theta1,r)
ax.set_title("A line plot on a polar axis", va='bottom')
print("Starting databse")
obj1 = PostgresConnection()
cur = obj1.con.cursor()
# for i in theta:
cur.execute('ALTER TABLE {} ADD COLUMN {} text'.format('radar', database_name))
# cur.execute("UPDATE radar SET {}")
obj1.con.commit()

for i in range(361):
    cur.execute("UPDATE radar SET {} = {} WHERE degree = {}" .format(database_name,r[i],i))
    obj1.con.commit()

plt.show()