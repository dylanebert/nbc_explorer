import numpy as np
import pandas as pd
import json

def actions_meta(method):
    global actions
    actions = pd.read_json('actions/{}.json'.format(method), orient='index')
    return actions['z'].value_counts().to_json()

def sample_action(action):
    global actions
    actions_ = actions[actions['z'] == action]
    actions_ = actions_.sample(n=6, replace=True)
    return actions_.to_json(orient='records')
