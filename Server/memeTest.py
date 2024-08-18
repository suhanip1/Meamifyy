import requests
from testGroqAPI import get_api_output
from groq import Groq

api_key = "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"
client = Groq(api_key=api_key)

def get_meme_templates():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    data = response.json()
    if data['success']:
        memes = data['data']['memes']
        return memes[:100]
        
    else:
        return None

def generate_meme(template_id, text0, text1):
    url = "https://api.imgflip.com/caption_image"
    params = {
        'template_id': template_id,
        'username': 'memeify23',  
        'password': 'memeify12',  
        'text0': text0,
        'text1': text1
    }
    response = requests.post(url, data=params)
    data = response.json()
    if data['success']:
        return data['data']['url']
    return None

def select_meme_template_using_groq(joke_content, meme_templates):
    meme_template_info = [(template['name'], template['id']) for template in meme_templates]
    
    prompt = f"""
    Given the following joke content:
    "{joke_content}"
    
    And the following meme templates with corresponding IDs:
    {', '.join(f"{name} (ID: {id})" for name, id in meme_template_info)}

    Which meme template is the most appropriate for the joke content? Respond with the exact template name and ID. 
    Follow this strict template DO NOT add additional information:
    name: [insert meme name here]
    id: [insert template id here]
    reason: [insert reason for picking]
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
    
    best_template_info = response.choices[0].message.content.strip()
    return best_template_info

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


def set_template_ids(file_name):
    api_output = get_api_output(file_name)

    # Ensure that api_output is a string containing the joke content
    if isinstance(api_output, list):
    # print(api_output)
        for i in api_output:
            meme_templates = get_meme_templates()
            selected_template = select_meme_template_using_groq(i, meme_templates)
            print(selected_template)
            name, id = extract_name_and_id(selected_template)
            i["name"] = name
            i["id"] = id

        for i in api_output:
            joke =  i["joke"].split("?")
            i["joke"] = joke[0] + "?"
            i["joke-followUp"] = joke[1]
            i["url"] = generate_meme(i["id"], i["joke"], i["joke-followUp"])
            print(i["joke"], i["url"])

        return api_output

    else:
        print("Invalid joke content.")




