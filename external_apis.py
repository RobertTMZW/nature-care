import io
import os
import requests
import bs4
# Imports the Google Cloud client library
from google.cloud import vision
# Instantiates a client
client = vision.ImageAnnotatorClient()

def classifyImage(image_path):
    # The name of the image file to annotate
    file_name = os.path.abspath(image_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]

def check_for_endangered(animal):
    wiki_url = 'https://en.wikipedia.org/wiki/{}'.format(animal)

    response = requests.get(wiki_url)

    if response is not None:
        page = bs4.BeautifulSoup(response.text, 'html.parser')
        paragraphs = page.select('p')
        images = page.select('img')
        wiki_text = (''. join(p.text for p in paragraphs)).encode('utf-8')
        return ["endangered" in wiki_text.decode('utf-8').lower(), wiki_url]
    else:
        return [False,wiki_url]

check_for_endangered('koala')