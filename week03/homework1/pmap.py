import threading
import argparse
import socket
import time
import sys
import os


def helper():
    print("""Usage:
    pmap.py [-h] -n NUMBER -f FUNCTION -ip IP [-w WRITE]
Examples:
    pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100
    pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json
Please make sure the target IPs are in the same subnet of x.x.x.x/24""")
    sys.exit(1)


def logger(message):

    global RESULT_FILE

    print(message)

    if RESULT_FILE:
        with open(RESULT_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{message}\n')


def main(args):

    global semaphore
    semaphore = threading.BoundedSemaphore(args.number)
    localtime = time.strftime(f'%Y-%m-%d %H:%M:%S', time.localtime())

    if args.ip.find('-') != -1:
        ip_start = args.ip.split('-')[0]
        ip_end = args.ip.split('-')[1]
    else:
        ip_start = args.ip
        ip_end = ''

    ip_start_parts = ip_start.split('.')
    if len(ip_start_parts) != 4:
        print(f'Invalid IP address!')
        helper()

    if ip_end:
        ip_end_parts = ip_end.split('.')
        if len(ip_end_parts) != 4:
            print(f'Invalid IP address!')
            helper()

    if args.function == 'ping':
        if not ip_end:
            helper()

        for i in range(0, 3):
            if ip_start_parts[i] != ip_end_parts[i]:
                helper()
        
        subnet = ('.').join([ip_start_parts[i] for i in range(0, 3)])

        logger(f'############### [{localtime}] ping test starts ###############')
        for i in range( int(ip_start_parts[3]), int(ip_end_parts[3])+1 ):
            ip = f'{subnet}.{str(i)}'
            t = threading.Thread(target=ping_test, args=(ip,))
            t.start()

    elif args.function == 'tcp':
        if ip_end:
            helper()

        logger(f'############### [{localtime}] tcp test against {ip_start} starts ###############')
        for port in range(1, 1025):
            t = threading.Thread(target=tcp_test, args=(ip_start, port))
            t.start()

    else:
        helper()


def ping_test(ip):

    semaphore.acquire()

    result = os.popen(f'ping -c 2 -t 2 {ip}').read()
    if 'ttl' in result:
        logger(f'{ip} is reachable')

    semaphore.release()


def tcp_test(ip, port):

    semaphore.acquire()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((ip, port))
    except Exception:
        pass
    else:
        logger(f'port {port} is open')
    finally:
        sock.close()
        semaphore.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, required=True, default=1, help='number of concurrency')
    parser.add_argument('-f', '--function', type=str, required=True, help='ping or tcp')
    parser.add_argument('-ip', type=str, required=True, help='target IPs')
    parser.add_argument('-w', '--write', type=str, help='file to store results')
    args = parser.parse_args()

    RESULT_FILE = ''
    if args.write:
        RESULT_FILE = args.write

    main(args)
