import streamlit as st
import post_generator
import io
from PIL import Image
import zipfile

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

greentext_image = st.text_input(
    "Image link:",
    "https://ichef.bbci.co.uk/ace/standard/976/cpsprodpb/16620/production/_91408619_55df76d5-2245-41c1-8031-07a4da3f313f.jpg"
)

greentext_input = st.text_area(
    "Enter your greentext, anon:",
    """> be me
> gay
> you get the rest
"""
)

html = post_generator.generate_html(greentext_title, greentext_image, greentext_input)
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