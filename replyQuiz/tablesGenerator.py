#!/usr/bin/env python3
import json

# Specify the path to your JSON file
json_file = "../data.json"
output_file = "./test-case1/cli_commands.txt"

try:
    # Open and read the JSON file
    with open(json_file, "r") as file:
        data = json.load(file)

    # Create the cli_commands.txt
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
            formatted_content = f"table_add comprobation forwardPacket 0x{country.encode('utf-8').hex()} => 0x{correct_answer.encode('utf-8').hex()} \n"
            file.write(formatted_content)
except Exception as e:
    print(f"An error occurred: {e}")

