# Web Crawler Component for Cookietective
The crawler is available in three algorithms: Bread-First Search, Depth-First-Search, and single-layer. For arguments, it takes in a list of URLs formatted as a txt file, a start index for the txt file, and an end index for the txt file.

## Instructions:
1. Download [Gecko driver](https://github.com/mozilla/geckodriver/releases) for Firefox


3. Run `pip install selenium` and `pip install firefox` as needed


5. Run `python3 <crawler version>.py <URLs list> <start line> <end line>`
  - For example: `python3 crawler_quick.py example_URLs.txt 0 5` to use the single-layer crawler on the first 5 domains in example_URLs.txt
