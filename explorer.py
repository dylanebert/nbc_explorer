import os
import sys
import json
import shutil
from parse_captions import SVO
import pandas as pd

phrases = pd.read_json('phrases.json', orient='index')

def get_phrases():
    d = {}
    phrases_ = phrases.drop('svo', axis=1)
    print(phrases_)
    groups = phrases_.groupby(['participant', 'task', 'caption']) \
        .apply(lambda x: x.to_json(orient='index'))
    for (k1, k2, k3), v in groups.items():
        if k1 in d:
            if k2 in d[k1]:
                d[k1][k2][k3] = json.loads(v)
            else:
                d[k1][k2] = {}
        else:
            d[k1] = {}
    return d

def get_images(idx):
    urls = []
    phrase = phrases.loc[idx]
    steps = range(phrase['start_step'] - 450, phrase['end_step'] + 450, 3)
    for step in steps:
        url = 'https://storage.cloud.google.com/nbc_release/{0}/{0}_task{1}/{2}.png'.format(phrase['participant'], phrase['task'], step)
        urls.append(url)
    return urls

def copy_phrase_images():
    for idx, row in tqdm(phrases.iterrows(), total=len(phrases)):
        urls = get_images(idx)
        dest_dir = '/media/dylan/Elements/nbc/phrases/src/{}'.format(idx)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        i = 0
        for url in urls:
            if os.path.exists(url):
                dest = os.path.join(dest_dir, '{:04d}.png'.format(i))
                shutil.copy(url, dest)
                i += 1

if __name__ == '__main__':
    phrases = get_phrases()
