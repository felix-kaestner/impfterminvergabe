# impfterminvergabe

A simple **proof of concept** automation for getting a vaccination appointment against COVID-19 in Saxony, Germany.

## Idea

This project provides a simple automation build on top of [selenium](https://www.selenium.dev/) which launches a new
Chrome window and submits the form for getting a vaccination appointment. In case you get a suggestion for an available
appointment the automation stops and leaves you with an open Chrome window, in which case you can decide to accept or
decline and complete the procedure manually.

## Quick Start

1. Generate a user account at [https://sachsen.impfterminvergabe.de/](https://sachsen.impfterminvergabe.de/).

    Make sure to save the `username` ("Vorgangskennung") and `password` of your account. You might also want to generate a second user, if you want to get an appointment together with someone other.


2. Make sure you have [Google Chrome](https://www.google.com/intl/de_de/chrome/) (or [Chromium](https://www.chromium.org/)) installed on your machine. Get the exact version number of Chrome installed on your machine. Simple click the three dots in the upper right corner of Chrome and select `Help > About`. You should find a version number like `Version 90.0.4430.212 (Offizieller Build) (64-Bit)`.


3. Download the appropriate [Chrome Webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your Chrome version and operating system. Afterwards, extract the `chromedriver` (or `chromedriver.exe`) file from the zip archive.


4. Create a virtual environment using [virtualenv](https://github.com/pypa/virtualenv) and install the [selenium](https://www.selenium.dev/) package.

    ```bash
    $ python3 -m venv env
    $ source ./env/bin/activate # or .\env\Scripts\activate on Windows
    $ pip install selenium beepy
    ```
   Otherwise, just use the integration of an IDE like [PyCharm](https://www.jetbrains.com/de-de/pycharm/) to get you started.


5. Run the script.

    ```bash
    $ python3 main.py --username="hallo" --password="welt" --impfzentrum="Dresden"
    $ python3 main.py --username="hallo" --password="welt" --impfzentrum "Dresden" "Belgern"
    ```
   
_Optional_

If you do not want a vaccination appointment in some venues available, simply delete the corresponding entries from the `locations` dictionary (line 24-40).

## Legal Disclaimer

```markdown
Copyright © 2021 Felix Kästner

Permission to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of this software and associated 
documentation files (the “Software”) is hereby not granted to 
any person.

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
```

