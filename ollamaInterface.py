import ollama
import functionNames
import importlib
import sys

funcName = ""


# generates and returns only the function
def generateFunction(functionPrompt):
    messageBaseEnd = "I want you to output ONLY the code, no descriptions, preambles, ''' above and below the code, etc"
    response = ollama.chat(
        model="codellama",
        messages=[
            {
                "role": "user",
                "content": functionPrompt + messageBaseEnd,
            },
        ],
        keep_alive=False,
    )
    return response["message"]["content"]


# passes given code to ollama to check if its valid
def validateCode(toWrite):
    messageStart = "I want you to validate the following code. Valid code means a fully bodied python function that will run with no issues as is given the neccesary inputs (dont care about logic errors). Presumably, any code that is only a function declaration will not be valid code. A simple yes or no will suffice for whether it is a compilable program (i dont care about logic errors) (no descriptions, preambles, etc)."
    response = ollama.chat(
        model="codellama",
        messages=[
            {
                "role": "user",
                "content": messageStart + toWrite,
            },
        ],
        keep_alive=False,
    )
    response = response["message"]["content"]
    if "yes" in response or "Yes" in response:
        return True
    return False


# calls generate function and writes the result to a specified file
def writeFunction(functionPrompt, file_path):
    function = generateFunction(functionPrompt)

    # Split the input string into lines
    lines = function.split("\n")

    startLine = 0
    endLine = len(lines) - 1
    while not "def" in lines[startLine]:
        startLine += 1

    while lines[endLine][0].__eq__("'"):
        endLine -= 1

    lines_to_append = lines[startLine:endLine]
    toWrite = ""
    for line in lines_to_append:
        toWrite += line + "\n"

    # get the name of the function
    funcName = lines[startLine]
    # get rid of the def portion
    funcName = funcName.split(" ")
    funcName = funcName[1]
    # get rid of (): portion
    end = len(funcName) - 3
    funcName = funcName[0:end]

    # Open the file in append mode ('a') to avoid overwriting
    with open(file_path, "a") as file:
        # Write each of the lines to the file
        file.write(toWrite)
        file.flush

    print("func Name :: " + funcName)
    loadFunction()
    print(call_generated_function())


def loadFunction():
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(funcName, "./functionNames.py")
    generated_method = importlib.util.module_from_spec(spec)
    sys.modules[funcName] = generated_method
    spec.loader.exec_module(generated_method)

    # Dynamically get the function name from the generated code
    # The generated function name should be the first function defined in the file
    function_name = None
    for attr_name in dir(generated_method):
        if callable(getattr(generated_method, attr_name)):
            function_name = attr_name
            break

    if function_name is None:
        raise ValueError("No callable function found in the generated module.")

    return generated_method, function_name


def call_generated_function():
    # Load the function and get the function name
    generated_method, function_name = loadFunction()

    # Get the function object dynamically
    dynamic_function = getattr(generated_method, function_name)

    # Call the function (with arguments, for example: 5, 3)
    result = dynamic_function(5, 2)
    print(f"Result of dynamic function: {result}")


writeFunction(
    "write a function to subtract two numbers",
    "./functionNames.py",
)
