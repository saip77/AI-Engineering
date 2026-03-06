import ollama

client = ollama.Client()

model = "gemma3:270m"
prompt = "Hi, who are you? and how are you?"

response = client.generate(
    model=model,
    prompt=prompt
)

print(response['response'])
