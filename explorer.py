import os
import sys
import json
import shutil
import pandas as pd
from tqdm import tqdm

phrases = pd.read_json('phrases.json', orient='index')[['participant', 'task', 'caption', 'phrase']].to_json(orient='index')
def get_legacy_phrases():
    return phrases

if __name__ == '__main__':
    print(phrases)
