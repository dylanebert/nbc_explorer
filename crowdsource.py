from tqdm import tqdm
from google.cloud import datastore
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

client = datastore.Client()

def find_id():
    methods = ['aligned', 'match_end', 'match_end_arbitrary', 'random']
    random.shuffle(methods)
    for method in methods:
        query = client.query(kind='segment')
        query.add_filter('n_res', '=', 0)
        query.add_filter('method', '=', method)
        results = list(query.fetch())
        if len(results) > 0:
            print(method)
            choice = random.choice(results)
            return str(choice.key.id)
    return None

def get_entity(id):
    key = client.key('segment', int(id))
    entity = client.get(key)
    return entity

def delete_entity(id):
    clear_responses(id)
    key = client.key('segment', int(id))
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
    res['eid'] = int(id)
    res['date'] = date
    res['q'] = val
    client.put(res)
    print('Saved {}: {}'.format(id, val))

def delete_response(id):
    key = client.key('response', int(id))
    response = client.get(key)
    eid = response['eid']
    client.delete(key)

    key = client.key('segment', int(eid))
    entity = client.get(key)
    if entity is not None:
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
    query = client.query(kind='segment')
    results = list(query.fetch())
    for result in tqdm(results):
        delete_entity(result.key.id)

def recount():
    query = client.query(kind='segment')
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

def get_report():
    responses = get_all_responses()
    report = []
    for response in responses:
        entity = get_entity(response['eid'])
        if entity is None:
            continue
        row = {
            'method': entity['method'],
            'q': response['q'],
            'verb': entity['verb'],
            'hmm': entity['hmm']
        }
        report.append(row)
    report = pd.DataFrame(report)
    report.to_json('/media/dylan/Elements/nbc/report.json', orient='index')

def plot_methods():
    report = pd.read_json('/media/dylan/Elements/nbc/report.json', orient='index')
    ax = plt.subplot(111)
    colors = ['g', 'r', 'y']
    xticks = []
    groups = report.groupby(['method', 'hmm'])
    for i, ([method, hmm], rows) in enumerate(groups):
        counts = {1: 0, 2: 0, 3: 0}
        for q, count in rows['q'].value_counts().iteritems():
            counts[q] = count
        label = '{} : {}'.format(method, hmm)
        xticks.append(label)
        for j in range(3):
            x = i + .2 * (j - 1)
            y = counts[j + 1]
            ax.bar(x, y, width=.2, color=colors[j % 3], align='center')
    plt.xticks(range(len(groups)), xticks, rotation=90)
    plt.tight_layout()
    plt.show()

def plot_methods_concise():
    report = pd.read_json('/media/dylan/Elements/nbc/report.json', orient='index')
    ax = plt.subplot(111)
    xticks = []
    groups = report.groupby(['method', 'hmm'])
    for i, ([method, hmm], rows) in enumerate(groups):
        value = 0
        map = {1: 1, 2: 0, 3: .5}
        for q, count in rows['q'].value_counts().iteritems():
            value += map[q] * count
        value /= len(rows)
        label = '{} : {}'.format(method, hmm)
        xticks.append(label)
        ax.bar(i, value)
    plt.xticks(range(len(groups)), xticks, rotation=90)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    #plot_methods()
    plot_methods_concise()
    pass
