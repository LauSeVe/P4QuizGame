#!/usr/bin/env python3
import json

# Specify the path to your JSON file
json_file = "../data.json"
output_file = "./test-case1/cli_commands.txt"

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
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes
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
            correct_answer_extra_bytes = 20 - len(correct_answer.encode("utf-8"))
            correct_answer_bytes = correct_answer.encode("utf-8") + b'\x00' * correct_answer_extra_bytes
            formatted_content = f"table_add comprobation forwardPacket 0x{country_bytes.hex()} => 0x{correct_answer_bytes.hex()} \n"
            file.write(formatted_content)

        # lvl2
        for item in data['lvl2']:
            id = item['Id']
            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes
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
            correct_answer_extra_bytes = 20 - len(correct_answer.encode("utf-8"))
            correct_answer_bytes = correct_answer.encode("utf-8") + b'\x00' * correct_answer_extra_bytes
            formatted_content = f"table_add comprobation forwardPacket 0x{country_bytes.hex()} => 0x{correct_answer_bytes.hex()} \n"
            file.write(formatted_content)

        # lvl3
        for item in data['lvl3']:
            id = item['Id']
            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes
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
            correct_answer_extra_bytes = 20 - len(correct_answer.encode("utf-8"))
            correct_answer_bytes = correct_answer.encode("utf-8") + b'\x00' * correct_answer_extra_bytes
            formatted_content = f"table_add comprobation forwardPacket 0x{country_bytes.hex()} => 0x{correct_answer_bytes.hex()} \n"
            file.write(formatted_content)

        # lvl4
        for item in data['lvl4']:
            id = item['Id']
            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes
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
            correct_answer_extra_bytes = 20 - len(correct_answer.encode("utf-8"))
            correct_answer_bytes = correct_answer.encode("utf-8") + b'\x00' * correct_answer_extra_bytes
            formatted_content = f"table_add comprobation forwardPacket 0x{country_bytes.hex()} => 0x{correct_answer_bytes.hex()} \n"
            file.write(formatted_content)

        formatted_content = f"\n # run traffic \n run_traffic packets \n #end \n exit \n"
        file.write(formatted_content)

except Exception as e:
    print(f"An error occurred: {e}")
