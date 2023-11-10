#!/usr/bin/env python 
import json
import random
from scapy.all import Packet, BitField

# Specify the path to your JSON file
json_file = "data.json"
output_file = "cli-command.txt"

try:
    # Open and read the JSON file
    with open(json_file, "r") as file:
        data = json.load(file)

    # Create the cli-commands.txt
    with open(output_file, "w") as file:

        for item in data['capitals']:
            id = item['Id']
            country = item['Country']
            options = item['Options']
            correct_answer_index = item['Answer']
            correct_answer = options[correct_answer_index]

            formatted_content = f"table_add capitals realAnswers 0x{hex(id)[2:]} => 0x{hex(correct_answer_index)[2:]}\n"
            file.write(formatted_content)

    # Select a random question
    random_question = random.choice(data['capitals'])
    random_id = random_question['Id']
    random_country = random_question['Country']
    random_options = random_question['Options']

    # Print the question
    print(f"Country: {random_country}")
    print(f"Options:")
    for i, option in enumerate(random_options):
        print(f"{option}")
    print()

    # Prompt the user to select an option
    user_answer = input("Select the option number: ")

    # Check if user_answer is 'A', 'B', or 'C'
    if (user_answer.upper() == 'A'):
        userAnswer = 0
    elif (user_answer.upper() == 'B'):
        userAnswer = 1
    elif (user_answer.upper() == 'C'):
        userAnswer = 2
    else:
        print("Invalid input. Please enter 'A', 'B', or 'C'.")

    # Create my header with scapy
    class MyCustomHeader(Packet):
        name = "quizHeader"
        fields_desc = [
            BitField("question", 0, 4),
            BitField("answeruser", 0, 2),
            BitField("correct", 0, 2),
        ]

        def my_custom_method(self):
            return f"Question: {self.question}, User Answer: {self.answeruser}, Correct: {self.correct}"

        custom_packet = Ether() / MyCustomHeader(question={hex(random_id)[2:]}, answeruser={hex(userAnswer)[2:]}, correct=0)

except Exception as e:
    print(f"An error occurred: {e}")


