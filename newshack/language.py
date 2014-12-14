from nltk.parse.earleychart import EarleyChartParser
from nltk.grammar import (
        CFG as ContextFreeGrammar,
        Production,
        Nonterminal as NT
    )


class Parser:
    def __init__(self, rules_file='rules.gr', vocab_file='vocabulary.gr'):
        self.rules = []
        test_sentences = []

        # get grammar rules
        grammar = open(rules_file, 'r')
        line = grammar.readline()
        while line:
            if line.strip() != '' and not line.strip().startswith('#'):
                line = line[2:]
                parts = line.partition("\t")
                lhs = parts[0].strip()
                rhs = [NT(x) for x in parts[2].strip().split(" ")]
                self.rules.append(Production(NT(lhs), rhs))
            line = grammar.readline()
        grammar.close()

        # get vocab rules
        vocab = open(vocab_file, 'r')
        line = vocab.readline()
        while line:
            if line.strip() != '' and not line.strip().startswith('#'):
                line = line[2:]
                parts = line.partition("\t")
                lhs = parts[0].strip()
                rhs = parts[2].strip().lower().split(" ")
                self.rules.append(Production(NT(lhs), rhs))
            line = vocab.readline()
        vocab.close()

        # create grammar and parser
        self.cfg = ContextFreeGrammar(NT("S"), self.rules)
        self.parser = EarleyChartParser(self.cfg, trace=0)


    def parse_sentence(self, sentence):
        unknown = []
        tokens = sentence.strip().split(" ")

        print tokens
        # todo: handle error states.  also is punctuation always required!?
        parse = self.parser.parse(tokens)
        parse_list = list(parse)

        #print parse_list

        return parse_list[0]
        #try:
        #    parse = list(self.parser.parse(tokens))
        #except:
        #    for token in tokens:
        #       if not self.cfg.covers([token]): unknown.append(token)
        #    parse = None

        #if parse:
        #    return parse[0]
        #else:
        #    return None


    def get_sentence_type(self, parse):
        if isinstance(parse, str):
            return 'unknown'

        print parse.productions()[0]

        lhs = parse.productions()[0].lhs()
        if lhs == NT("Ind_Clause_Ques") or lhs == NT("Ind_Clause_Ques_Aux"):
            return 'question'
        elif lhs == NT("Ind_Clause") or lhs == NT("Ind_Clause_Pl"):
            if parse.productions()[0].rhs()[0] == NT("VP_Inf"):
                return 'command'
            else:
                return 'statement'


        for subtree in parse:
            type = self.get_sentence_type(subtree)
            if type: return type

        return 'unknown'


    def find_topic(self, parse, type, qword=None):
        if isinstance(parse, str): return None
        tree = parse.productions()[0]
        print type, "- tree: ", tree

        if type == 'question':

            if tree.lhs() == NT("Ind_Clause_Ques") or \
               tree.lhs() == NT("Ind_Clause_Ques_Aux"):
                if not qword:
                    qword = parse[0].leaves()[0]
                    print "qword: ", qword

                rhs = tree.rhs()
                if rhs[-1] == NT("VP_3rd"):
                    print "VP_3rd"
                    t = self.find_after_verb(parse[-1][-1])
                    if not t:
                        t = self.find_PP(parse[-1][-1])

                    return t, qword

                elif rhs[-1] == NT("Ind_Clause_Ques_Aux"):
                    print "Ind_Clause_Ques_Aux"
                    return self.find_topic(parse[-1][-1], type='statement'), qword

                elif rhs[-1] == NT("Interrog_Clause"):
                    print "Interrog_Clause"
                    t = self.find_after_verb(parse[-1][-1])
                    if not t:
                        t = self.find_PP(parse[-1][-1])
                    return t, qword

                elif rhs[-1] == NT("Ind_Clause_Inf") or \
                     rhs[-1] == NT("Ind_Clause_Inf_3rd"):
                    print "Ind_Clause_Inf"
                    return self.find_topic(parse[-1], type='statement'), qword
            else:
                for subtree in parse:
                    subj = self.find_topic(subtree, type)
                    if subj: return subj

        elif type == 'statement':
            if tree.lhs() == NT("VP_1st") or \
               tree.lhs() == NT("VP_Inf"):
                t = self.find_after_verb(parse[-1][-1])
                if not t:
                    t = self.find_PP(parse[-1][-1])
                return t
            else:
                for subtree in parse:
                    subj = self.find_topic(subtree, type)
                    if subj: return subj

        elif type == 'command':
            if tree.lhs() == NT("VP_Inf"):
                rhs = tree.rhs()
                if rhs[-1] == NT("PP"):
                    return parse[-1]
                else:
                    return self.find_after_verb(parse)

            elif tree.lhs() == NT("PP"):
                return parse[-1]
            else:
                for subtree in parse:
                    subj = self.find_topic(subtree, type)
                    if subj: return subj

        return None


    def find_PP(self, parse):
        """
        Finds the first prepositional phrase in the parse.
        """
        if isinstance(parse, str): return None
        tree = parse.productions()[0]

        if tree.lhs() == NT("PP"):
            return parse[-1]
        else:
            for subtree in parse:
                pp = self.find_PP(subtree)
                if pp: return pp

        return None


    def find_after_verb(self, parse):
        """
        Finds the first "After_Verb_*" structure in the parse.
        """
        if isinstance(parse, str): return None
        tree = parse.productions()[0]

        if tree.lhs() == NT("After_Verb_Tr") or \
           tree.lhs() == NT("After_Verb_In"):
            return parse
        else:
            for subtree in parse:
                subj = self.find_after_verb(subtree)
                if subj: return subj

