import os
import sys
import pickle
import json
import shutil
from parse_captions import SVO

SKIP = 3

with open('phrases.p', 'rb') as f:
    phrases = pickle.load(f)

def get_phrases():
    d = {}
    phrases_ = phrases.drop('svo', axis=1)
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
    return json.dumps(d)

def get_images(idx):
    urls = []
    phrase = phrases.iloc[idx]
    steps = range(phrase['start_step'] - 450, phrase['end_step'] + 450, SKIP)
    for step in steps:
        url = 'https://storage.cloud.google.com/nbc_release/{0}/{0}_task{1}/{2}.png'.format(phrase['participant'], phrase['task'], step)
        urls.append(url)
    return json.dumps(urls)

def get_phrase(idx):
    phrase = phrases.iloc[idx]
    svo = phrase['svo'].df
    return svo.to_json(orient='index')

if __name__ == '__main__':
    images = get_images(0)
    print(len(json.loads(images)))
    print('')
