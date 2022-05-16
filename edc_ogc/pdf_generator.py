import base64
import io
from typing import List

import pdfkit as pdf
from flask import send_file, render_template
from pandas._typing import FilePathOrBuffer


def svg_image_file_path_to_string(svg_image_file_path: str):
    with open(svg_image_file_path, "r") as svg_image_file:
        return svg_image_file.read()


def image_file_path_to_base64_string(image: FilePathOrBuffer):
    if isinstance(image, str):
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    else:
        return base64.b64encode(image.read()).decode()



def generate_pdf(data: List[dict], generated_image: FilePathOrBuffer):
    table_headers = [header for header in data[0]]
    table_values = [[v for k, v in d.items()] for d in data]

    context = {
        "mobygis_logo": svg_image_file_path_to_string("static/mobylogo.svg"),
        "waterjade_logo": svg_image_file_path_to_string("static/waterjade.svg"),
        "data_headers": table_headers,
        "data": table_values,
        "test_image": image_file_path_to_base64_string(generated_image)
    }

    rendered_template = render_template("pdf.html", **context)
    pdfkit_sample = pdf.from_string(rendered_template, css="static/css/style.css")
    return send_file(
        io.BytesIO(pdfkit_sample),
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename='download.pdf',
        cache_timeout=1  # Avoid to store file in cache
    )
