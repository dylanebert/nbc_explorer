import numpy as np
import pandas as pd
import json

def get_paths():
    return json.dumps([
        'partial_states_kappa=10.json',
        'partial_states_kappa=50.json',
        'partial_states_kappa=100.json',
        'partial_states_kappa=200.json',
        'partial_states_kappa=500.json',
        'partial_states_kappa=1000.json',
        'partial_states_latentdim=2_beta=0_KMeans=20.json',
        'partial_states_latentdim=2_beta=0_KMeans=50.json',
        'partial_states_latentdim=2_beta=0_KMeans=100.json',
        'partial_states_latentdim=2_beta=0_KMeans=200.json',
        'partial_states_latentdim=3_beta=0_KMeans=20.json',
        'partial_states_latentdim=3_beta=0_KMeans=50.json',
        'partial_states_latentdim=3_beta=0_KMeans=100.json',
        'partial_states_latentdim=3_beta=0_KMeans=200.json',
        'partial_states_latentdim=4_beta=0_KMeans=20.json',
        'partial_states_latentdim=4_beta=0_KMeans=50.json',
        'partial_states_latentdim=4_beta=0_KMeans=100.json',
        'partial_states_latentdim=4_beta=0_KMeans=200.json'
    ])

def get_actions(path):
    actions = pd.read_json('static/states/' + path, orient='index')
    return actions['state'].value_counts().to_json()

def sample_action(path, action):
    actions = pd.read_json('static/states/' + path, orient='index')
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
