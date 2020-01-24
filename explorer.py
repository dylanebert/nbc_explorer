import os
import sys
import json
import shutil
from parse_captions import SVO
import pandas as pd
from tqdm import tqdm

phrases = pd.read_json('phrases.json', orient='index')
phrases_old = pd.read_json('phrases_old.json', orient='index')

def get_phrases():
    phrases_ = phrases[['participant', 'task', 'verb', 'object']]
    return phrases_.to_json(orient='index')

def get_phrases_old():
    phrases_old_ = phrases_old[['participant', 'task', 'caption', 'phrase']]
    return phrases_old_.to_json(orient='index')

def get_phrase_data(idx, method='hand_seg'):
    phrase = phrases.loc[idx]
    seg = json.loads(phrase[method])
    steps = range(seg['start_step'], seg['end_step'], 3)
    urls = ['https://storage.googleapis.com/nbc_release/{0}/{0}_task{1}/{2}.png'.format(
        phrase['participant'], phrase['task'], step) for step in steps]
    vid_url = 'https://storage.googleapis.com/nbc_release/videos/{}/{}.mp4'.format(
        method, idx)
    data = {
        'phrase': phrase['phrase'],
        'caption': phrase['caption'],
        'start_step': seg['start_step'],
        'end_step': seg['end_step'],
        'images': urls,
        'video': vid_url
    }
    return json.dumps(data)

with open('questions.json') as f:
    questions = json.loads(f.read())
def get_questions(idx):
    idx = str(idx)
    if idx not in questions:
        raise ValueError('Couldn\'t find questions for {}'.format(idx))
    return json.dumps(questions[idx])

def copy_phrase_images():
    for method in ['obj_seg', 'hand_seg']:
        for idx, row in tqdm(phrases.iterrows(), total=len(phrases)):
            try:
                phrase_data = json.loads(get_phrase_data(idx, method))
            except:
                print(method, idx, row)
                continue
            dest_dir = '/media/dylan/Elements/nbc/videos/{}/src/{}'.format(method, idx)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            i = 0
            for url in phrase_data['images']:
                source = url.replace('https://storage.cloud.google.com/nbc_release',
                    '/media/dylan/Elements/nbc/images')
                dest = os.path.join(dest_dir, '{:04d}.png'.format(i))
                if os.path.exists(source) and not os.path.exists(dest):
                    shutil.copy(source, dest)
                    i += 1

if __name__ == '__main__':
    pass
