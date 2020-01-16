import os
import sys
import json
import shutil
from parse_captions import SVO
import pandas as pd

phrases = pd.read_json('/media/dylan/Elements/nbc/phrases.json', orient='index')

def get_phrases():
    phrases_ = phrases[['participant', 'task', 'verb', 'object']]
    return phrases_.to_json(orient='index')

def get_phrase_data(idx):
    phrase = phrases.loc[idx]
    data = {
        'phrase': phrase['phrase'],
        'caption': phrase['caption']
    }
    return json.dumps(data)

def get_images(idx, method='hand_seg'):
    urls = []
    phrase = phrases.loc[idx]
    seg = phrase[method]
    steps = range(seg['start_step'], seg['end_step'], 6)
    for step in steps:
        url = 'https://storage.cloud.google.com/nbc_release/{0}/{0}_task{1}/{2}.png'.format(phrase['participant'], phrase['task'], step)
        urls.append(url)
    return urls

if __name__ == '__main__':
    pass
