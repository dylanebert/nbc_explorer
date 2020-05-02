import numpy as np
import pandas as pd
import json

def actions_meta():
    global actions
    actions = pd.read_json('partial_states.json', orient='index')
    return actions['state'].value_counts().to_json()

def sample_action(action):
    global actions
    sample = actions[actions['state'] == action]
    sample = sample.sample(n=6, replace=True)
    frames = []
    for i, frame in sample.iterrows():
        startstep = i
        endstep = i
        while startstep > 0 and actions.iloc[startstep-1]['state'] == frame['state']:
            startstep -= 1
        while endstep < len(actions) - 1 and actions.iloc[endstep]['state'] == frame['state']:
            endstep += 1
        frames.append({
            'start_step': actions.iloc[startstep]['step'],
            'end_step': actions.iloc[endstep]['step'],
            'participant': frame['participant'],
            'task': frame['task']
        })
    return pd.DataFrame(frames).to_json(orient='index')
