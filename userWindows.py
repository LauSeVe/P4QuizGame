import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import tkinter as tk
from tkinter import ttk
from scapy.all import *
import random
import os
from headers import *

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P4QuizGame")
        self.root.geometry('500x250')

        # Paths
        self.path_packet_in = "./P4/test-case1/packets_in.pcap"
        self.path_packet_out = "./P4/test-case1/packets_out.pcap"
        
        self.session_request = 0
        # Page
        self.welcomeLabel = tk.Label(self.root, text="Welcome to P4QuizGame, there are 4 levels \n \nChoose the level you want to play with:")
        self.welcomeLabel.pack(pady=10)

        self.button0 = tk.Button(self.root, text="lvl1", command=lambda:self.lvlButton(0))
        self.button0.pack(pady=10)
        
        self.button1 = tk.Button(self.root, text="lvl2", command=lambda:self.lvlButton(1))
        self.button1.pack(pady=10)
        
        self.button2 = tk.Button(self.root, text="lvl3", command=lambda:self.lvlButton(2))
        self.button2.pack(pady=10)
        
        self.button3 = tk.Button(self.root, text="lvl4", command=lambda:self.lvlButton(3))
        self.button3.pack(pady=10)
    
    
    def playAgain(self):
        self.welcomeLabel.pack_forget()
        self.button0.pack_forget()
        self.button1.pack_forget() 
        self.button2.pack_forget()
        self.button3.pack_forget()
        
        self.session_request = 0
        # Page
        self.welcomeLabel = tk.Label(self.root, text="Welcome to P4QuizGame, there are 4 levels \n \nChoose the level you want to play with:")
        self.welcomeLabel.pack(pady=10)

        self.button0 = tk.Button(self.root, text="lvl1", command=lambda:self.lvlButton(0))
        self.button0.pack(pady=10)
        
        self.button1 = tk.Button(self.root, text="lvl2", command=lambda:self.lvlButton(1))
        self.button1.pack(pady=10)
        
        self.button2 = tk.Button(self.root, text="lvl3", command=lambda:self.lvlButton(2))
        self.button2.pack(pady=10)
        
        self.button3 = tk.Button(self.root, text="lvl4", command=lambda:self.lvlButton(3))
        self.button3.pack(pady=10)
        
        os.system("rm ./P4/test-case1/packets_in.pcap")
        os.system("rm ./P4/test-case1/packets_out.pcap")
        
    
    def wait_for_file(self, timeout=60, interval=1):
        start_time = time.time()
        while not os.path.exists(self.path_packet_out):
            print(start_time)
            if time.time() - start_time > timeout:
                return False
            time.sleep(interval)
        return True
           
    def replyOut(self):
        # Wait until reply_packet_out is created
        if self.wait_for_file():
            # Print the question and options from the packet_out
            packets = rdpcap(self.path_packet_out)
            for packet in packets:
                if QuizHeaderReply in packet:
                    quizHeaderReply = packet[QuizHeaderReply]
                    session_reply = quizHeaderReply.session
                    type_reply = quizHeaderReply.type
                    correct_reply = quizHeaderReply.correct
                    correct_text_reply = quizHeaderReply.user_answer.decode('utf-8').split('\x00')[0]
                    question_text_reply = quizHeaderReply.question.decode('utf-8').split('\x00')[0]
                    if (correct_reply == 1):
                        self.welcomeLabel.config(text="Congratulations, you got it right! \n\nThe capital of " + str(question_text_reply) +" is " + str(correct_text_reply))
                    elif (correct_reply == 2):
                        self.welcomeLabel.config(text="You have failed, keep playing. \n\nThe capital of " + str(question_text_reply) +" is " + str(correct_text_reply))
                    else:
                        print(f"There was a problem \n\nThe capital of " + str(question_text_reply) +" is " + str(correct_text_reply))
                        
                    self.button0.pack(pady=10)
                    self.button0.config(text = "Play again", command=lambda:self.playAgain())
        
    def answerButton(self, question_text_request, userAnswer):
        os.system("cp ./P4/test-case1/packets_in.pcap ./P4/test-case1/packets0.pcap")
        os.system("rm ./P4/test-case1/packets_in.pcap")
        os.system("cp ./P4/test-case1/packets_out.pcap ./P4/test-case1/packets1.pcap")
        os.system("rm ./P4/test-case1/packets_out.pcap")
    
        # Create the header to reply the quiz
        correct_reply_packet = 0;
        bind_layers(Ether, QuizHeaderReply, type=TYPE_QUIZ_REPLY)
        custom_packet_reply = Ether(type = TYPE_QUIZ_REPLY) / QuizHeaderReply(session=self.session_request, type=2, correct=correct_reply_packet, question=question_text_request, user_answer=userAnswer) 
        wrpcap(self.path_packet_in, custom_packet_reply)
        
        self.welcomeLabel.config(text="Checking the answer...")
        self.button1.pack_forget() 
        self.button2.pack_forget()
        self.button3.pack_forget()  
        
        root.after(100,self.replyOut)


    def requestOut(self): 
        if self.wait_for_file():
        # Print the question and options from the packet_out
            packets = rdpcap(self.path_packet_out)
            for packet in packets:
                if QuizHeaderRequest in packet:
                    quizHeaderRequest = packet[QuizHeaderRequest]
                    self.session_request = quizHeaderRequest.session
                    type_request = quizHeaderRequest.type
                    lvl_request = quizHeaderRequest.lvl
                    question_text_request = quizHeaderRequest.question.decode('utf-8').split('\x00')[0]
                    self.welcomeLabel.config(text="Which is the capital of " +  str(question_text_request) + "?")
                    answer1_text_request = quizHeaderRequest.answer1.decode('utf-8').split('\x00')[0]
                    self.button1.pack(pady=10)
                    self.button1.config(text= "a. " +  str(answer1_text_request), command=lambda:self.answerButton(question_text_request, 1))
                    answer2_text_request = quizHeaderRequest.answer2.decode('utf-8').split('\x00')[0]
                    self.button2.pack(pady=10)
                    self.button2.config(text= "b. " +  str(answer2_text_request), command=lambda:self.answerButton(question_text_request, 2))
                    answer3_text_request = quizHeaderRequest.answer3.decode('utf-8').split('\x00')[0]
                    self.button3.pack(pady=10)
                    self.button3.config(text= "c. " +  str(answer3_text_request), command=lambda:self.answerButton(question_text_request, 3))
        else:
        # Handle the case when the timeout is reached
            print("File not created within the specified timeout.")
            exit

    def lvlButton(self, userLevel):       
        # Create the header to request the quiz
        userSession = random.randint(0, 15)
        packetQuestion = {userSession}
        packetAnswer1= {userSession}
        packetAnswer2= {userSession}
        packetAnswer3= {userSession}

        bind_layers(Ether, QuizHeaderRequest, type=TYPE_QUIZ_REQUEST)
        custom_packet_request = Ether(type = TYPE_QUIZ_REQUEST) / QuizHeaderRequest(session=userSession, type=0, lvl=userLevel, question=packetQuestion, answer1=packetAnswer1, answer2=packetAnswer2, answer3=packetAnswer3)
        wrpcap(self.path_packet_in, custom_packet_request)
        
        self.welcomeLabel.config(text="Waiting for the question...")
        self.button0.pack_forget() 
        self.button1.pack_forget() 
        self.button2.pack_forget()
        self.button3.pack_forget()  
        
        root.after(100,self.requestOut)

        
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
