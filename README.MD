# Asynchronous Email Scraper with Progress Bar

This project is an asynchronous email scraper that extracts email addresses from web pages. It supports multiple URLs and displays a progress bar to track the scraping process.

## Features

- **Asynchronous requests**: Faster scraping using Python's `asyncio` and `aiohttp`.
- **Email filtering**: Extracts valid email addresses while excluding unwanted patterns like image extensions.
- **Progress bar**: A progress bar using the `tqdm` library shows the scraping progress in real time.
- **Error handling**: Skips over any URLs that can't be reached or return errors.

## Requirements

Make sure you have the following Python libraries installed:
S
- `requests`: To fetch the main page for scraping links.
- `aiohttp`: For asynchronous HTTP requests.
- `beautifulsoup4`: To parse the HTML content.
- `tqdm`: To display the progress bar.
- `re`: Regular expression for email pattern matching.

You can install all dependencies using the following command:

```bash
pip install requests aiohttp beautifulsoup4 tqdm
```

## How It Works

1. The user enters a URL to scrape.
2. The scraper extracts all links from the provided URL.
3. For each extracted link, it fetches the page content and looks for email addresses using a regular expression.
4. It filters out any invalid email addresses, such as those ending with image or media file extensions.
5. A progress bar is displayed to show the completion percentage as the scraper processes each URL.
6. All unique email addresses found are displayed once scraping is complete.

## Usage

1. Run the script by executing the following command:

```bash
python email_scraper.py
```

2. You will be prompted to enter a URL:

```
Enter url : https://example.com
```

3. The scraper will fetch and process the links on the given URL, displaying the progress in real time.

4. Once completed, the unique emails found will be printed in the terminal.

## Example Output

```
url : https://example.com
Processing URLs: 100%|██████████████████████████████████| 50/50 [00:05<00:00,  9.22it/s]
Total unique emails found: 5
example1@example.com
contact@example.org
info@website.com
```

## Code Explanation

### Main Components

- **`format_url(url)`**: Normalizes the URL, ensuring it starts with `http://` or `https://` and correcting common domain typos (like `.xom` to `.com`).
  
- **`find_emails(session, url)`**: Asynchronously fetches the content of a given URL and extracts valid email addresses using regular expressions. It filters out emails with unwanted file extensions (like `.jpg`, `.png`, etc.).

- **`process_urls(urls)`**: Handles the asynchronous processing of all URLs and displays the progress using `tqdm`.

- **`get_htmlcontent(url)`**: Fetches the HTML content from the main URL and extracts all the hyperlinks on the page.

## Customization

### Filtering Email Patterns

You can customize the regular expression in the `find_emails()` function to match specific email formats or add additional filters as needed.

For example, to exclude additional file types or domain patterns, modify the `exclude_pattern`:

```python
exclude_pattern = r'@.*\.(jpg|jpeg|png|...)$'
```

### Limiting URLs to a Specific Domain

If you want to limit scraping to URLs from the same domain as the input URL, uncomment and modify the relevant code section in the `get_htmlcontent(url)` function.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.


