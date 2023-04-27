"""
This script generates random images with triangles and uploads them to Mastodon.
"""

import os
import time
import numpy as np
from mastodon import Mastodon
from PIL import Image, ImageDraw

# Your Mastodon API credentials
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
ACCESS_TOKEN = 'ACCESS_TOKEN'
API_BASE_URL = 'https://mstdn.bronyfurry.com'

mastodon = Mastodon(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
    api_base_url=API_BASE_URL,
)

NUM_TRIANGLES = 5
SIZE = 512


def generate_image_with_colors(num_triangles, size, colors):
    """
    Generates a PIL image with random triangles of random colors.
    """
    image = Image.new('RGB', (size, size), color=colors[0])
    draw = ImageDraw.Draw(image)

    for i in range(num_triangles):
        vertices = [
            (np.random.randint(0, size), np.random.randint(0, size)),
            (np.random.randint(0, size), np.random.randint(0, size)),
            (np.random.randint(0, size), np.random.randint(0, size)),
        ]
        draw.polygon(vertices, fill=colors[np.random.randint(0, len(colors))])

    return image


def create_and_upload_image_by_request(num_triangles, size, colors, mastodon):
    """
    Generates an image and uploads it to Mastodon.
    """
    image = generate_image_with_colors(num_triangles, size, colors)
    image_path = 'image.png'
    image.save(image_path)

    media_dict = mastodon.media_post(image_path)
    mastodon.status_post(status='Here is your image!', media_ids=[media_dict['id']])

    os.remove(image_path)


def main():
    """
    Main function that generates and uploads images every 15 minutes.
    """
    while True:
        colors = [tuple(np.random.randint(0, 256, size=3)) for i in range(3)]
        create_and_upload_image_by_request(NUM_TRIANGLES, SIZE, colors, mastodon)
        time.sleep(900)  # 15 minutes


if __name__ == '__main__':
    main()
