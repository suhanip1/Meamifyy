import requests
from testGroqAPI import api_output
from groq import Groq

api_key = "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"
client = Groq(api_key=api_key)

# API endpoint for fetching meme templates
url = "https://api.imgflip.com/get_memes"
response = requests.get(url)
data = response.json()


if data['success']:
    memes = data['data']['memes']
    meme_templates = memes[:100]
    
    #for idx, meme in enumerate(meme_templates):
       # print(f"{idx + 1}. ID: {meme['id']}, Name: {meme['name']}, URL: {meme['url']}")
else:
    print("Failed to fetch memes.")


def select_meme_template_using_groq(joke_content, meme_templates):
    # Prepare the input for the Groq API
    meme_template_names = [template['name'] for template in meme_templates]
    prompt = f"""
    Given the following joke content:
    "{joke_content}"
    
    And the following meme templates:
    {', '.join(meme_template_names)}

    Which meme template is the most appropriate for the joke content? Respond with the exact template name and id.
    follow this strict template DO NOT add additional information
    name: [insert meme name here]
    id: [insert template id]
    reason: [insert reason of picking]
    """

    # Assuming a valid client setup for the Groq API
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    best_template_name = response.choices[0].message.content.strip()
    return best_template_name



def extract_name_and_id(text):
    # Split the text into lines
    lines = text.split('\n')

    # Initialize variables to hold name and ID
    name = None
    meme_id = None

    # Iterate through each line to find the relevant information
    for line in lines:
        if 'name:' in line:
            # Extract the name from the line
            name = line.split('name:')[1].strip()
        elif 'id:' in line:
            # Extract the ID from the line
            id_part = line.split('id:')[1].strip()
            meme_id = id_part.strip('[]')  # Remove square brackets if present

    # Return the extracted name and ID if found
    if name and meme_id:
        return name, meme_id
    else:
        return None

# Ensure that api_output is a string containing the joke content
if isinstance(api_output, list):
   # print(api_output)
    for i in api_output:
        selected_template = select_meme_template_using_groq(i, meme_templates)
        name, id = extract_name_and_id(selected_template)
        i["name"] = name
        i["id"] = id
        #print(f"Selected Meme Template: {selected_template}")
        print(f"name: {name}, id: {id} tesstt ", i["name"])
        break

else:
    print("Invalid joke content.")
