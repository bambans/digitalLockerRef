from machine import Pin, PWM
import esp, gc

from digitalLocker_libray import wifi_connector, socket_connector, socket_accept, socket_request, web_page, socket_response

def startServer():
    esp.osdebug(None)
    gc.collect()

    wifi_connector('NameOfNetworkTP', '0123456789')

    p25 = Pin(25, Pin.OUT)
    motor = PWM(p25, freq=50)
    motor.duty(40)
    locker_state = "OFF"

    s = socket_connector(3000, 2)

    while True:
        conn = socket_accept(s)

        request = socket_request(conn, 1024)

        locker_on = request.find('/?locker=on')
        locker_off = request.find('/?locker=off')

        if locker_on == 6:
            print('LOCKER ON')
            motor.duty(110)
            locker_state = "ON"
        if locker_off == 6:
            print('LOCKER OFF')
            motor.duty(40)
            locker_state = "OFF"

        response = web_page('page.html','""" + locker_state + """', locker_state)

        socket_response(conn, response)
