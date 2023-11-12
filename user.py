#!/usr/bin/env python3

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import random
import os
import time
from headers import *

def wait_for_file(file_path, timeout=60, interval=1):
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            return False
        time.sleep(interval)
    return True

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

    # Create the header to request the quiz
    userSession = random.randint(0, 15)
    packetQuestion="Spain"
    packetAnswer1="Madrid"
    packetAnswer2="Spain"
    packetAnswer3="Spain"

    bind_layers(Ether, QuizHeaderRequest, type=TYPE_QUIZ_REQUEST)
    custom_packet_request = Ether(type = TYPE_QUIZ_REQUEST) / QuizHeaderRequest(session=userSession, type=00, lvl = userLevel, question=packetQuestion, answer1=packetAnswer1, answer2=packetAnswer2, answer3=packetAnswer3) 
    request_packet_in = "./requestQuiz/packet_in.pcap"
    wrpcap(request_packet_in, custom_packet_request)

    # Wait until packet_out is created
    request_packet_out = "./requestQuiz/packet_out.pcap"
    if wait_for_file(request_packet_out):
    # Print the question and options from the packet_out
        packets = rdpcap(request_packet_out)
        for packet in packets:
            print(packet.summary())
            packet.show()
            if QuizHeaderRequest in packet:
                quizHeaderRequest = packet[QuizHeaderRequest]
                session_request = quizHeaderRequest.session
                type_request = quizHeaderRequest.type
                lvl_request = quizHeaderRequest.lvl
                question_text_request = quizHeaderRequest.question.decode('utf-8').split('\x00')[0]
                print(f"Which is the capital of {question_text_request}?")
                answer1_text_request = quizHeaderRequest.answer1.decode('utf-8').split('\x00')[0]
                print(f"a. {answer1_text_request}")
                answer2_text_request = quizHeaderRequest.answer2.decode('utf-8').split('\x00')[0]
                print(f"b. {answer2_text_request}")
                answer3_text_request = quizHeaderRequest.answer3.decode('utf-8').split('\x00')[0]
                print(f"c. {answer3_text_request}")
    else:
    # Handle the case when the timeout is reached
        print("File not created within the specified timeout.")
        exit()
    
    # Prompt the user to select an option
    user_answer = input("Select the option: ")

    # Check if user_answer is 'A', 'B', or 'C'
    if (user_answer.upper() == 'A'):
        userAnswer = answer1_text_request
    elif (user_answer.upper() == 'B'):
        userAnswer = answer2_text_request
    elif (user_answer.upper() == 'C'):
        userAnswer = answer3_text_request
    else:
        print("Invalid input. Please enter 'A', 'B', or 'C'.")
        exit()


    # Create the header to reply the quiz
    bind_layers(Ether, QuizHeaderRequest, type=TYPE_QUIZ_REPLY)
    custom_packet_reply = Ether(type = TYPE_QUIZ_REPLY) / QuizHeaderReply(session=session_request, type=2, lvl=lvl_request, question=question_text_request, user_answer=userAnswer) 
    reply_packet_in = "./replyQuiz/packet_in.pcap"
    wrpcap(reply_packet_in, custom_packet_reply)



except Exception as e:
    print(f"An error occurred: {e}")

