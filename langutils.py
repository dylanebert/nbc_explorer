import pandas as pd
import pyinflect
import inflect
import numpy as np
import pickle
import json

p = inflect.engine()

class SVOParser:
    def __init__(self, svo):
        self.svo = svo
        subject = self.get_subject()
        first_person = subject in ['i', 'we', '\'s', 'us', 'you']
        verb = self.get_verb()
        object = self.get_object()
        particle = self.get_particle()
        subject, verb, object = self.filter(subject, verb, object)
        self.questions = []
        q1, q2, q3 = [None] * 3
        q1 = self.q1(first_person, subject, verb, object, particle)
        q2 = self.q2(first_person, subject, object)
        q3 = self.q3(first_person, subject, verb, object, particle)
        self.questions = [q1, q2, q3]
        #print(self.questions)

    def q1(self, first_person, subject, verb, object, particle):
        try:
            if not first_person and object is not None:
                verb = self.inflect_verb(verb, tag='VBN')
            else:
                verb = self.inflect_verb(verb, tag='VBG')
        except:
            return None

        q1 = None
        if first_person:
            if object is not None:
                q1 =  'The person is {} something'.format(verb)
            else:
                q1 = 'The person is {}'.format(verb)
        else:
            if object is not None:
                q1 = 'Something is being {}'.format(verb)
            else:
                q1 = 'Something is {}'.format(verb)

        if particle is not None:
            q1 += ' {}'.format(particle)

        return q1

    def q2(self, first_person, subject, object):
        item = None
        if not first_person and object is None and subject is not None:
            item = subject
        else:
            item = object

        if item is None:
            return None

        if p.singular_noun(item):
            return 'There are {}'.format(item)
        else:
            item = p.a(item)
            return 'There is {}'.format(item)

    def q3(self, first_person, subject, verb, object, particle):
        item = None
        if not first_person and object is None and subject is not None:
            item = subject
        else:
            item = object

        try:
            if not first_person and item is not None:
                verb = self.inflect_verb(verb, tag='VBN')
            else:
                verb = self.inflect_verb(verb, tag='VBG')
        except:
            return None

        if item is not None:
            if p.singular_noun(item) is False:
                item = 'the {}'.format(item)

        q3 = None
        if first_person:
            if item is not None:
                q3 =  'The person is {} {}'.format(verb, item)
        elif item is not None:
            if item is not subject:
                if p.singular_noun(item):
                    q3 = '{} are being {}'.format(item.capitalize(), verb)
                else:
                    q3 = '{} is being {}'.format(item.capitalize(), verb)
            else:
                if p.singular_noun(item):
                    q3 = '{} are {}'.format(item.capitalize(), verb)
                else:
                    q3 = '{} is {}'.format(item.capitalize(), verb)

        if q3 is not None and particle is not None:
            q3 += ' {}'.format(particle)

        return q3

    def get_subject(self):
        if 'nsubj' in self.svo['dep'].values:
            subj = self.svo[self.svo['dep'] == 'nsubj'].iloc[0]['token'].lower()
            return subj
        return None

    def get_verb(self):
        verb = None
        if any(comp in self.svo['dep'].values for comp in ['xcomp', 'ccomp', 'pcomp']):
            verb = self.svo[self.svo['dep'].isin(['xcomp', 'ccomp', 'pcomp'])].iloc[0]['lemma']
        elif 'ROOT' in self.svo['dep'].values:
            verb = self.svo[self.svo['dep'] == 'ROOT'].iloc[0]['lemma']
        elif any(comp in self.svo['dep'].values for comp in ['acl', 'relcl', 'advcl', 'conj']):
            verb = self.svo[self.svo['dep'].isin(['acl', 'relcl', 'advcl', 'conj'])].iloc[0]['lemma']
        return verb

    def inflect_verb(self, verb, tag='VBG'):
        try:
            return pyinflect.getInflection(verb, tag=tag)[0]
        except:
            raise 'Couldn\'t inflect verb "{}"'.format(verb)

    def get_object(self):
        if 'dobj' in self.svo['dep'].values:
            obj = self.svo[self.svo['dep'] == 'dobj'].iloc[0]
            if not pd.isna(obj['coref']):
                coref = obj['coref'].split('/')[0]
                if ' ' in coref:
                    coref = coref.split(' ')[-1]
                obj = coref
            else:
                obj = obj['token']
            obj = obj.lower()
            return obj
        return None

    def get_particle(self):
        if 'prt' in self.svo['dep'].values:
            return self.svo[self.svo['dep'] == 'prt'].iloc[0]['token']
        return None

    def filter(self, subject, verb, object):
        if verb in ['be']:
            verb = None
        invalid = ['it', 'him', 'her', 'them', 'one', 'thing', 'what', 'that', 'this', 'they']
        if subject in invalid:
            subject = None
        if object in invalid:
            object = None
        if verb in ['go', 'put', 'pick', 'take'] and object is None:
            verb = None
        return subject, verb, object

if __name__ == '__main__':
    with open('phrases.p', 'rb') as f:
        phrases = pickle.load(f)
    questions = {}
    for idx, row in phrases.iterrows():
        parser = SVOParser(row['svo'].df)
        questions[idx] = parser.questions
    with open('questions.json', 'w+') as f:
        f.write(json.dumps(questions, indent=4))
