import network
def wifi_connector(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while station.isconnected() == False:
      pass
    print('Connection successful')
    print(station.ifconfig())

# try:
#   import usocket as socket
# except:
import socket
def socket_connector(port, listen):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(listen)
    return s

def socket_accept(s):
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    return conn

def socket_request(conn, request_size):
    request = conn.recv(request_size)
    request = str(request)
    print('Content = %s' % request)
    return request

def web_page(file_address, replace_string, locker_state):
    with open(file_address, 'r') as f:
        html = f.read().replace(replace_string, locker_state)
        return html

def socket_response(conn, response):
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()