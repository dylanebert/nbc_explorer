import pandas as pd
import pyinflect
import inflect
import numpy as np
import pickle

p = inflect.engine()

class SVOParser:
    def __init__(self, svo):
        self.svo = svo
        first_person = self.first_person()
        verb = self.get_verb()
        object = self.get_object()
        particle = self.get_particle()
        verb, object = self.filter(verb, object)
        self.questions = []
        q1, q2, q3 = [None] * 3
        q1 = self.q1(first_person, verb, object, particle)
        if object is not None:
            q2 = self.q2(object)
        q3 = self.q3(first_person, verb, object, particle)
        self.questions = [q1, q2, q3]
        for q in self.questions:
            if q is not None:
                pass
                #print(q)
        #print('')

    def q1(self, first_person, verb, object, particle):
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
            print(q1)

        if particle is not None:
            q1 += ' {}'.format(particle)

        return q1

    def q2(self, object):
        if p.singular_noun(object):
            return 'There are {}'.format(object)
        else:
            object = p.a(object)
            return 'There is {}'.format(object)

    def q3(self, first_person, verb, object, particle):
        try:
            if not first_person and object is not None:
                verb = self.inflect_verb(verb, tag='VBN')
            else:
                verb = self.inflect_verb(verb, tag='VBG')
        except:
            return None

        if object is not None:
            if p.singular_noun(object) is False:
                object = 'the {}'.format(object)

        q3 = None
        if first_person:
            if object is not None:
                q3 =  'The person is {} {}'.format(verb, object)
        else:
            if object is not None:
                if p.singular_noun(object):
                    q3 = '{} are being {}'.format(object.capitalize(), verb)
                else:
                    q3 = '{} is being {}'.format(object.capitalize(), verb)
                print(q3)

        if q3 is not None and particle is not None:
            q3 += ' {}'.format(particle)

        return q3

    def first_person(self):
        if 'nsubj' in self.svo['dep'].values:
            subj = self.svo[self.svo['dep'] == 'nsubj'].iloc[0]['token'].lower()
            if subj not in ['i', 'we', '\'s', 'us']:
                return False
        return True

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

    def filter(self, verb, object):
        if verb in ['be']:
            verb = None
        if object in ['it', 'him', 'her', 'them', 'me', 'one']:
            object = None
        if verb in ['go', 'put', 'pick', 'take'] and object is None:
            verb = None
        return verb, object

if __name__ == '__main__':
    with open('phrases.p', 'rb') as f:
        phrases = pickle.load(f)
    questions = {}
    for idx, row in phrases.iterrows():
        parser = SVOParser(row['svo'].df)
        questions[idx] = parser.questions
    #with open('questions.p', 'wb+') as f:
        #pickle.dump(questions, f)
