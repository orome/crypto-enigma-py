#!/usr/bin/env python
# encoding: utf8

""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)


def numA0(ch):
    return ord(ch) - ord('A')

def chrA0(i):
    return chr(i + ord('A'))

# ASK - How to make private so it can't be instantiated outside of module? Make private to EnigmaConfig? <<<
class Component(object):

     def __init__(self, name, wiring, turnovers):

        self.name = name
        self.wiring = wiring
        self.turnovers = turnovers

# REV - Better way to initialize and store these as constants? <<<
comps = {}

rots = {}
comps["I"] = rots["I"] = Component("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q")
comps["II"] = rots["II"] = Component("II","AJDKSIRUXBLHWTMCQGZNPYFVOE","E")
comps["III"] = rots["III"] = Component("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V") 
comps["IV"] = rots["IV"] = Component("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
comps["V"] = rots["V"] = Component("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
comps["VI"] = rots["VI"] = Component("VI", "JPGVOUMFYQBENHZRDKASXLICTW", "ZM") 
comps["VII"] = rots["VII"] = Component("VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM") 
comps["VIII"] = rots["VIII"] = Component("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM") 
comps["β"] = rots["β"] = Component("β", "LEYJVCNIXWPBQMDRTAKZGFUHOS", "") 
comps["γ"] = rots["γ"] = Component("γ", "FSOKANUERHMBTIYCWLQPZXVGJD", "") 

refs = {}
comps["A"] = refs["A"] = Component("A", "EJMZALYXVBWFCRQUONTSPIKHGD", "")
comps["B"] = refs["B"] = Component("B", "YRUHQSLDPXNGOKMIEBFZCWVJAT", "")
comps["C"] = refs["C"] = Component("C", "FVPJIAOYEDRZXWGCTKUQSBNMHL", "")
comps["b"] = refs["b"] = Component("b", "ENKQAUYWJICOPBLMDXZVFTHRGS", "")
comps["c"] = refs["c"] = Component("c", "RDOBJNTKVEHMLFCWZAXGYIPSUQ", "")

kbd = {}
comps[""] = kbd[""] = Component("", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "")


def component(name):
    if name in comps.keys():
        return comps[name]
    else:
        # TBD - Generate wiring for plugboard <<<
        comps[name] = Component(name,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","")



class EnigmaConfig(object):

    @property
    def components(self):
        return self._components

    @property
    def positions(self):
        return self._positions

    @property
    def rings(self):
        return self._rings

    @property
    def stages(self):
        return self._stages

    def __init__(self, rotors, windows, plugs, rings):

        # TBD - Assertions for validation <<<

        comps = list(reversed((rotors+'-'+plugs).split('-')))
        winds = list(reversed([numA0(c) for c in "A"+windows+"A"]))
        rngs = list(reversed([int(x) for x in ("01."+rings+ ".01").split('.')]))

        self._components = comps
        self._positions = map(lambda w, r: ((w - r + 1) % 26) + 1, winds, rngs)
        self._rings = rngs
        self._stages = range(0,len(self._components))

    def _window_letter(self, st):
        return chrA0((self._positions[st] + self._rings[st] - 2) % 26)

    def windows(self):
        return ''.join(list(reversed([self._window_letter(st) for st in self._stages][1:-1])))

    # TBD - Decide on best strategy for iteration and on whether EnigmaConfig should be mutable (or step returns new) <<<
    def step(self):

        def is_turn(st):
            return self._window_letter(st) in component(self.components[st]).turnovers

        def di(st):
            if st == 0: return 0
            elif st > 3: return 0
            elif st == 1: return 1
            elif st == 2 and is_turn(2): return 1
            elif is_turn(st-1): return 1
            else: return 0

        self._positions = [((self._positions[st] + di(st) - 1) % 26) + 1 for st in self.stages]
        return self
