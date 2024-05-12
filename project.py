import re
import os
import time
import requests
import cssbeautifier
from typing import List
from slugify import slugify
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
}


def main():
    while True:
        url = input("Enter URL: ")
        soup = get_soup(url)
        try:
            css_styles = soup.head.find_all("style")
            css_links = soup.head.find_all(css_selector)
        except AttributeError:
            print("Invalid URL. Please enter a valid URL.")
        else:
            break
    if css_links or css_styles:
        folder_name = get_title(soup)
        print("Page title: " + str(soup.head.title.get_text()))
        create_folder(folder_name, url, soup)
    else:
        print("No CSS found.")


def get_soup(url):
    """This function prepares the soup."""
    try:
        request = Request(url, headers=headers)
        time.sleep(3)
        html = urlopen(request)
    except URLError:
        raise URLError("Server could not be found!")
    except ValueError:
        raise ValueError("Invalid URL. Please enter a valid URL.")
    else:
        soup = BeautifulSoup(html.read(), "html.parser")
        return soup


def get_title(soup):
    """This function grabs the soup's title and converts it into an OS-friendly name"""
    if soup.head.title:
        title = soup.head.title.get_text()
        folder_name = slugify(title)
    else:
        folder_name = "website"
    return folder_name


def get_basename(basename):
    """This function updates the basename of a file by removing any extra characters
    after the file's extension"""
    url_pattern = re.compile(r"([\w-]+\.\w+).*")
    updated_basename = re.sub(
        url_pattern, lambda match: match.group(1), basename)
    return updated_basename


def get_css_urls(css_url, links):
    """This function downloads all the resources from a css file into a "resources" folder"""
    global headers
    resources_path = "resources"
    if not os.path.exists(resources_path):
        os.makedirs(resources_path)
    os.chdir(resources_path)  # change to "resources" folder
    for link in links:
        basename = get_basename(os.path.basename(link[0]))
        filetype_path = link[1]
        if not os.path.exists(filetype_path):
            os.makedirs(filetype_path)
        os.chdir(filetype_path)  # change to {filetype} folder
        with open(basename, "wb") as file:
            if not urlparse(link[0]).scheme:
                full_url = urljoin(css_url, link[0])
                response = requests.get(full_url, headers=headers)
                file.write(response.content)
            else:
                response = requests.get(link[0], headers=headers)
                file.write(response.content)
        os.chdir("../")  # go back to "resources" folder
    os.chdir("../")  # go back to "css" folder


def replace_urls_regex(css_file):
    """This function replaces the URLs within the CSS files with their appropriate relative paths"""
    url_pattern = re.compile(
        r"([^\"\']?(?<=url\([\"\'\/\w])(?!data:)[^\)]+\.(\w+)[^\)\"\']*)"
    )

    def replace_url(match):
        url = match.group(1)
        file_basename = os.path.basename(url)
        new_url = f"resources/{match.group(2)}/{file_basename}"
        return new_url

    with open(css_file) as file:
        css_contents = file.read()

    new_css_contents = re.sub(url_pattern, replace_url, css_contents)

    with open(css_file, "w") as file:
        file.write(new_css_contents)


def create_folder(path: str, url: str, soup: BeautifulSoup):
    """This function creates the folder that will contain the website's contents"""
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)  # change to website folder
    css_path = "css/"
    if not os.path.exists(css_path):
        os.makedirs(css_path)
    os.chdir(css_path)  # change to css folder
    css_links = soup.head.find_all(css_selector)
    css_styles = soup.head.find_all("style")
    if css_links:
        links = get_css_links(css_links, url)
        write_css_file(links, "link")
        get_resources("links.css", links[0])
        replace_urls_regex("links.css")
    if css_styles:
        write_css_file(css_styles, "style")
        get_resources("styles.css", url)
        replace_urls_regex("styles.css")
    os.chdir("../")  # go back to the website's folder
    create_index(soup)


def get_resources(css_file, css_url):
    """This function gets all the resources from urls found in a css file in a "resources" folder"""
    with open(css_file) as file:
        css_contents = file.read()
        url_pattern = re.compile(
            r"([^\"\']?(?<=url\([\"\'\/\w])(?!data:)[^\)]+\.(\w+)[^\)\"\']*)"
        )
        links_re = re.findall(url_pattern, css_contents)
        if links_re:
            get_css_urls(css_url, links_re)
            print(f'Created "resources" folder from {len(links_re)} links')


def create_index(soup):
    """This function creates the index.html file with either a <link> or <style> tags
    in the head section"""
    css_links = soup.head.find_all(css_selector)
    css_styles = soup.head.find_all("style")
    if css_links:
        for link in css_links:
            link.decompose()
        new_css_link = soup.new_tag(
            "link", href="css/links.css", rel="stylesheet", type="text/css"
        )
        soup.head.append(new_css_link)
    if css_styles:
        for style in css_styles:
            style.decompose()
        new_css_style = soup.new_tag(
            "link", href="css/styles.css", rel="stylesheet", type="text/css"
        )
        soup.head.append(new_css_style)
    formatted_html = soup.prettify()
    with open("index.html", "wb") as file:
        file.write(formatted_html.encode())


def css_selector(tag):
    """Selector for find_all() function that filters all css <link> tags"""
    return tag.name == "link" and (
        (tag.has_attr("rel") and "stylesheet" in tag.get("rel"))
        or (tag.has_attr("type") and "text/css" in tag.get("type"))
    )


def get_css_links(results, url):
    """This function returns a list of full href URLs found from <link> tags"""
    links = []
    for result in results:
        link = result.get("href")
        parsed_link = urlparse(link)
        if parsed_link.scheme:
            links.append(link)
        elif not parsed_link.scheme and result.has_attr("href"):
            css_location = urljoin(url, result.get("href"))
            links.append(css_location)
    return links


def get_css(url):
    """This function requests a css file from URL and returns it"""
    global headers
    request = Request(url, headers=headers)
    css = urlopen(request).read().decode()
    return css


def write_css_file(input, tag_name):
    """This function takes either a list of links or a ResultSet object with <style> Tag objects,
    formats their contents, and outputs them into a css file"""
    try:
        if isinstance(input, ResultSet):
            with open("styles.css", "w") as file:
                output_name = "styles.css"
                for item in input:
                    css = item.get_text()
                    formatted_css = cssbeautifier.beautify(css)
                    file.write(formatted_css)
        elif isinstance(input, List):
            with open("links.css", "w") as file:
                output_name = "links.css"
                for item in input:
                    css = get_css(item)
                    formatted_css = cssbeautifier.beautify(css)
                    file.write(formatted_css)
    except HTTPError as error:
        print(f"Something went wrong. Reason: {error.status} {error.reason}")
    else:
        print(f"Created {output_name} from {len(input)} <{tag_name}> tag(s)")


if __name__ == "__main__":
    main()