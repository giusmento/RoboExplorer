import socket
import binascii

def main():
  MCAST_GRP = '224.0.0.1'
  MCAST_PORT = 5007
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
  sock.sendto(b'Hello World!', (MCAST_GRP, MCAST_PORT))
  while 1:
      try:
          data, addr = sock.recvfrom(1024)
          hexdata = binascii.hexlify(data)
          print('Data = %s' % hexdata)
      except socket.error:
          print('Expection')
          hexdata = binascii.hexlify(data)
          print('Data = %s' % hexdata)

if __name__ == '__main__':
  main()