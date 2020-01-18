import os
import sys
import json
import shutil
from parse_captions import SVO
import pandas as pd

phrases = pd.read_json('D:/nbc/phrases.json', orient='index')

def get_phrases():
    phrases_ = phrases[['participant', 'task', 'verb', 'object']]
    return phrases_.to_json(orient='index')

def get_phrase_data(idx, method='hand_seg'):
    phrase = phrases.loc[idx]
    seg = json.loads(phrase[method])
    data = {
        'phrase': phrase['phrase'],
        'caption': phrase['caption'],
        'start_step': seg['start_step'],
        'end_step': seg['end_step']
    }
    return json.dumps(data)

def get_images(idx, method='hand_seg'):
    urls = []
    phrase = phrases.loc[idx]
    seg = json.loads(phrase[method])
    steps = range(seg['start_step'], seg['end_step'], 3)
    for step in steps:
        #url = 'D:/nbc/images/{0}/{0}_task{1}/{2}.png'.format(phrase['participant'], phrase['task'], step)
        url = 'https://storage.cloud.google.com/nbc_release/{0}/{0}_task{1}/{2}.png'.format(phrase['participant'], phrase['task'], step)
        urls.append(url)
    return json.dumps(urls)

if __name__ == '__main__':
    print(get_images(0))
    pass
