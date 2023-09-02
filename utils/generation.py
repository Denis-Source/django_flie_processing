from random import randint


def generate_noisy_image(image, noise_intensity=30):
    """Generate image with some random noise"""
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            if isinstance(pixel, tuple):
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]

                noise_r = randint(-noise_intensity, noise_intensity)
                noise_g = randint(-noise_intensity, noise_intensity)
                noise_b = randint(-noise_intensity, noise_intensity)

                r = max(0, min(255, r + noise_r))
                g = max(0, min(255, g + noise_g))
                b = max(0, min(255, b + noise_b))

                if len(pixel) == 3:
                    image.putpixel((x, y), (r, g, b))
                else:
                    image.putpixel((x, y), (r, g, b, 255))
            else:
                noise = randint(-noise_intensity, noise_intensity)
                v = max(0, min(255, pixel + noise))
                image.putpixel((x, y), v)

    return image


def generate_document():
    """Generate a tuple of documents (HTML and markdown)"""
    html = b"<!DOCTYPE html>" \
           b"<html>" \
           b"<body>" \
           b"<h1>First Heading</h1>" \
           b"<p>First paragraph.</p>" \
           b"</body>" \
           b"</html>"

    markdown = "# First Heading\n\n" \
               "First paragraph.\n"

    return html, markdown
