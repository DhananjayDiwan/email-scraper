# importing the libires
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import aiohttp
import asyncio

# unique emails for the final result of emails
unique_emails = set()

# url fomat for proper url like https://example.com
def format_url(url):
    url = re.sub(r"\.xom$", ".com", url)# Correct common domain typos (e.g., ".xom" -> ".com")
    if not re.match(r'http[s]?://|ftp://|mailto:', url):  # Check if the URL starts with http/https/ftp/mailto, if not add "http://"
        url = f"https://{url}"
        
    return url 

# Function to find emails on a given URL LIST
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
        # Initialize the tqdm progress bar with the total number of URLs
        with tqdm(total=len(urls), desc="Processing URLs") as pbar:
            tasks = [find_emails(session, url) for url in urls]
            for future in asyncio.as_completed(tasks):
                result = await future
                unique_emails.update(result)
                # Update progress bar each time a task is completed
                pbar.update(1)

# get_htmlcontent for getting URL list on pages
def get_htmlcontent(url):
    # Get request  
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    asyncio.run(process_urls(links))
    

# application of this a
if __name__ == "__main__":
    urlinput = input("Enter url : ")
    url = format_url(urlinput)
    get_htmlcontent(url)
    
    
# Print all result and found email
    print(f"Total unique emails found: {len(unique_emails)}")
    for email in unique_emails:
        print(email)
