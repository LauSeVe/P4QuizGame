#!/usr/bin/env python3
from scapy.all import *
import random

try:
    # Print the question
    print(f"Welcome to P4QuizGame, there are 4 levels")
    print(f"a. lvl1")
    print(f"b. lvl2")
    print(f"c. lvl3")
    print(f"d. lvl4")

    # Prompt the user to select an option
    user_lvl = input("Choose the level you want to play with: ")

    # Check if user_lvl is correct
    if (user_lvl.upper() == 'A' or user_lvl.upper() == "LVL1" or user_lvl=="1"):
        userLevel = 0
    elif (user_lvl.upper() == 'B' or user_lvl.upper() == "LVL2" or user_lvl=="2"):
        userLevel = 1
    elif (user_lvl.upper() == 'C' or user_lvl.upper() == "LVL3" or user_lvl=="3"):
        userLevel = 2
    elif (user_lvl.upper() == 'D' or user_lvl.upper() == "LVL4" or user_lvl=="4"):
        userLevel = 3
    else: 
        print("Invalid input.")
        exit()

    # Create my header with scapy
    class QuizHeader0(Packet):
        name = "QuizHeader0"
        fields_desc = [
            BitField("session", 0, 4),
            BitField("type", 0, 2),
            BitField("lvl", 0, 2),
            StrFixedLenField("question", b"\x00" * 20, length=20),
            StrFixedLenField("answer1", b"\x00" * 20, length=20),
            StrFixedLenField("answer2", b"\x00" * 20, length=20),
            StrFixedLenField("answer3", b"\x00" * 20, length=20),
        ]
    
    userSession = random.randint(0, 15)
    packetType=00
    packetQuestion=0
    packetAnswer1=0
    packetAnswer2=0
    packetAnswer3=0

    custom_packet = Ether() / QuizHeader0(session=userSession, type=packetType, lvl = userLevel, question=packetQuestion, answer1=packetAnswer1, answer2=packetAnswer2, answer3=packetAnswer3) 
    pcap_file = "packet0.pcap"
    wrpcap(pcap_file, custom_packet)

except Exception as e:
    print(f"An error occurred: {e}")

