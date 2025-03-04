import ollama


# generates and returns only the function
def generateFunction(functionPrompt):
    messageBaseEnd = "I want you to output ONLY the code, no descriptions, preambles, ''' above and below the code, etc"
    response = ollama.chat(model='codellama', 
    messages=[{
    'role': 'user',
    'content': functionPrompt + messageBaseEnd,
    },],
    keep_alive=False)
    return response['message']['content']


# passes given code to ollama to check if its valid
def validateCode(toWrite):
    print(toWrite + "\n")
    messageStart = "I want you to validate the following code. A simple yes or no will suffice for whether it is a combilable program (i dont care about logic errors) (no descriptions, preambles, etc)."
    
    print("startin\n")
    response = ollama.chat(model='codellama', messages=[{
    'role': 'user',
    'content': messageStart + toWrite,
    },],
    keep_alive=False)
    response = response['message']['content']
    print(response)
    
    if(response[0] == "y" or response[0] == "Y"):
        print("we good")
        return True
    print("something is off")
    return False


# calls generate function and writes the result to a specified file
def writeFunction(functionPrompt, file_path):
    validCode = False
    i = 0
    if(not validCode and i < 3):
        function = generateFunction(functionPrompt)
        
        # Split the input string into lines
        lines = function.split('\n')
        
        # Exclude the first and last lines
        lines_to_append = lines[1:-1]
        toWrite = ""
        for line in lines_to_append:
                toWrite += line + "\n"
        
        validCode = validateCode(toWrite)
        i += 1
        if(not validCode and i >= 2):
            print("something is off\n")
    
    # Open the file in append mode ('a') to avoid overwriting
    with open(file_path, 'a') as file:
        # Write each of the lines to the file
        file.write(toWrite)

            
        
            
            
writeFunction("write a function to add two numbers", "./functionNames.txt")

