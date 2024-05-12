# Hippity-Hoppity Your Web Page is Now My Property!
### April 2024
### Video Demo: https://www.youtube.com/watch?v=Y4h5m06fvh0
----
Hello world! Welcome to my final CS50P project. My name is Edmond Mitar and I'm international business student living in the Netherlands. I am originally from Romania. 🇷🇴
#### Description
For this final project I've decided to build a website scraper that grabs all the HTML and CSS code from a given web page. The reason I decided to build this program was because I always wanted to test my front-end development skills locally on a web page.

It does not serve as the ultimate offline replacement for a webpage, but it does manage to grab all the HTML and CSS code on the surface level - it does not account for javascript or images (yet).
### `project.py`
#### First part
The `project.py` program has over 200 lines of code and a dozen functions. The backbone of this project are the `BeautifulSoup`, `urllib`, and `requests` libraries, which work together to gather the code and resources of a given web page.

The program starts by asking the user for a URL and the program converts it to a `BeautifulSoup` object. It then looks within the `<title>` tag from the soup object and uses the `slugify` function to create the name of the folder where the contents of the website will reside. This is to ensure a unique name for every website that is easy to read and does not contain any special characters.

The next part is to create a folder using the web page's title. The program then enters that directory using `os.chdir()` function. It then creates a new `css` directory that will store all the css and resources found within the web page - and enters that directory using `os.chdir()`.

The next part of the program grabs all the CSS `href` values from all the `<link>` tags and all contents within every `<style>` tag. Then, the program gets the CSS code from every `href` URL using urllib, formats their contents using `cssbeautifier`, and outputs their contents in a `links.css` file.

For every URL found within the `href` attribute of `<link>` tags, the program can determine whether it's a relative or absolute URL. It does this by using the `urlparse()` function as well as `urljoin()` and appends the link to a `links` list.

Similarly, the program follows the same procedure with all `<style>` tags it found within the soup object using the `write_css_file()` function. It then uses the `cssbeautifier` function to format their contents and outputs them in a `styles.css` file.

So far, the program has managed to grab all the CSS code found within all `<link>` and `<style>` tags and put it into the `links.css` and `styles.css` folders respectively.
#### Second part
The second part of the program uses the `get_resources()` and `get_css_urls` functions to download any fonts, images, or external css files using a fairly complex regular expression:

`([^\"\']?(?<=url\([\"\'\/\w])(?!data:)[^\)]+\.(\w+)[^\)\"\']*)`

This regular expression captures all relative or absolute URLs from the `links.css` and `styles.css` files and downloads their contents using the `get_css_urls()` function. I found this part extremely challenging because I had to write a lot of regular expressions, most of which were not successful.

In the end, I managed to write the regular expression using a lookahead assertion `([^\"\']?(?<=url\([\"\'\/\w])` to grab everything after the "url(" text from a given css file. The first capturing group is the URL itself, and the second one is the extension of the file within the URL which I later used to organize the downloaded files.

The program downloads the URL's contents and outputs them to a file using the URL's file basename. It does this by using the `get_basename()` function, which uses yet another regular expression to remove every character after the file's extension. This is to avoid writing any `?` or `#` characters to the file's name.
#### The third part
The final part is to write the `index.html` file by updating its `<link>` and `<style>` tags, which means removing any of those tags and instead using the `links.css` and `styles.css` files the program previously created. Similar to the css files, it uses the `soup.prettify()` function to format its contents, albeit not in a prettier fashion than the `cssbeautifier` library does.
### Final words
Given the program's complexity, I was only able to test a third of my functions. The other two-thirds required a lot of I/O operations and also depended on other (css) files to function. Regardless, I did my best in having functions perform only one task and not perform extensive requests to the web server.
### Conclusion
Thank you very much for showing interest in my final CS50P project. Special thanks to David Malan for his amazing teaching style, which captivated me from the very beginning. If you consider learning to program, then I highly recommend taking CS50P to anyone interested. Best of luck!
