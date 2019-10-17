import os
import sys
import pickle
import json
import shutil
from parse_captions import SVO
from tqdm import tqdm
from google.cloud import datastore
import random
from datetime import datetime

SKIP = 3

with open('phrases.p', 'rb') as f:
    phrases = pickle.load(f)
client = datastore.Client()

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

def get_phrase(idx):
    return phrases.iloc[idx].drop('svo').to_json()

def get_svo(idx):
    phrase = phrases.iloc[idx]
    svo = phrase['svo'].df
    return svo.to_json(orient='index')

def get_images(idx):
    urls = []
    phrase = phrases.iloc[idx]
    steps = range(phrase['start_step'] - 450, phrase['end_step'] + 450, SKIP)
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

def save_response(id, res):
    key = client.key('response', int(id))
    entity = client.get(key)
    entity['res'] = res
    entity['modified'] = datetime.now()
    client.put(entity)
    print('Saved {}: {}'.format(id, res))

def get_response(id):
    key = client.key('response', int(id))
    entity = client.get(key)
    if entity is None:
        return json.dumps('dne')
    if entity['res'] is not 0:
        print('Warning: Entity {} already has response'.format(id))
    return json.dumps(entity)

def find_id():
    query = client.query(kind='response')
    query.add_filter('res', '=', 0)
    results = list(query.fetch())
    if len(results) is 0:
        return json.dumps('No entities remaining')
    choice = random.choice(results)
    return json.dumps(str(choice.key.id))

def generate_responses():
    for idx, phrase in phrases.iterrows():
        pid, qid = idx, idx #phrase matches video
        id = hash('{},{}'.format(pid, qid))
        key = client.key('response', id)
        entity = datastore.Entity(key=key)
        entity['pid'] = pid; entity['qid'] = qid
        entity['res'] = 0; entity['sess'] = 0;
        client.put(entity)

if __name__ == '__main__':
    id = find_id()
    print(get_response(id))
