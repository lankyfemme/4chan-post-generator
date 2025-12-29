import streamlit as st
import post_generator
import io
from PIL import Image
import zipfile
import random
from magic import Magic

def zip_files(list_of_images):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, image_byte in enumerate(list_of_images):
            zip_file.writestr(f"image{i}.png", image_byte.read())

    # Get the value of the buffer (the zip file's bytes)
    return buffer.getvalue()

st.set_page_config(
    page_title="4chan Post Generator",
    page_icon="🤖"
)

greentext_title = st.text_input(
    "Title of your greentext:"
)

greentext_image = st.file_uploader(
    "Image upload:",
    type=["jpg", "jpeg", "png"]
)

greentext_input = st.text_area(
    "Enter your greentext, anon:",
    """> be me
> gay
> you get the rest
"""
)

if greentext_image:

    mime_type = Magic(mime=True).from_buffer(greentext_image.getvalue())

    greentext_image_name = f'{random.randint(100000,999999)}.{mime_type.split('/')[-1]}'

    with open(f'./pictures/{greentext_image_name}', 'wb+') as f:
        f.write(greentext_image.getvalue())
else:
    greentext_image_name = None

html = post_generator.generate_html(greentext_title, greentext_image_name, greentext_input)
images = post_generator.create_screenshots(html)

image_bytes = []

for image in images:
    image_byte_buffer = io.BytesIO()
    image.save(image_byte_buffer, format='PNG')
    image_byte_buffer.seek(0)
    image_bytes.append(image_byte_buffer)

images_zipped = zip_files(image_bytes)

st.download_button(
    label="Download Images",
    data=images_zipped,
    file_name="images.zip",
    mime="application/zip"
)

st.text(
    "Preview:"
)
st.image(images)

st.markdown(
    """
Made with :rainbow[love] by lankyfemme. [Source Code](https://github.com/lankyfemme/4chan-post-generator)
"""
)
