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
            id_num = item['Id']
            id = "0x0"+ hex(id_num)[2:] + "0"*(38)

            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes

            answer1 = item['Answer1']
            answer1_extra_bytes = 20 - len(answer1.encode("utf-8"))
            answer1_bytes = answer1.encode("utf-8") + b'\x00' * answer1_extra_bytes

            answer2 = item['Answer2']
            answer2_extra_bytes = 20 - len(answer2.encode("utf-8"))
            answer2_bytes = answer2.encode("utf-8") + b'\x00' * answer2_extra_bytes

            answer3 = item['Answer3']
            answer3_extra_bytes = 20 - len(answer3.encode("utf-8"))
            answer3_bytes = answer3.encode("utf-8") + b'\x00' * answer3_extra_bytes

            formatted_content = f"table_add lvl1 lvl1Forward {id} => 0x{country_bytes.hex()} 0x{answer1_bytes.hex()} 0x{answer2_bytes.hex()} 0x{answer3_bytes.hex()} \n"
            file.write(formatted_content)

        # lvl2
        for item in data['lvl2']:
            id_num = item['Id']
            id =   "0x0"+ hex(id_num)[2:] + "0"*(38)

            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes

            answer1 = item['Answer1']
            answer1_extra_bytes = 20 - len(answer1.encode("utf-8"))
            answer1_bytes = answer1.encode("utf-8") + b'\x00' * answer1_extra_bytes

            answer2 = item['Answer2']
            answer2_extra_bytes = 20 - len(answer2.encode("utf-8"))
            answer2_bytes = answer2.encode("utf-8") + b'\x00' * answer2_extra_bytes

            answer3 = item['Answer3']
            answer3_extra_bytes = 20 - len(answer3.encode("utf-8"))
            answer3_bytes = answer3.encode("utf-8") + b'\x00' * answer3_extra_bytes

            formatted_content = f"table_add lvl2 lvl2Forward {id}  => 0x{country_bytes.hex()} 0x{answer1_bytes.hex()} 0x{answer2_bytes.hex()} 0x{answer3_bytes.hex()} \n"
            file.write(formatted_content)
        # lvl3
        for item in data['lvl3']:
            id_num = item['Id']
            id =   "0x0"+ hex(id_num)[2:] + "0"*(38)

            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes

            answer1 = item['Answer1']
            answer1_extra_bytes = 20 - len(answer1.encode("utf-8"))
            answer1_bytes = answer1.encode("utf-8") + b'\x00' * answer1_extra_bytes

            answer2 = item['Answer2']
            answer2_extra_bytes = 20 - len(answer2.encode("utf-8"))
            answer2_bytes = answer2.encode("utf-8") + b'\x00' * answer2_extra_bytes

            answer3 = item['Answer3']
            answer3_extra_bytes = 20 - len(answer3.encode("utf-8"))
            answer3_bytes = answer3.encode("utf-8") + b'\x00' * answer3_extra_bytes

            formatted_content = f"table_add lvl3 lvl3Forward {id}  => 0x{country_bytes.hex()} 0x{answer1_bytes.hex()} 0x{answer2_bytes.hex()} 0x{answer3_bytes.hex()} \n"
            file.write(formatted_content)

        # lvl4
        for item in data['lvl4']:
            id_num = item['Id']
            id = "0x0"+ hex(id_num)[2:] + "0"*(38)

            country = item['Country']
            country_extra_bytes = 20 - len(country.encode("utf-8"))
            country_bytes = country.encode("utf-8") + b'\x00' * country_extra_bytes

            answer1 = item['Answer1']
            answer1_extra_bytes = 20 - len(answer1.encode("utf-8"))
            answer1_bytes = answer1.encode("utf-8") + b'\x00' * answer1_extra_bytes

            answer2 = item['Answer2']
            answer2_extra_bytes = 20 - len(answer2.encode("utf-8"))
            answer2_bytes = answer2.encode("utf-8") + b'\x00' * answer2_extra_bytes

            answer3 = item['Answer3']
            answer3_extra_bytes = 20 - len(answer3.encode("utf-8"))
            answer3_bytes = answer3.encode("utf-8") + b'\x00' * answer3_extra_bytes

            formatted_content = f"table_add lvl4 lvl4Forward {id}  => 0x{country_bytes.hex()} 0x{answer1_bytes.hex()} 0x{answer2_bytes.hex()} 0x{answer3_bytes.hex()} \n"
            file.write(formatted_content)

        formatted_content = f"\n \n # run traffic \n \n run_traffic packets \n \n #end \n \n exit \n"
        file.write(formatted_content)

except Exception as e:
    print(f"An error occurred: {e}")
