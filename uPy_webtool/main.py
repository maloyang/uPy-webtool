# -*- coding: utf-8 -*-

import machine
import network
import time
import os

#- check ap config file
AP_SSID = 'upy'
AP_PWD = 'pypypypy'
ap_config = None
ap_config_fn = 'ap.txt'
if ap_config_fn in os.listdir():
    print('ap config here!')
    f = open(ap_config_fn)
    ap_config = f.read()
    f.close()
if ap_config:
    print( ('ap_config:', ap_config))
    ap_config = ap_config.split('\n')
    AP_SSID = ap_config[0].strip()
    AP_PWD = ap_config[1].strip()
print('line to: ', (AP_SSID, AP_PWD))

#-- 連到AP 為Station
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(AP_SSID, AP_PWD)
sta_if.isconnected()
for i in range(20):
    time.sleep(0.5)
    if sta_if.isconnected():
        break
sta_ip = ''
if sta_if.isconnected():
    print('connected!  --> ', sta_if.ifconfig())
    sta_ip = sta_if.ifconfig()[0]
else:
    print('not connected!  --> ', sta_if.ifconfig())

#-- 當AP，並指定
uid = machine.unique_id()
#ap_if.ifconfig()
# ('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.43.1')
# (ip, mask, gateway, dns)
my_sn = '%02X-%02X-%02X-%02X' %(uid[0], uid[1], uid[2], uid[3])

#- Change name/password/ip of ESP8266's AP:
ap_if = network.WLAN(network.AP_IF)
#ap_if.ifconfig([my_ip, my_mask, my_gw, my_dns])

my_ssid = 'upy_%s_%s' %(my_sn, sta_ip)
#ap_if.config(essid = my_ssid)#改ssid，馬上生效
ap_if.config(essid=my_ssid, authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
#DHCP 功能micropython預設就有，不用設定
#AP的IP，每次重開都會回到預設值，因此需要開機時就設定
#一般是配給AP ip的下一號ip


import socket
from machine import Pin
from machine import PWM
import dht
#from hcsr04 import HCSR04

def Tune(buzzer, freq=262, t=500, duty=50):
    ''' t: ms '''
    if freq==0:
        buzzer.duty(0)
    else:
        buzzer.duty(duty)
    buzzer.freq(freq)
    time.sleep_ms(t)


# PIN Define:
D0 = 16
D1 = 5  #PWM
D2 = 4  #PWM
D3 = 0  #PWM
D4 = 2  #PWM, #Led on board
D5 = 14 #PWM
D6 = 12 #PWM
D7 = 13 #PWM
D8 = 15 #PWM

#Setup PINS
led = machine.Pin(2, machine.Pin.OUT)

# buzzer
NOTE_C4=262
NOTE_D4=294
NOTE_E4=330
NOTE_F4=349
NOTE_G4=392
NOTE_A4=440
NOTE_B4=494
buzzer = PWM(Pin(D2), freq=1000, duty=0)

# servo
SV_ANGLE_0 = 40
SV_ANGLE_90 = 77
SV_ANGLE_180 = 115
servo = PWM(Pin(D5), freq=50)
servo2 = PWM(Pin(D6), freq=50)
servo3 = PWM(Pin(D7), freq=50)
servo4 = PWM(Pin(D8), freq=50)

# th_sensor
th_sensor = dht.DHT11(Pin(D3))

# HCSR04, not work, TODO: later
#sr04 = HCSR04(trigger_pin=D7, echo_pin=D8)

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    '''
    Got a connection from ('10.107.85.22', 64869)
    Content = b'GET /favicon.ico HTTP/1.1\r\nHost: 10.107.85.21\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://10.107.85.21/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n'
    '''
    request = str(request)
    led_on = request.find('GET /?LED=ON')
    led_off = request.find('GET /?LED=OFF')
    buzzer_on = request.find('GET /?buzzer=on')
    buzzer_off = request.find('GET /?buzzer=off')
    buzzer_play = request.find('GET /?buzzer=play')
    servo_0 = request.find('GET /?servo=0')
    servo_90 = request.find('GET /?servo=90')
    servo_180 = request.find('GET /?servo=180')
    servo2_0 = request.find('GET /?servo2=0')
    servo2_90 = request.find('GET /?servo2=90')
    servo2_180 = request.find('GET /?servo2=180')
    servo3_0 = request.find('GET /?servo3=0')
    servo3_90 = request.find('GET /?servo3=90')
    servo3_180 = request.find('GET /?servo3=180')
    servo4_0 = request.find('GET /?servo4=0')
    servo4_90 = request.find('GET /?servo4=90')
    servo4_180 = request.find('GET /?servo4=180')
    th_sensor_read = request.find('GET /?th_sensor=read')
    sr04_read = request.find('GET /?sr04=read')
    runfile = request.find('GET /?runfile=')



    if led_on >= 0:
        print('TURN Led ON')
        led.value(0)
    if led_off >= 0:
        print('TURN Led OFF')
        led.value(1)
    if buzzer_on >= 0:
        print('buzzer on')
        Tune(buzzer, NOTE_C4, 10)
    if buzzer_off >= 0:
        print('buzzer off')
        Tune(buzzer, 0, 10)
    if buzzer_play >= 0:
        melody = [NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4, 0]
        print('buzzer play')
        for tn in melody:
            print('Tune:', tn)
            Tune(buzzer, tn, 500)
            #Tune(buzzer, 0, 100)
    if servo_0 >= 0:
        print('servo turn to 0')
        servo.duty(SV_ANGLE_0)
    if servo_90 >= 0:
        print('servo turn to 0')
        servo.duty(SV_ANGLE_90)
    if servo_180 >= 0:
        print('servo turn to 0')
        servo.duty(SV_ANGLE_180)
    if servo2_0 >= 0:
        print('servo2 turn to 0')
        servo2.duty(SV_ANGLE_0)
    if servo2_90 >= 0:
        print('servo2 turn to 0')
        servo2.duty(SV_ANGLE_90)
    if servo2_180 >= 0:
        print('servo2 turn to 0')
        servo2.duty(SV_ANGLE_180)
    if servo3_0 >= 0:
        print('servo3 turn to 0')
        servo3.duty(SV_ANGLE_0)
    if servo3_90 >= 0:
        print('servo3 turn to 0')
        servo3.duty(SV_ANGLE_90)
    if servo3_180 >= 0:
        print('servo3 turn to 0')
        servo3.duty(SV_ANGLE_180)
    if servo4_0 >= 0:
        print('servo4 turn to 0')
        servo4.duty(SV_ANGLE_0)
    if servo4_90 >= 0:
        print('servo4 turn to 0')
        servo4.duty(SV_ANGLE_90)
    if servo4_180 >= 0:
        print('servo4 turn to 0')
        servo4.duty(SV_ANGLE_180)
    my_t = None
    if th_sensor_read >= 0:
        print('th_sensor read')
        th_sensor.measure()
        my_t = th_sensor.temperature()
        print('T=', th_sensor.temperature())
        print('H=', th_sensor.humidity())
    my_distance = None
    if sr04_read >= 0:
        print('sr04 read')
        my_distance = -1 #sr04.distance_cm()
        print('distance=', my_distance)
    my_run_code_result = None
    if runfile >= 0:
        print('run file')
        try:
            file_name = request.split('\r\n', 1)[0].split('GET /?runfile=')[1].split()[0]
            print('file_name: ', file_name)
            if file_name in os.listdir():
                print('file got!')
                f = open(file_name)
                run_code = f.read()
                f.close()
                exec(run_code)
                my_run_code_result = 'OK'
            else:
                print('no file!')
                my_run_code_result = 'no file!'
        except Exception as ex:
            my_run_code_result = 'Exception:<br>[%s]%s' %(type(ex), str(ex))

    f = open('webtool.html')

    while(1):
        html = f.read(1024)

        if my_t:
            html = html.replace('T=?degree', 'T=%d degree' %(my_t))
        else:
            html = html.replace('T=?degree', '')
        if my_distance:
            html = html.replace('distance=? cm', 'distance=%s cm' %(my_distance))
        else:
            html = html.replace('distance=? cm', '')
        if my_run_code_result:
            html = html.replace('run result:', 'run result: %s' %(my_run_code_result))
        else:
            html = html.replace('run result:', '')
        #conn.send(html)
        conn.sendall(html) #改用send all就不會有資料傳一半的問題
        if(len(html)<=0):
            break
    f.close()
    conn.close()
