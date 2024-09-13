import requests
import os
key = os.environ.get("NEWSAPIKEY")
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}"
a = requests.get(url).json()
print(a)