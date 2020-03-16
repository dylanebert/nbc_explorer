from tqdm import tqdm
from google.cloud import datastore
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

client = datastore.Client()

def find_id():
    methods = ['action_given_word', 'word_given_action', 'action_given_word_normalized', 'word_given_action_normalized']
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
    colors = ['g', 'y', 'r']
    x_pos_major = []
    x_ticks_major = []
    x_pos_minor = []
    x_ticks_minor = []
    i = 0
    for method in ['aligned', 'random_aligned', 'match_end', 'match_end_arbitrary', 'random']:
        j = 0
        for hmm in ['niekum1', 'niekum2', 'niekum3', 'niekum_relative1']:
            rows = report[(report['method'] == method) & (report['hmm'] == hmm)]
            map_q = [0, 1, 3, 2]
            counts = {1: 0, 2: 0, 3: 0}
            sum = 0
            for q, count in rows['q'].value_counts().iteritems():
                counts[map_q[q]] = count
                sum += count
            for k in [1, 2, 3]:
                counts[k] /= sum
            x_pos_minor.append(i * 5 + j)
            x_ticks_minor.append(hmm)
            for k in range(3):
                x = i * 5 + j + .2 * (k - 1)
                y = counts[k + 1]
                ax.bar(x, y, width=.2, color=colors[k % 3], align='center')
            j += 1
        x_pos_major.append(i * 5 + 1.5)
        x_ticks_major.append(method)
        i += 1
    plt.xticks(x_pos_major, x_ticks_major, rotation=90)
    #plt.xticks(x_pos_minor, x_ticks_minor, rotation=90)
    plt.tight_layout()
    plt.show()

def plot_methods_concise():
    report = pd.read_json('/media/dylan/Elements/nbc/report.json', orient='index')
    ax = plt.subplot(111)
    x_pos = []
    x_ticks = []
    i = 0
    for method in ['aligned', 'match_end', 'match_end_arbitrary', 'random']:
        j = 0
        for hmm in ['niekum1', 'niekum2', 'niekum3', 'niekum_relative1']:
            rows = report[(report['method'] == method) & (report['hmm'] == hmm)]
            value = 0
            map = {1: 1, 2: 0, 3: .5}
            for q, count in rows['q'].value_counts().iteritems():
                value += map[q] * count
            value /= len(rows)
            label = '{} : {}'.format(method, hmm)
            x = i * 5 + j
            ax.bar(x, value)
            j += 1
        x_pos.append(i * 5 + 1.5)
        x_ticks.append(method)
        i += 1
    plt.xticks(x_pos, x_ticks, rotation=90)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    #get_report()
    report = pd.read_json('/media/dylan/Elements/nbc/report.json', orient='index')
    print(report[report['method'] == 'random_aligned']['hmm'].value_counts())
    #plot_methods()
    #plot_methods_concise()
    pass
