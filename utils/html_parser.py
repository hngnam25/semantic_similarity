from bs4 import BeautifulSoup

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'lxml')
    return soup

def extract_main_content(soup):
    # Assuming the main content is within <body> tags
    body = soup.find('body')
    if body:
        text = body.get_text(separator=' ')
    else:
        text = soup.get_text(separator=' ')
    return text

