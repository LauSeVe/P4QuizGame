#!/usr/bin/env python
import json
import random
import time

# Specify the path to your JSON file
json_file = "data.json"
output_file = "cli_command.txt"

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
    random_answer = random_question['Answer']

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
        exit()


    time.sleep(3)
    if (userAnswer == random_answer):
        print("Your answer was correct")
    else:
        print("Your answer was incorrect")


except Exception as e:
    print(f"An error occurred: {e}")


