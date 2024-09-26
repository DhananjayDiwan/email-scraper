import time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import aiohttp
import asyncio


# unique emails for the final result of emal
unique_emails = set()

def format_url(url):
    # Correct common domain typos (e.g., ".xom" -> ".com")
    url = re.sub(r"\.xom$", ".com", url)

    # Check if the URL starts with http/https, if not add "http://"
    if not re.match(r'http[s]?://', url):
        url = f"https://{url}"

    return url


# Function to find emails on a given URL
async def find_emails(session, url):
    emails = []
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                exclude_pattern = r'@.*\.(jpg|jpeg|png|gif|bmp|webp|tiff|svg|ico|heif|raw|mp4|avi|mov|wmv|flv|mkv)$'
                emails = re.findall(email_pattern, text)
                emails = [item for item in emails if re.fullmatch(
                    email_pattern, item) and not re.search(exclude_pattern, item)]
                
    except Exception as e:
        # print(f"Error fetching {url}: {e}")
        ...
    return emails

# Function to process a list of URLs and find emails
async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [find_emails(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for email_set in results:
            unique_emails.update(email_set)
            
        # for url, email_list in zip(urls, results):
        #     print(f"Emails found on {url}: {email_list}")


# get_htmlcontecnt for geting url list on pages

def get_htmlcontecnt(url):
    # Start measuring time
    start_time = time.time()
    # for get request  
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    for i in tqdm(links, desc="Processing", bar_format="{l_bar}{bar} [Elapsed: {elapsed}, Remaining: {remaining}]"):
        time.sleep(0.1)
    asyncio.run(process_urls(links))
    # code for only with that domain
    
    # base_url = urlparse(url).netloc
    # urls = [link for link in links if base_url in urlparse(link).netloc]
    

if __name__ == "__main__":
    urlinput = input("url : ")
    url = format_url(urlinput)
    get_htmlcontecnt(url)

    for email in unique_emails:
        elapsed_time = time.time() 
        print(email)
