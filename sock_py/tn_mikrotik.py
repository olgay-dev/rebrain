#!/usr/bin/python3
import telnetlib
import time

HOST = '172.16.234.129'
PORT = 23
LOGIN = 'admin'
PASSWD = 'admin'
CMD = '/ip route print'

def tn_connect(host, port, login, password):
    tn = telnetlib.Telnet(host, port)
    tn_auth(tn, login, password)
    return tn

def tn_auth(tn, login, password):
    auth_try = 3
    auth_ok = False
    try:
        while auth_try > 0:
            r = tn.expect([b'Login:', b'Mikrotik Login:', b' > '], 5)
            tn.write(bytes(login, 'utf-8'))
            tn.write(b'\r\n')
            time.sleep(0.5)
            r = tn.expect([b'password:', b'PassWord:', b'Password:'], 5)
            tn.write(bytes(password, 'utf-8'))
            tn.write(b'\r\n')
            time.sleep(1)
            r = tn.expect([b' > '], 20)
            time.sleep(1)
            print(r)
            if r[0] == 0:
                auth_ok = True
                print('Auth OK')
                return
            else:
                print("Auth Failed")
                auth_try -= 1
    except Exception as e:
        logger.exception(f'error: {e}')

def tn_disconnect(tn):
    tn.write(b'quit\r\n')
    tn.close()

def main():
    tn = tn_connect(HOST, PORT, LOGIN, PASSWD)
    time.sleep(0.5)
    cmd = CMD
    tn.write(bytes(cmd, 'utf-8'))
    tn.write(b'\r\n')
    res = tn.read_until(bytes(' > ' + cmd + '\r\n', 'utf-8'), 2)
    res = tn.read_until(bytes(' > ', 'utf-8'), 2)
    print(res.decode('utf-8'))
    tn_disconnect(tn)
    
if __name__ == '__main__':
    main()
