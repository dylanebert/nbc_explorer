import pandas as pd
import numpy as np

actions = pd.read_json('D:/nbc/segments/final.json', orient='index')
words = pd.read_json('D:/nbc/words.json', orient='index')
z_offset = sorted(list(set(actions['z'])))[-1]

def get_phrase(word):
    words_ = words[words['phrase'] == word['phrase']]
    return ' '.join(words_['word'].values)

def get_current_action(word):
    actions_ = actions[(actions['participant'] == word['participant']) \
        & (actions['task'] == word['task'])]
    action = actions_[(actions_['start_step'] < word['end_step']) \
        & (actions['end_step'] >= word['end_step'])]
    if len(action) == 1:
        action = action.iloc[0]
        word['action_z'] = action['z']
        word['action_start_step'] = action['start_step']
        word['action_end_step'] = action['end_step']
        word['action_start_obj'] = action['start_obj']
        word['action_end_obj'] = action['end_obj']
        if word['action_end_obj'] == None:
            word['action'] = action['z']
        else:
            word['action'] = action['z'] + z_offset
    return word

if __name__ == '__main__':
    words['full_phrase'] = words.apply(lambda row: get_phrase(row), axis=1)

    pick = words[words['lemma'] == 'pick']
    pick = pick.apply(lambda row: get_current_action(row), axis=1)
    action_counts = pick['action'].value_counts()
    print(pick['action'].value_counts())
