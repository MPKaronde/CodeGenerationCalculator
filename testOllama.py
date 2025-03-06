import ollama


response = ollama.chat(model='llama3', messages=[{
    'role': 'user',
    'content': 'Why is the sky blue? (explain in one sentenceoll)',
    },])


print(response['message']['content'])