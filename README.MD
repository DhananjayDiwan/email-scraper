# Asynchronous Email Scraper with Progress Bar

This project is an asynchronous email scraper designed to extract email addresses from web pages efficiently. It supports multiple URLs, including those read from a file, and displays a progress bar to track the scraping process.

## Features

- **Asynchronous Requests**: Utilizes Python's `asyncio` and `aiohttp` for fast and concurrent web scraping.
- **Email Filtering**: Extracts valid email addresses and excludes unwanted patterns such as image file extensions.
- **Progress Bar**: Displays a real-time progress bar using the `tqdm` library to indicate scraping progress.
- **File Input Support**: Can read a list of URLs from a file (`urls.txt`), in addition to direct URL input.
- **Error Handling**: Skips over URLs that can't be reached or result in errors.

## Requirements

Ensure you have the following Python libraries installed:

- `requests`: For fetching the main page to scrape links.
- `aiohttp`: For making asynchronous HTTP requests.
- `beautifulsoup4`: For parsing HTML content.
- `tqdm`: For displaying the progress bar.
- `re`: For regular expression-based email pattern matching.

Install all dependencies using the following command:

```bash
pip install requests aiohttp beautifulsoup4 tqdm
```

## How It Works

1. **Input Selection**: You can provide a single URL directly or a file containing multiple URLs.
2. **Link Extraction**: The scraper extracts all links from the provided URL(s).
3. **Email Extraction**: For each extracted link, it fetches the page content and searches for email addresses using regular expressions.
4. **Filtering**: The scraper filters out invalid email addresses, such as those ending with image or media file extensions.
5. **Progress Tracking**: A progress bar is displayed to show the completion percentage as URLs are processed.
6. **Results**: All unique email addresses found are printed once the scraping is complete.

## Usage

1. **Run the Script**: Execute the script with a single URL or a file containing URLs:

   ```bash
   python email_scraper.py <url_or_file>
   ```

   - To input a single URL:
     ```bash
     python email_scraper.py https://example.com
     ```

   - To use a file with URLs (e.g., `urls.txt`), ensure each URL is on a new line:
     ```bash
     python email_scraper.py urls.txt
     ```

2. **Input Prompt**: If providing a single URL, you will be prompted to enter it directly:
   
   ```
   Enter URL: https://example.com
   ```

3. **Output**: The scraper will process the URLs and display the progress in real time. Once completed, the unique email addresses found will be listed in the terminal.

## Example Output

```
Processing URLs: 100%|██████████████████████████████████| 50/50 [00:05<00:00,  9.22it/s]
Total unique emails found: 5
example1@example.com
contact@example.org
info@website.com
```

## Code Explanation

### Main Components

- **`format_url(url)`**: Normalizes URLs, ensuring they start with `http://` or `https://` and correcting common domain typos (e.g., `.xom` to `.com`).
  
- **`find_emails(session, url)`**: Asynchronously fetches the content of a URL and extracts valid email addresses using regular expressions. It filters out emails with unwanted file extensions.

- **`process_urls(urls)`**: Manages the asynchronous processing of URLs and displays the progress using `tqdm`.

- **`get_htmlcontent(url)`**: Fetches HTML content from a URL and extracts hyperlinks on the page.

- **`process_urls_from_file(filename)`**: Reads URLs from a file, with each URL on a new line.

## Customization

### Filtering Email Patterns

You can customize the regular expression in the `find_emails()` function to match specific email formats or exclude additional patterns. Modify the `exclude_pattern` to add more file types or domain patterns.

```python
exclude_pattern = r'@.*\.(jpg|jpeg|png|...)$'
```

### Limiting URLs to a Specific Domain

To limit scraping to URLs from the same domain as the input URL, you can modify the `get_htmlcontent(url)` function accordingly.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.


