from random import randint


def generate_noisy_image(image,  noise_intensity=30):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            noise_r = randint(-noise_intensity, noise_intensity)
            noise_g = randint(-noise_intensity, noise_intensity)
            noise_b = randint(-noise_intensity, noise_intensity)

            r = max(0, min(255, r + noise_r))
            g = max(0, min(255, g + noise_g))
            b = max(0, min(255, b + noise_b))
            image.putpixel((x, y), (r, g, b))
    return image

def generate_document():
    content = b"<!DOCTYPE html>" \
                   b"<html>" \
                   b"<body>" \
                   b"<h1>First Heading</h1>" \
                   b"<p>First paragraph.</p>" \
                   b"</body>" \
                   b"</html>"

    expected = "# First Heading\n\n" \
                "First paragraph.\n"

    return content, expected