from tqdm import tqdm
from google.cloud import datastore
import random
from datetime import datetime
from explorer import phrases

client = datastore.Client()

def find_id():
    query = client.query(kind='entity')
    query.add_filter('n_res', '=', 0)
    results = list(query.fetch())
    if len(results) is 0:
        return 'No entities remaining'
    choice = random.choice(results)
    return str(choice.key.id)

def get_entity(id):
    key = client.key('entity', int(id))
    entity = client.get(key)
    if entity is None:
        print('dne')
        return 'dne'
    else:
        return entity

def delete_entity(id):
    clear_responses(id)
    key = client.key('entity', int(id))
    client.delete(key)

def save_response(id, val):
    entity = get_entity(id)
    if entity is 'dne':
        return entity
    else:
        entity['n_res'] += 1
    client.put(entity)

    date = datetime.now()
    key_id = hash('{},{}'.format(id, date))
    key = client.key('response', key_id)
    res = datastore.Entity(key)
    res['eid'] = id
    res['date'] = date
    k = 1
    for q in val:
        res['q{}'.format(k)] = q
        k += 1
    client.put(res)
    print('Saved {}: {}'.format(id, val))

def delete_response(id):
    key = client.key('response', int(id))
    response = client.get(key)
    eid = response['eid']
    client.delete(key)

    key = client.key('entity', int(id))
    entity = client.get(key)
    entity['n_res'] -= 1
    client.put(entity)

    print('deleted {}'.format(id))

def clear_responses(eid):
    query = client.query(kind='response')
    query.add_filter('eid', '=', int(eid))
    results = list(query.fetch())
    for result in results:
        delete_response(result.key.id)

def generate_entities():
    from explorer import phrases
    for idx, phrase in tqdm(phrases.iterrows(), total=len(phrases)):
        pid, qid = idx, idx #phrase matches video
        id = hash('{},{}'.format(pid, qid))
        key = client.key('entity', id)
        entity = datastore.Entity(key=key)
        entity['pid'] = pid; entity['qid'] = qid
        entity['n_res'] = 0
        client.put(entity)

def clear_entities():
    query = client.query(kind='entity')
    results = list(query.fetch())
    for result in tqdm(results):
        delete_entity(result.key.id)

def recount():
    query = client.query(kind='entity')
    entities = list(query.fetch())
    for entity in tqdm(entities):
        res_query = client.query(kind='response')
        res_query.add_filter('eid', '=', int(entity.key.id))
        res = list(res_query.fetch())
        if entity['n_res'] is not len(res):
            print('Updating {} n_res from {} to {}'.format(entity.key.id, entity['n_res'], len(res)))
            entity['n_res'] = len(res)
            client.put(entity)

if __name__ == '__main__':
    pass
