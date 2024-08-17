from groq import Groq
from test import transcript


if (transcript.text):
    api_key = "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"  # Replace with your actual key

    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": transcript.text,
            }
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)