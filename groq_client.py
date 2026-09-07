from groq import Groq

def ask_groq(prompt, api_key, model, json_mode=False):
    client = Groq(api_key=api_key)
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a precise professional resume and job-matching assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.15,
        "max_tokens": 8000
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()
