import gdown
import sys

URL = 'https://drive.google.com/file/d/1Ga_QU6PFZYkxt1Qy7h_roW-OZKToO22H/view?usp=sharing'

file_id = URL.split('/')[-2]

prefix = 'https://drive.google.com/uc?export=download&id='

gdown.download(prefix + file_id, 'test.jpg', quiet=False)
