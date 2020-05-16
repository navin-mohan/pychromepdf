# Pychromepdf

Pychromepdf is a Python package that lets you easily create PDFs by rendering HTML content using Chrome or Chromium as backend. It works without any external dependecies except a working installation of Chrome or Chromium that supports headless mode.

# Installation

```bash
pip install pychromepdf
```

## Usage

### Rendering HTML bytestring to PDF

```python
from pychromepdf import ChromePDF

# change to your chrome executable path
PATH_TO_CHROME_EXE = '/usr/bin/google-chrome-stable'
# if you're on MacOS
# PATH_TO_CHROME_EXE = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'

if __name__ == '__main__':
    # initialize chromepdf object
    cpdf = ChromePDF(PATH_TO_CHROME_EXE)

    # the html that need to be rendered into pdf
    html_bytestring = '''
    <!doctype html>
    <html>
        <head>
            <style>
            @media print {
                @page { margin: 0; }
                body { margin: 1.6cm; }
            }
            </style>
        </head>
        <body>
            <h1>Hello, World</h1>
            <h5> Generated using headless chrome </h5>
        </body>
    </html>
    '''

    # create a file and write the pdf to it
    with open('test.pdf','w') as output_file:
        if cpdf.html_to_pdf(html_bytestring,output_file):
            print("Successfully generated the pdf: {}".format(output_file.name))
        else:
            print("Error generating pdf")

```

### Rendering a flask template into PDF

```python
from flask import Flask, render_template, send_file
import tempfile
from pychromepdf import ChromePDF

app = Flask(__name__)

# change to your chrome executable path
PATH_TO_CHROME_EXE = '/usr/bin/google-chrome-stable'

# initialize a chromepdf object
cpdf = ChromePDF(PATH_TO_CHROME_EXE)

# home route
@app.route('/')
def index():
    return render_template('index.html',username="John")

# custom pdf route
@app.route('/getpdf',defaults={'username': 'John'})
@app.route('/getpdf/<username>')
def getpdf(username):

    # get the rendered html as string using the template
    rendered_html = render_template('index.html',username=username)

    # create a temporary output file which will be deleted when closed
    with tempfile.NamedTemporaryFile(suffix='.pdf') as output_file:

        # create a pdf from the rendered html and write it to output_file
        if cpdf.html_to_pdf(rendered_html,output_file):
            print("PDF generated successfully: {0}".format(output_file.name))

            try:
                # send the file to user
                return send_file(output_file.name,attachment_filename='awesome.pdf')
            except Exception as e:
                return str(e)
        else:
            print("Error creating PDF")

    return "Error"
                

if __name__ == '__main__':
    app.run(debug=True)

```

Template

```html
{# templates/index.html #}

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Example</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        @media print {
            @page { margin: 0; }
            body { margin: 1.6cm; }
        }
    </style>    
</head>
<body>
    <h1>Hello {{ username }}!</h1>
    <h4>Generated using ChromePDF</h4>
</body>
</html>

```
