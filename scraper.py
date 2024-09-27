
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import aiohttp
import asyncio
import sys

# Unique emails for the final result
unique_emails = set()

# URL format for proper URL like https://example.com
def format_url(url):
    url = re.sub(r"\.xom$", ".com", url)  # Correct common domain typos
    if not re.match(r'http[s]?://|ftp://|mailto:', url):
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
        
        with tqdm(total=len(urls), desc="Processing URLs") as pbar:
            tasks = [find_emails(session, url) for url in urls]
            for future in asyncio.as_completed(tasks):
                result = await future
                unique_emails.update(result)
                
                pbar.update(1)

# Get HTML content and extract URLs
def get_htmlcontent(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    formatted_links = [format_url(link) for link in links]
    return formatted_links

# Process URLs from a file
def process_urls_from_file(filename):
    with open(filename, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

# Main function to handle input and processing
async def main(input_path):
    if input_path.endswith('.txt'):
        urls = process_urls_from_file(input_path)
    else:
        urls = [format_url(input_path)]

    all_links = []
    for url in urls:
        all_links.extend(get_htmlcontent(url))
    
    # Remove duplicates and format links
    all_links = list(set(all_links))
    all_links = [format_url(link) for link in all_links]
    
    await process_urls(all_links)
    
    # Print all result and found emails
    print(f"Total unique emails found: {len(unique_emails)}")
    for email in unique_emails:
        print(email)

# Application entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python web_scraper.py <url_or_file>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    asyncio.run(main(input_path))
