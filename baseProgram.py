import functions
import os
import subprocess

os.environ["PATH"] = os.pathsep.join(os.environ["PATH"].split(os.pathsep))

# x = input("Enter Operand 1")
# y = input("Enter Operand 2")
# operation = input("What operation do you want to do")


# Create the process for cmd.exe
process = subprocess.Popen(
    "cmd.exe",
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# Send command to the process (instead of using communicate)
# process.stdin.write("ollama serve\n")
# process.stdin.flush()
process.stdin.write("ollama run llama3\n")  # Add a newline to simulate pressing Enter
process.stdin.flush()  # Flush the input buffer to make sure the data is sent

# Optionally, you can read the output or error
stdout, stderr = process.communicate()  # This will capture all output

# Print the output
print("Output:")
print(stdout)

# Print errors (if any)
if stderr:
    print("Error:")
    print(stderr)

while 1 == 1:
    x = input("$: ")
    process.stdin.write(x + "\n")
    process.stdin.flush()
    # Optionally, you can read the output or error
stdout, stderr = process.communicate()  # This will capture all output

# Print the output
print("Output:")
print(stdout)

# Print errors (if any)
if stderr:
    print("Error:")
    print(stderr)
