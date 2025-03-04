import ollama


response = ollama.chat(model='llama3', messages=[{
    'role': 'user',
    'content': 'Why is the sky blue? (explain in one sentence)',
    },])


print(response['message']['content'])def add_two_numbers(num1, num2):
    return num1 + num2
