import base64
import io
from typing import List

import pdfkit as pdf
from flask import send_file, render_template
from pandas._typing import FilePathOrBuffer


def image_file_path_to_base64(generated_image: FilePathOrBuffer):
    if isinstance(generated_image, str):
        with open(generated_image, 'rb') as image_file:
            return base64.b64encode(image_file.read())
    else:
        return base64.b64encode(generated_image.read())


def generate_pdf(data: List[dict], generated_image: FilePathOrBuffer):
    table_headers = [header for header in data[0]]
    table_values = [[v for k, v in d.items()] for d in data]

    context = {
        "data_headers": table_headers,
        "data": table_values,
        "test_image": image_file_path_to_base64(generated_image).decode()
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
