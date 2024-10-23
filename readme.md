# AI Web Scraping Agent

An intelligent web scraping agent powered by gpt-4o-mini that can adaptively navigate websites to find and extract specific information. The agent uses a recursive approach to explore links and locate requested data.

## Features

- gpt-4o-mini powered intelligent scraping
- Recursive link exploration
- Target-specific information extraction
- Dynamic website navigation
- Efficient abort conditions to prevent endless searches

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install required dependencies:
```bash
pip install openai beautifulsoup4 python-dotenv requests tiktoken
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the scraper from the command line using:

```bash
python agent.py --prompt "Your search prompt" --website "https://website-to-scrape.com"
```

### Parameters:
- `--prompt`: Specify what information you want to extract
- `--website`: The starting URL for the scraping process

### Example Usage
For a detailed example of how the scraper works, including sample output and execution logs, check out [Example.md](Example.md).

## How It Works

1. The agent starts by scraping the main page using BeautifulSoup4
2. It analyzes the content for the requested information
3. If the information isn't found, it identifies all links on the current page
4. The agent intelligently follows promising links that might contain the required information
5. The process repeats until either:
   - The required information is found
   - All relevant links have been exhausted

### Output Format

The agent returns data in JSON format:

```json
{
    "source_url": "URL where information was found",
    "required_information": "Extracted information"
}
```

If no relevant information is found:
```json
{
    "error": "Required information not found"
}
```

## Project Structure

- `agent.py`: Main agent logic and OpenAI integration
- `scraper.py`: Web scraping functionality using BeautifulSoup4
- `Example.md`: Sample execution logs and output demonstration

## Technical Details

- Uses OpenAI's gpt-4o-mini model for intelligent navigation
- Uses function calling feature for tool use
- Maximum of 5 recursive iterations to prevent infinite loops
- Supports both relative and absolute URL handling

## Limitations

- Requires valid OpenAI API key
- Limited to 5 recursive iterations
- Subject to website robots.txt rules and rate limiting
- Token limitations based on gpt-4o-mini model constraints