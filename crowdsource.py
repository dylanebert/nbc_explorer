from tqdm import tqdm
from google.cloud import datastore
import random
from datetime import datetime
import pandas as pd

client = datastore.Client()

def find_id():
    methods = ['matching', 'single_trajectories', 'pixelwise', 'conv_transform_absolute', 'svd3', 'random']
    random.shuffle(methods)
    for method in methods:
        query = client.query(kind='entity')
        query.add_filter('n_res', '=', 1)
        query.add_filter('method', '=', method)
        results = list(query.fetch())
        if len(results) > 0:
            print(method)
            choice = random.choice(results)
            return str(choice.key.id)
    return None

def get_entity(id):
    key = client.key('entity', int(id))
    entity = client.get(key)
    return entity

def delete_entity(id):
    clear_responses(id)
    key = client.key('entity', int(id))
    client.delete(key)

def save_response(id, val):
    entity = get_entity(id)
    if entity is None:
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

    key = client.key('entity', int(eid))
    entity = client.get(key)
    entity['n_res'] -= 1
    client.put(entity)

def clear_responses(eid):
    query = client.query(kind='response')
    query.add_filter('eid', '=', int(eid))
    results = list(query.fetch())
    for result in results:
        delete_response(result.key.id)

def clear_all_responses():
    query = client.query(kind='response')
    results = list(query.fetch())
    for result in results:
        delete_response(result.key.id)

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

def get_all_responses():
    query = client.query(kind='response')
    results = list(query.fetch())
    return results

def summarize():
    responses = get_all_responses()
    report = []
    for response in responses:
        entity = get_entity(response['eid'])
        if entity is None:
            continue
        row = {
            'eid': response['eid'],
            'method': entity['method'],
            'q1': -response['q1'] + 2,
            'q2': -response['q2'] + 2,
            'q3': -response['q3'] + 2
        }
        report.append(row)
    report = pd.DataFrame(report)
    print(report.groupby('method').mean()[['q1', 'q2', 'q3']])
    report.to_json('/media/dylan/Elements/nbc/report.json', orient='index')

    '''agreed = 0; sum = 0
    for _, group in report.groupby('eid'):
        if len(group) > 1:
            for key in ['q1', 'q2', 'q3']:
                if group.iloc[0][key] == group.iloc[1][key]:
                    agreed += 1
                sum += 1
    print(agreed / float(sum))
    print(report.groupby('method').mean()[['q1', 'q2', 'q3']])'''

if __name__ == '__main__':
    summarize()
