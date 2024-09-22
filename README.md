This Project allows for the scraping of a webpage in order that it might be translated or summarized by an LLM through an API key. 

The first python file, web1.py is based off beautifulSoup, and does not require the installation of any executables, but only python libraries. 
pip install beautifulsoup4 requests should be enough to run it.
![web1](https://github.com/user-attachments/assets/9ed2db33-8d08-44a4-b644-693c9e4f1348)

On running it (python3 web1.py on Bash) , you should see a Tkinter gui which allows for inputing the API key, website URL, file path , prompt, and other such values. Any values which are prefilled need not be touched.

The second python file, web2.py is based off both beautifulSoup and selenium, and simulates the process of opening a browser for sites which do not give any output when running web1.py.
For this script, installation of a ChromeDriver is required on top of the python libraries, and the Tkinter GUI will also require a browser path and the ChromeDriver path. This may work for other browsers too, as it is a webdriver, but I have not checked.
pip install beautifulsoup4 requests selenium will be the pip command.
![web2](https://github.com/user-attachments/assets/61a83fa7-5a47-494a-8e9c-a9e16d7144a2)

The third python file, test.py is the second python file but without a Tkinter GUI, you will have to manually configure values if you run it.
pip install beautifulsoup4 requests selenium will be the pip command.

To install the Chrome Webdriver, check your Chromium- based Browser's  Chromium version, and install the chromedriver accordingly from https://googlechromelabs.github.io/chrome-for-testing/ or https://developer.chrome.com/docs/chromedriver/downloads if its an older version.'

