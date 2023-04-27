import os
import time
import numpy as np
from mastodon import Mastodon
from PIL import Image, ImageDraw, ImageFilter

# Ваши данные доступа к Mastodon
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
access_token = 'ACCESS_TOKEN'
base_url = 'https://mstdn.bronyfurry.com'

mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=access_token,
    api_base_url=base_url
)

num_triangles = 5
size = 512

def generate_image_with_colors(num_triangles, size, colors):
    image = Image.new('RGB', (size, size), color=colors[0])
    draw = ImageDraw.Draw(image)

    for i in range(num_triangles):
        vertices = [
            (np.random.randint(0, size), np.random.randint(0, size)),
            (np.random.randint(0, size), np.random.randint(0, size)),
            (np.random.randint(0, size), np.random.randint(0, size))
        ]
        draw.polygon(vertices, fill=colors[np.random.randint(0, len(colors))])

    return image


def create_and_upload_image_by_request(num_triangles, size, colors, mastodon):
    image = generate_image_with_colors(num_triangles, size, colors)
    image_path = 'image.png'
    image.save(image_path)
    media_dict = mastodon.media_post(image_path)
    mastodon.status_post(status='Here is your image!', media_ids=[media_dict['id']])
    os.remove(image_path)


def main():
    while True:
        create_and_upload_image_by_request(num_triangles, size, [tuple(np.random.randint(0, 256, size=3)) for i in range(3)], mastodon)
        time.sleep(9000) # 15 минут

if __name__ == '__main__':
    main()
