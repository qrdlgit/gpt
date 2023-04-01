import requests
import json
import time
import qoai
import re
import subprocess
import os

def evaluate_solution():
    # Save the solution in a file
    solution_filename = 'generated_solution.py'

    # Execute the solution and capture the output
    try:
        output = subprocess.check_output(['python3', solution_filename], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Clean up the generated solution file
    with open('output', 'w') as f:
        f.write(output)
    # Parse the JSON output and return the metrics
    


def append_strings_from_tag_to_file(input_string, output_filename):
    pattern = r'<obs>(.*?)</obs>'
    matches = re.findall(pattern, input_string, re.DOTALL)

    if matches:
        try:
            strings = json.loads(matches[0])
            with open(output_filename, 'a') as file:
                for string in strings:
                    file.write(f"{string}\n")
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON from <obs> tags: {matches[0]}")
    else:
        print("Error: No <obs> tags found in the input string.")

               

def extract_json_between_embed_tags(response_text):
    pattern = r'<embed>(.*?)</embed>'
    matches = re.findall(pattern, response_text, re.DOTALL)

    if matches:
        try:
            extracted_json = json.loads(matches[0])
            return extracted_json
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON from <embed> tags: {matches[0]}")
            return []
    else:
        print("Error: No <embed> tags found in the response text.")
        return []

def apply_replacements(replacements, input_filename, output_filename):
    replacements = extract_json_between_embed_tags(replacements)
    with open(input_filename, 'r') as file:
        file_contents = file.read()

    for replacement in replacements:
        file_contents = file_contents.replace(replacement['find'], replacement['replace'])

    with open(output_filename, 'w') as file:
        file.write(file_contents)
        

def concatenate_files_with_prefixes(files):
    result = ''
    for prefix, filename in files:
        try:
            with open(filename, 'r') as file:
                file_contents = file.read()
            result += f"{prefix}{file_contents}"
        except FileNotFoundError:
            print(f"Error: Could not find the file '{filename}'")
    return result


def do_ml(iterations = 1):
    
    for i in range(iterations):
        current_prompt = concatenate_files_with_prefixes([('''
        Use the sklearn.datasets.load_breast_cancer to predict breast.  Here is the code that just ran:
        ''', 'generated_solution.py'), ('''here are evaluation metrics from running this code.
        ''', 'output'), ('''here is a list of observations made about previous changes
        ''', 'observations'), ('''
        ''', 'prompt')])
        
        print(f"Iteration: {i + 1}")
        print(f"current_prompt: {current_prompt}")
        solution = qoai.get_response(current_prompt)
        print(f"Solution: {solution}")
        append_strings_from_tag_to_file(solution, 'observations')        
        apply_replacements(solution, 'generated_solution.py', 'generated_solution.py')
        evaluate_solution()
        
        time.sleep(1)  # Sleep to avoid hitting rate limits
