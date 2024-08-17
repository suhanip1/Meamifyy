from groq import Groq
from test import transcriptFinal

# Assuming you've imported transcriptFinal from another file
# from some_module import transcriptFinal

api_key = "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"

client = Groq(api_key=api_key)

# Define your prompt using the provided template
prompt = f"""
Using the following transcript:

{transcriptFinal}

1. Provide a funny text
2. Relate the funny text to an educational question derived from the transcript
3. Provide 4 possible answers
4. Provide the correct answer
5. Provide ten of these
6. The content should be relevant to the entire transcript provided
7. Follow this template strictly and add no other symbol or text:

Create ten funny memes for the topic following this exact template from the funniest to least funniest:

Joke {{INSERT JOKE NUMBER}}: {{INSERT JOKE RELATED TO THE TRANSCRIPT WITH ANSWER}}  
Question {{INSERT QUESTION NUMBER}}: {{INSERT EDUCATIONAL QUESTION RELATED TO THE JOKE AND TRANSCRIPT}}  
Option 1: {{INSERT CORRECT OR INCORRECT OPTION 1}}  
Option 2: {{INSERT CORRECT OR INCORRECT OPTION 2}}  
Option 3: {{INSERT CORRECT OR INCORRECT OPTION 3}}  
Option 4: {{INSERT CORRECT OR INCORRECT OPTION 4}}  
Answer: {{INSERT CORRECT OPTION NUMBER}}

Ensure the jokes and questions are related to the transcript, and include exactly four answer choices with only one correct answer. Follow the template precisely and avoid adding any extra information.
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
# print(chat_completion.choices[0].message.content)

output = chat_completion.choices[0].message.content

def parse_api_response(api_response):
    sections = api_response.strip().split('\n\n')
    cards = []
    for section in sections:
        lines = section.split('\n')
        if len(lines) >= 6:
            # Extract the joke number and content, and use them to form the new key
            joke_number = lines[0].split(' ')[1].strip(':')
            joke_content = lines[0].split(': ')[1]
            
            # Extract the question number and content, and use them to form the new key
            question_number = lines[1].split(' ')[1].strip(':')
            question_content = lines[1].split(': ')[1]

            # Extract the options and answer
            options = {lines[i].split(':')[0].strip(): lines[i].split(':')[1].strip() for i in range(2, 6)}
            answer = lines[6].replace('Answer: ', '').strip()

            # Form the dictionary with the new key format
            cards.append({
                f'joke {joke_number}': joke_content,
                f'question {question_number}': question_content,
                'options': options,
                'answer': answer
            })
    return cards

# Use the function to parse the API response
list1 = parse_api_response(output)

# Example of printing the result to check
for card in list1:
    print(card)
