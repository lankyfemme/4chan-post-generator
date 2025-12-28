# -*- coding: utf-8 -*-
import os
from PIL import Image
from datetime import datetime
import random
import imgkit
import io
import math
import requests

def get_image_data(image_path):
    # Returns the image data of the image at the given path.
    image = Image.open(image_path)
    height = image.height
    width = image.width
    size = int(os.path.getsize(image_path) / 1024)
    file_info = f"({size} KB, {width}x{height})"

    if height > 150:
        width = int(width * 150 / height)
        height = 150
    
    if width > 250:
        height = int(height * 250 / width)
        width = 250
    
    
    return (height, width, file_info)

def create_blockquote(rtext):
    lines = rtext.split("\n")
    ret = []
    for i in lines:
        if i.startswith(">"):
            ret.append(f'<span class="quote">{i}</span>')
        else:
            ret.append(i)
    final = "<br>".join(ret)
    final.replace(">", "&gt;")

    return final


def generate_html(post_subject, image_link, post_content):

    blockquote = create_blockquote(post_content)
    formatted_date = datetime.now().strftime("%m/%d/%y(%a)%H:%M:%S")

    with open("./web/index_source.html", "r") as f:
        html_output = f.read()

    # download the picture
    image_name = image_link.split("/")[-1]
    r = requests.get(image_link, stream=True)
    with open(f'./pictures/{image_name}', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

    height, width, file_info = get_image_data(f'./pictures/{image_name}')

    if len(image_link) > 40:
        image_link = f"{image_link}"[:40] + '...' 
    else:
        image_link = f"{image_link}"

    html_output = html_output.replace("[FILE_NAME]", image_link)
    html_output = html_output.replace("[FILE_PATH]", os.path.abspath(f'./pictures/{image_name}'))
    html_output = html_output.replace("[FILE_INFO]", file_info)
    html_output = html_output.replace("[IMAGE_HEIGHT]", str(height))
    html_output = html_output.replace("[IMAGE_WIDTH]", str(width))
    html_output = html_output.replace("[POST_SUBJECT]", post_subject)
    html_output = html_output.replace("[DATE]", formatted_date)
    html_output = html_output.replace("[RANDOM_INT_REPLY]", str(random.randint(10000000, 99999999)))
    html_output = html_output.replace("[BLOCKQUOTE]", blockquote)

    return html_output

def create_screenshots(html_input):
    options = {
        'width': 640,
        'quality': 100,
        'enable-local-file-access': None,
        'allow': [
            '/app/pictures',
            '/app/web'
        ]
    }
    image_bytes = imgkit.from_string(html_input, False, options=options)
    image_stream = io.BytesIO(image_bytes)
    image = Image.open(image_stream)
    width, height = image.size
    
    number_of_pictures = math.floor(height / 1280)
    completed_height = 0
    images = []
    pixels = image.load()
    for i in range(number_of_pictures):
        # we need to make sure we're not cropping in the middle of a line of text, so check the colour of each pixel on the crop line
        # if the pixel contains any colour that isn't the background, then try the next row of pixels
        height_of_screenshot = 1280
        x = 0
        while x < width:
            pixel_colour = pixels[x, completed_height + height_of_screenshot]
            if pixel_colour[0] < 251:
                height_of_screenshot += 1
                x = 0
            x += 1

        left = 0
        top = completed_height
        right = width
        bottom = completed_height + height_of_screenshot
        cropped_image = image.crop((left, top, right, bottom))
        images.append(cropped_image)
        completed_height += height_of_screenshot

    # take the last screenshot, this will be shorter than the rest hence being outside the loop
    left = 0
    top = completed_height
    right = width
    bottom = height
    cropped_image = image.crop((left, top, right, bottom))
    images.append(cropped_image)

    return images

if __name__ == "__main__":
    post_content = """
sample text
> be me
more sample text for extra testing
> programmer
> want to make 4chan post generator
> someone else already made it but a discord bot
> take their code, twist it beyond recognition
> it's now a webapp
> cool.jpg
anyone else taken the programmerpill, anons?
"""
    html_output = generate_html("Example generate_html", "https://ichef.bbci.co.uk/ace/standard/976/cpsprodpb/16620/production/_91408619_55df76d5-2245-41c1-8031-07a4da3f313f.jpg", post_content)   
    with open("./web/test_output.html", "w+") as f:
        f.write(html_output)
    for image in create_screenshots(html_output):
        image.show()