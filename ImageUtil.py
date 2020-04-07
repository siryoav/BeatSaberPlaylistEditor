import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def text_wrap(text, font_name, font_size, max_width, max_height):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return

    font = ImageFont.truetype(font_name, font_size)
    if font.getsize(text)[0] <= max_width:
        lines.append((text, font.getsize(text)[0]))
    else:
        # split the line by spaces to get words
        words = text.split(' ')
        if font_size > 1:
            for word in words:
                if font.getsize(word)[0] > max_width:
                    return text_wrap(text, font_name, font_size - 1, max_width, max_height)
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word,
            # add the line to the lines array
            lines.append((line, font.getsize(line)[0]))
    if font_size > 1:
        line_height = font.getsize('hg')[1]
        total_line_height = len(lines) * line_height
        if total_line_height > max_height:
            return text_wrap(text, font_name, font_size - 1, max_width, max_height)
    return lines, font


def create_text_image(text, dim, x_margin, y_margin, font_name, max_font_size, font_color):

    # open the background file
    image = Image.new('RGBA', (dim, dim), (255, 0, 0, 0))

    # size() returns a tuple of (width, height)
    image_size = image.size
    # get shorter lines
    lines, font = text_wrap(
        text,
        font_name,
        max_font_size,
        image_size[0] - (2 * x_margin),
        image_size[1] - (2 * y_margin),
    )
    line_height = font.getsize('hg')[1]
    draw = ImageDraw.Draw(image)
    total_line_height = line_height * len(lines)
    start_y = image_size[1] / 2 - total_line_height / 2
    if start_y < y_margin:
        start_y = y_margin
    for line, width in lines:
        # draw the line on the image
        start_x = image_size[0] / 2 - width / 2
        if start_x < x_margin:
            start_x = x_margin
        draw.text((start_x, start_y), line, fill=font_color, font=font)

        # update the y position so that we can use it for next line
        start_y += line_height
    return image


def create_text_image_base64(
        text,
        dim=200,
        x_margin=10,
        y_margin=10,
        font_name='arial.ttf',
        max_font_size=50,
        font_color='black',
        format='PNG',
):
    image = create_text_image(text, dim, x_margin, y_margin, font_name, max_font_size, font_color)
    buffered = BytesIO()
    image.save(buffered, format=format)
    result = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # image.save(os.path.join('images', '{}.png'.format(text).replace("/", "_")))
    return result
