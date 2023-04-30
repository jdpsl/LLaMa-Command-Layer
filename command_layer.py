import subprocess
import json
import os
import fcntl

# Run a command that expects input from stdin and returns JSON output
cmd = ["./main", "-m", "./models/alpaca-13b-tool-ggml-q4_0.bin", "--color", "-f", "./prompts/tool.txt", "--ctx_size", "2048", "-n", "-1", "-ins", "-b", "256", "--top_k", "10000", "--temp", "0.2", "--repeat_penalty", "1", "-t", "7"]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

# Set the output stream to non-blocking mode

#fcntl.fcntl(proc.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

# Loop continuously to read input from the user and pass it to the subprocess
while True:
    # Print any output from the subprocess
    try:
        output_str = proc.stdout.read().decode().strip()
        if output_str:
            try:
                # Parse the JSON output as a Python dictionary
                output_dict = json.loads(output_str)

                # Access specific values in the dictionary
                thoughts = output_dict['thoughts']
                command = output_dict['command']
                thought_text = thoughts['text']
                thought_reasoning = thoughts['reasoning']
                thought_plan = thoughts['plan']
                thought_criticism = thoughts['criticism']
                thought_speak = thoughts['speak']
                command_name = command['name']
                command_args = command['args']

                # Print the values to the console
                print("Thoughts text:", thought_text)
                print("Thoughts reasoning:", thought_reasoning)
                print("Thoughts plan:", thought_plan)
                print("Thoughts criticism:", thought_criticism)
                print("Thoughts speak:", thought_speak)
                print("Command name:", command_name)
                print("Command args:", command_args)
            except json.JSONDecodeError:
                # If the output is not JSON-formatted, print it as plain text
                print(output_str)
    except:
        pass

    # Read a line of input from the user
    input_str = input("")

    # Exit the loop if the user enters 'exit'
    if input_str == '.exit':
        break

    # Pass the input to the subprocess
    proc.stdin.write(input_str.encode() + b"\n")
    proc.stdin.flush()

# Terminate the subprocess when the loop is finished
proc.terminate()
