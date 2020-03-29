import numpy as np
import pandas as pd
import json

actions = pd.read_json('D:/nbc/actions/1hz.json', orient='index')

def actions_meta():
    return actions['z'].value_counts().to_json()

def sample_action(action):
    actions_ = actions[actions['z'] == action]
    actions_ = actions_.sample(n=6, replace=True)
    return actions_.to_json(orient='records')
