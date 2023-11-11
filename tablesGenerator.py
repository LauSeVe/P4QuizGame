#!/usr/bin/env python3
import json

# Specify the path to your JSON file
json_file = "data.json"
output_file = "cli-command.txt"

try:
    # Open and read the JSON file
    with open(json_file, "r") as file:
        data = json.load(file)

    # Create the cli-commands.txt
    with open(output_file, "w") as file:

        # lvl1
        for item in data['lvl1']:
            id = item['Id']
            country = item['Country']
            answer1 = item['Answer1']
            answer2 = item['Answer2']
            answer3 = item['Answer3']
            correct_index = item['Correct']
            if (correct_index == 0):
                correct_answer = answer1
            elif (correct_index == 1):
                correct_answer = answer2
            elif (correct_index == 2):
                correct_answer = answer3
            formatted_content = f"table_add lvl1 lvl1Foward 0x{hex(id)[2:]} => 0x{country.encode('utf-8').hex()} 0x{answer1.encode('utf-8').hex()} 0x{answer2.encode('utf-8').hex()} 0x{answer3.encode('utf-8').hex()} 0x{correct_answer.encode('utf-8').hex()}\n"
            file.write(formatted_content)

        # lvl2
        for item in data['lvl2']:
            id = item['Id']
            country = item['Country']
            answer1 = item['Answer1']
            answer2 = item['Answer2']
            answer3 = item['Answer3']
            correct_index = item['Correct']
            if (correct_index == 0):
                correct_answer = answer1
            elif (correct_index == 1):
                correct_answer = answer2
            elif (correct_index == 2):
                correct_answer = answer3
            formatted_content = f"table_add lvl2 lvl2Foward 0x{hex(id)[2:]} => 0x{country.encode('utf-8').hex()} 0x{answer1.encode('utf-8').hex()} 0x{answer2.encode('utf-8').hex()} 0x{answer3.encode('utf-8').hex()} 0x{correct_answer.encode('utf-8').hex()}\n"
            file.write(formatted_content)

        # lvl3
        for item in data['lvl3']:
            id = item['Id']
            country = item['Country']
            answer1 = item['Answer1']
            answer2 = item['Answer2']
            answer3 = item['Answer3']
            correct_index = item['Correct']
            if (correct_index == 0):
                correct_answer = answer1
            elif (correct_index == 1):
                correct_answer = answer2
            elif (correct_index == 2):
                correct_answer = answer3
            formatted_content = f"table_add lvl3 lvl3Foward 0x{hex(id)[2:]} => 0x{country.encode('utf-8').hex()} 0x{answer1.encode('utf-8').hex()} 0x{answer2.encode('utf-8').hex()} 0x{answer3.encode('utf-8').hex()} 0x{correct_answer.encode('utf-8').hex()}\n"
            file.write(formatted_content)

        # lvl4
        for item in data['lvl4']:
            id = item['Id']
            country = item['Country']
            answer1 = item['Answer1']
            answer2 = item['Answer2']
            answer3 = item['Answer3']
            correct_index = item['Correct']
            if (correct_index == 0):
                correct_answer = answer1
            elif (correct_index == 1):
                correct_answer = answer2
            elif (correct_index == 2):
                correct_answer = answer3
            formatted_content = f"table_add lvl4 lvl4Foward 0x{hex(id)[2:]} => 0x{country.encode('utf-8').hex()} 0x{answer1.encode('utf-8').hex()} 0x{answer2.encode('utf-8').hex()} 0x{answer3.encode('utf-8').hex()} 0x{correct_answer.encode('utf-8').hex()}\n"
            file.write(formatted_content)
except Exception as e:
    print(f"An error occurred: {e}")

