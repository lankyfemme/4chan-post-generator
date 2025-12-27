# -*- coding: utf-8 -*-
import os
from PIL import Image
from datetime import datetime
import random

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


def greentext(post_subject, image_path, post_content):

    blockquote = create_blockquote(post_content)
    height, width, file_info = get_image_data(f'./{image_path}')
    formatted_date = datetime.now().strftime("%m/%d/%y(%a)%H:%M:%S")

    with open("./web/index_source.html", "r") as f:
        html_output = f.read()

    html_output = html_output.replace("[FILE_NAME]", image_path)
    html_output = html_output.replace("[FILE_PATH]", os.path.abspath(f'./{image_path}'))
    html_output = html_output.replace("[FILE_INFO]", file_info)
    html_output = html_output.replace("[IMAGE_HEIGHT]", str(height))
    html_output = html_output.replace("[IMAGE_WIDTH]", str(width))
    html_output = html_output.replace("[POST_SUBJECT]", post_subject)
    html_output = html_output.replace("[DATE]", formatted_date)
    html_output = html_output.replace("[RANDOM_INT_REPLY]", str(random.randint(10000000, 99999999)))
    html_output = html_output.replace("[BLOCKQUOTE]", blockquote)

    return html_output

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
    with open("./web/test_output.html", "w+") as f:
        f.write(greentext("Example Greentext", "pictures/example.jpg", post_content))

