import pandas as pd
import pyinflect
import inflect
import numpy as np

p = inflect.engine()

class SVOParser:
    def __init__(self, svo):
        self.svo = svo
        q1 = self.generate_q1()
        if self.has_object():
            obj = self.get_object()
            q2 = self.generate_q2(obj)
            q3 = self.generate_q3(obj, q1)
            self.questions = [q1, q2, q3]
        else:
            self.questions = [q1]

    def has_object(self):
        return 'dobj' in self.svo['dep'].values

    def has_particle(self):
        return 'prt' in self.svo['dep'].values

    def get_verb(self):
        if any(comp in self.svo['dep'].values for comp in ['xcomp', 'ccomp', 'pcomp']):
            return self.svo[self.svo['dep'].isin(['xcomp', 'ccomp', 'pcomp'])].iloc[0]['lemma']
        elif 'ROOT' in self.svo['dep'].values:
            return self.svo[self.svo['dep'] == 'ROOT'].iloc[0]['lemma']
        elif any(comp in self.svo['dep'].values for comp in ['acl', 'relcl', 'advcl', 'conj']):
            return self.svo[self.svo['dep'].isin(['acl', 'relcl', 'advcl', 'conj'])].iloc[0]['lemma']
        else:
            raise 'Couldn\'t find verb'

    def get_object(self):
        obj = self.svo[self.svo['dep'] == 'dobj'].iloc[0]
        if not pd.isna(obj['coref']):
            coref = obj['coref'].split('/')[0]
            if ' ' in coref:
                coref = coref.split(' ')[-1]
            obj = coref
        else:
            obj = obj['token']
        return obj

    def generate_q1(self):
        verb = self.get_verb()
        try:
            pp = pyinflect.getInflection(verb, tag='VBG')[0]
        except:
            raise 'Couldn\'t inflect verb'
        q1 = 'The person is {}'.format(pp)
        if self.has_object():
            q1 += ' something'
        if self.has_particle():
            particle = self.svo[self.svo['dep'] == 'prt'].iloc[0]['token']
            q1 += ' {}'.format(particle)
        return q1

    def generate_q2(self, obj):
        if p.singular_noun(obj) is False:
            obj = p.a(obj)
        return 'There is {} in the video'.format(obj)

    def generate_q3(self, obj, q1):
        if p.singular_noun(obj) is False and obj not in ['it', 'him', 'her', 'them']:
            obj = 'the {}'.format(obj)
        q3 = q1.replace('something', obj)
        return q3
