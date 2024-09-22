import json
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import io

def extract_text_from_url(url):
    brave_path = ""  # Adjust this path according to your system
    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    option.add_argument("--incognito")
    option.add_argument("--headless")
    option.add_argument('--remote-debugging-port=9204') 
    chromedriver_path = '' # Adjust this path according to your system
    service = Service(executable_path=chromedriver_path)
    browser = webdriver.Chrome(service=service, options=option)

    try:
        browser.get(url)
        html_string = browser.page_source
        soup = BeautifulSoup(html_string, 'html.parser')
        
        scripts = soup.find_all('div')
        text_after_patterns = []
        for script in scripts:
            if len(script.find_all('br')) >= 2:
                text_after_pattern = str(script)
                text_after_pattern = text_after_pattern.replace('</div>', '')
                text_after_pattern = text_after_pattern.replace('<div>', '')
                text_after_pattern = text_after_pattern.replace('\n', '')
                text_after_patterns.append(text_after_pattern)
        text = '\n'.join(text_after_patterns)
        
        
        
    except Exception as e:
        import logging
        logging.error(f"An error occurred: {e}")
        text = ""
    finally:
        browser.quit()

    return text

def chunk_text(text, max_chunk_size=500): # Adjust the chunk size if needed
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    return chunks

import os
import logging

logging.basicConfig(level=logging.INFO)

def translate_text(text):
    # Use environment variable or another secure method to store your API key
    api_key = "" # Replace with your actual API key

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": text},
            {"role": "user", "content": "Translate this text into English"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        print("Response:", response_json)
        translated_text = response_json['choices'][0]['message']['content']
        with io.open('new.txt', 'a', encoding='utf-8') as f:
        	f.write(translated_text)
        return translated_text
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        
    return ""


def main():
    novel_url = ""
    novel_text = extract_text_from_url(novel_url)
    with io.open('output.txt', 'w', encoding='utf-8') as f:
        f.write(novel_text)
    text_chunks = chunk_text(novel_text)
    translated_novel = ""
    for chunk in text_chunks:
        translated_chunk = translate_text(chunk)
        translated_novel += translated_chunk
    print(translated_novel)
    with io.open('newer.txt', 'w', encoding='utf-8') as f:
        f.write(translated_novel)



if __name__ == "__main__":
    main()
