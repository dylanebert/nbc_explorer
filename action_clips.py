import pandas as pd
import numpy as np
import json

def get_phrase(word, words):
    words_ = words[words['phrase'] == word['phrase']]
    return ' '.join(words_['word'].values)

def get_action(word, words, actions):
    z_offset = sorted(list(set(actions['z'])))[-1]
    actions_ = actions[(actions['participant'] == word['participant']) \
        & (actions['task'] == word['task'])]
    action = actions_[(word['end_step'] > actions_['start_step']) \
        & (word['end_step'] <= actions['end_step'])]
    if not len(action) == 1:
        return None
    action = action.iloc[0]
    word['action_z'] = action['z']
    word['action_start_step'] = action['start_step']
    word['action_end_step'] = action['end_step']
    word['action_start_obj'] = action['start_obj']
    word['action_end_obj'] = action['end_obj']
    word['action_idx'] = action.name
    if word['action_end_obj'] == None:
        word['action'] = action['z']
    else:
        word['action'] = action['z'] + z_offset
    return word

def get_word(word):
    import os
    if os.path.exists('D:/nbc/case/{0}.json'.format(word)):
        return pd.read_json('D:/nbc/case/{0}.json'.format(word), orient='index')
    words = pd.read_json('D:/nbc/words.json', orient='index')
    words['full_phrase'] = words.apply(lambda row: get_phrase(row, words), axis=1)
    rows = words[words['lemma'] == word]
    rows = rows.apply(lambda row: get_action(row, words, actions), axis=1)
    rows.dropna(how='all', inplace=True)
    rows.to_json('D:/nbc/case/{0}.json'.format(word), orient='index')

def shift(idx, shift):
    shifted = actions.loc[idx + shift]
    if shift > 0:
        if not actions.loc[idx + shift - 1]['end_step'] == shifted['start_step']:
            return ''
    if shift < 0:
        if not actions.loc[idx + shift + 1]['start_step'] == shifted['end_step']:
            return ''
    return shifted.to_json()

actions = pd.read_json('D:/nbc/segments/final.json', orient='index').sort_values(by=['participant', 'task', 'end_step'])
pick = get_word('pick').sort_values(by=['action', 'participant', 'task'])
def get_pick(i):
    print(pick.iloc[i]['action_idx'])
    return pick.iloc[i].to_json()

if __name__ == '__main__':
    s = pick.iloc[4]
    print(shift(s['action_idx'], 1))
