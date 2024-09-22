import json
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import io
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import ttk
import logging

def extract_text_from_url(url, browser_path, chrome_path):
    brave_path = browser_path  
    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    option.add_argument("--incognito")
    option.add_argument("--headless")
    option.add_argument('--remote-debugging-port=9204')
    chromedriver_path = chrome_path 
    service = Service(executable_path=chromedriver_path)
    browser = webdriver.Chrome(service=service, options=option)
    extraction = 'yes' if change_logic.get() else 'no'

    try:
        browser.get(url)
        html_string = browser.page_source
        soup = BeautifulSoup(html_string, 'html.parser')
        
        if extraction == 'yes':
            logicc = logic.get().strip()
            text_elements = soup.select(logicc)  
            text_after_patterns = []
            for element in text_elements:
                text = element.get_text(strip=True)
                text_after_patterns.append(text)
            text = '\n'.join(text_after_patterns)
        else:
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
        logging.error(f"An error occurred: {e}")
        text = ""
    finally:
        browser.quit()

    return text

def chunk_text(text, max_chunk_size=500): 
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    return chunks

logging.basicConfig(level=logging.INFO)

def translate_text(text, api_key, user_prompt, api_url):
    global total_tokens_used
    api_key = api_key 
    url = api_url
    output_file = output_file_entry.get()
    mode = 'a' if append_to_file.get() else 'w'
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": text},
            {"role": "user", "content": user_prompt}
        ]
    }
    update = 'yes' if update_gui.get() else 'no'
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        print("Response:", response_json)
        translated_text = response_json['choices'][0]['message']['content']
        output_text_box.insert(tk.END, translated_text + "\n")
        if update == 'yes':
            root.update_idletasks()
        with io.open(output_file, mode, encoding='utf-8') as f:
        	f.write(translated_text)
        tokens_used = len(text) // 4 + len(translated_text) // 4
        total_tokens_used += tokens_used
          

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        
    return translated_text 


def process_inputs():
    global total_tokens_used
    total_tokens_used = 0

    url = url_entry.get()
    api_key = api_key_entry.get()
    output_file = output_file_entry.get()
    user_prompt = prompt_entry.get("1.0", tk.END).strip()
    api_url = api_url_combobox.get()

    if api_url == "Other":
        api_url = custom_api_url_entry.get().strip()

    if not url or not api_key or not user_prompt or not api_url:
        messagebox.showerror("Input Error", "Please provide a URL, an API key, a prompt, and an API URL.")
        return
    browser_path = browser_path_entry.get().strip()
    chrome_path = chrome_path_entry.get().strip()
    novel_text = extract_text_from_url(url, browser_path, chrome_path)
    text_chunks = chunk_text(novel_text)
    translated_novel = ""

    for chunk in text_chunks:
        translated_chunk = translate_text(chunk, api_key, user_prompt, api_url)
        translated_novel += translated_chunk
        
    messagebox.showinfo("Success", f"Translation completed and saved to '{output_file}'.")

def show_token_info():
    messagebox.showinfo("Token Usage", f"Total tokens used: {total_tokens_used}")

def choose_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                               initialfile="output.txt",
                                               filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

def choose_path():
    b_path = filedialog.askopenfilename()  # Use askopenfilename for choosing the browser executable
    if b_path:
        browser_path_entry.delete(0, tk.END)  
        browser_path_entry.insert(0, b_path)  

def on_api_url_change(event):

    if api_url_combobox.get() == "Other":
        custom_api_url_entry.pack(pady=5)
    else:
        custom_api_url_entry.pack_forget()  

def logic_change():  
    if change_logic.get():
        logic.grid(row=4, column=3, columnspan=2, sticky=tk.W, pady=5)  
    else:
        logic.grid_forget()

root = tk.Tk()
root.title("Web Page Translator")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(padx=10, pady=10)

tk.Label(main_frame, text="Website URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
url_entry = tk.Entry(main_frame, width=50)
url_entry.grid(row=0, column=1, pady=5)

tk.Label(main_frame, text="API Key: (Default : ChatGPT)").grid(row=1, column=0, sticky=tk.W, pady=5)
api_key_entry = tk.Entry(main_frame, width=50, show='*')
api_key_entry.grid(row=1, column=1, pady=5)

tk.Label(main_frame, text="Browser Path:").grid(row= 5, column=0, sticky=tk.W, pady=5)
browser_path_entry = tk.Entry(main_frame, width=50)
browser_path_entry.grid(row=5, column=1, pady=5)

browser_path_button = tk.Button(main_frame, text="Choose Path", command=choose_path)
browser_path_button.grid(row=5, column=2, padx=5)

tk.Label(main_frame, text="ChromeDriver Path:").grid(row= 6, column=0, sticky=tk.W, pady=5)
chrome_path_entry = tk.Entry(main_frame, width=50)
chrome_path_entry.grid(row=6, column=1, pady=5)

chrome_button = tk.Button(main_frame, text="Choose Path", command=choose_path)
chrome_button.grid(row=6, column=2, padx=5)

tk.Label(root, text="API URL: (Default : ChatGPT)").pack(pady=5)
api_url_combobox = ttk.Combobox(root, width=50)
api_url_combobox['values'] = [
    "https://api.openai.com/v1/chat/completions",
    "Other"
]
api_url_combobox.current(0)
api_url_combobox.pack(pady=5)
api_url_combobox.bind("<<ComboboxSelected>>", on_api_url_change)

custom_api_url_entry = tk.Entry(root, width=50)
custom_api_url_entry.insert(0, "Enter custom API URL")
custom_api_url_entry.pack_forget() 


tk.Label(main_frame, text="Output File:").grid(row=4, column=0, sticky=tk.W, pady=5)
output_file_entry = tk.Entry(main_frame, width=50)
output_file_entry.insert(0, "output.txt")
output_file_entry.grid(row=4, column=1, pady=5)

output_file_button = tk.Button(main_frame, text="Choose File", command=choose_file)
output_file_button.grid(row=4, column=2, padx=5)

append_to_file = tk.BooleanVar(value=True)  
tk.Checkbutton(main_frame, text="Append to file", variable=append_to_file).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

update_gui = tk.BooleanVar(value=False)  
tk.Checkbutton(main_frame, text="Update GUI after each chunk? GUI may become sluggish", variable=update_gui).grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)

change_logic = tk.BooleanVar(value=False)  
tk.Checkbutton(main_frame, text="Change Extraction Logic?", variable=change_logic, command=logic_change).grid(row=3, column=3, columnspan=2, sticky=tk.W, pady=5)

logic = tk.Entry(main_frame, width=50)
logic.insert(0, "div")
logic.grid(row=4, column=3, columnspan=2, sticky=tk.W, pady=5) 
logic.grid_forget()

tk.Label(main_frame, text="Prompt:").grid(row=7, column=0, sticky=tk.W, pady=5)
prompt_entry = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=5)
prompt_entry.insert(tk.END, "Translate this text into English")
prompt_entry.grid(row=7, column=1, pady=5)

button_frame = tk.Frame(main_frame)
button_frame.grid(row=8, column=0, columnspan=3, pady=20)

process_button = tk.Button(button_frame, text="Process", command=process_inputs)
process_button.pack(side=tk.LEFT, padx=5)

info_button = tk.Button(button_frame, text="i", command=show_token_info)
info_button.pack(side=tk.LEFT, padx=5)

tk.Label(main_frame, text="Translated Text:").grid(row=9, column=0, sticky=tk.W, pady=5)
output_text_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=15)
output_text_box.grid(row=9, column=1, pady=5)

on_api_url_change(None)
logic_change()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root.mainloop()

