from groq import Groq
from test import transcriptFinal

# Assuming you've imported transcriptFinal from another file
# from some_module import transcriptFinal

api_key = "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"

client = Groq(api_key=api_key)

# Define your prompt using the provided template
prompt = f"""
Using the following transcript on the Animal Kingdom:

{transcriptFinal}

1. Provide a funny text
2. Relate to the funny text educational question on a topic
3. Provide 4 possible answers
4. Provide the correct answer
5. Provide ten of these
6. The topic is Animal Kingdom
7. Follow this template strictly and add no other symbol or text:

Create ten funny memes for the topic following this exact template from the funniest to least funniest:

Joke {{INSERT JOKE NUMBER}}: {{INSERT JOKE ABOUT ANIMAL KINGDOM WITH ANSWER}}  
Question {{INSERT QUESTION NUMBER}}: {{INSERT EDUCATIONAL QUESTION ABOUT ANIMAL KINGDOM RELATE IT TO THE JOKE}}  
Option 1: {{INSERT CORRECT OR INCORRECT OPTION 1}}  
Option 2: {{INSERT CORRECT OR INCORRECT OPTION 2}}  
Option 3: {{INSERT CORRECT OR INCORRECT OPTION 3}}  
Option 4: {{INSERT CORRECT OR INCORRECT ANSWER OPTION 4}}  
Answer: {{INSERT CORRECT OPTION NUMBER}}

Ensure the memes are related to the topic, and include exactly four answer choices with only one correct answer. Follow the template precisely and avoid adding any extra information.
"""

# Send the prompt to the API
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama3-8b-8192",
)

# Print the response
print(chat_completion.choices[0].message.content)
