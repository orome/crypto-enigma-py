#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''

import cProfile
import pytest

#from enigma.machine import *
from crypto_enigma import *


def print_header(level, label='', mark=None):
    if mark is None:
        mark = {1: '==', 2: '--', 3: '- ', 4: ' - '}[level]

    rule = (mark * 40)[:((81-(len(label)+2))//2)]
    #rule = rule + mark[0] if rule[-1] !=  mark[0] else rule
    header_string = '{rule_l} {text} {rule_r}'.format(rule_l=rule, rule_r=rule[::-1], text=label)[:80]

    print('{blanks}{fmt_start}{header_string}{fmt_end}'.format(blanks='\n' if level is not 1 else '\n\n',
                                                               fmt_start='\033[1m' if level is 1 else '',
                                                               fmt_end='\033[0;0m' if level is 1 else '',
                                                               header_string=header_string))


test_result = pytest.main(b"--cache-clear -v --color=yes --exitfirst --showlocals --durations=5")
if test_result != 0:
    exit(test_result)


print_header(1, 'eyeball checks')
print_header(2, 'components')
print_header(3, 'instantiation')
print(component(u'UX.MI'))
print(component(u'I'))

print_header(3, 'mapping rotation')
print(component('I').mapping(1, FWD))
print(component('II').mapping(-1, FWD))
print(component('III').mapping(2, FWD))
print(component('IV').mapping(-2, FWD))

print(component('VIII').mapping(11, REV))
print(component('B').mapping(-12, REV))
print(component('C').mapping(17, REV))
print(component('V').mapping(-8, REV))

print_header(2, 'configs')
print_header(3, 'instantiation')

ec = EnigmaConfig.config_enigma('c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09')
print(ec.components)
print(ec.rings)
print(ec.positions)
print(ec.stages)
# print(ec._window_letter(1))
# print(ec._window_letter(2))
# print(ec._window_letter(3))
# st = 2
# print(ec._window_letter(st))
# print(component(ec.components[st]).turnovers)
# print(ec._window_letter(st) in component(ec.components[st]).turnovers)
print(ec.windows())
print(ec.step().windows())
print(ec.step().step().windows())
print(ec.windows())


print_header(3, 'stage mappings')
#print([str(ec.windows())] + [str(ec.step().windows()) for _ in xrange (99)])
cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', 'UX.MO.KZ.AY.EF.PL', '03.17.04.11')
# print(cfg.positions)
# print(cfg)
for m in cfg.stage_mapping_list():
    print(m)

print_header(3, 'stepping')

cfg = EnigmaConfig.config_enigma('c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09')
print(cfg)
print([str(ec.windows()) for ec in cfg.stepped_configs(0)])
print([str(ec.windows()) for ec in cfg.stepped_configs(99)])



print([str(ec[1].windows()) for ec in zip('ABCDEFG',cfg.stepped_configs())])
cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LEZO', 'UX.MO.KZ.AY.EF.PL', '03.17.04.11')
print([ec[1].windows() for ec in zip([1, 2, 3],cfg.stepped_configs())])
cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LEZO', 'UX.MO.KZ.AY.EF.PL', '03.17.04.11')
print([ec[1].windows() for ec in zip([1, 2, 3],[i for i in cfg.stepped_configs(3)])])

print_header(2, 'display')

print_header(3, 'marked mappings')
print(EnigmaConfig._marked_mapping(LETTERS, 3))
print(EnigmaConfig._marked_mapping(LETTERS, 0))
print(EnigmaConfig._marked_mapping(LETTERS, 10))
print(EnigmaConfig._marked_mapping(LETTERS, 25))
print(EnigmaConfig._marked_mapping(LETTERS, 25, lambda c: '[' + c + ']'))

# print(len(LETTERS))
# print(len(EnigmaConfig._marked_mapping(LETTERS, 3)))
# print(len(EnigmaConfig._marked_mapping(LETTERS, 25, lambda c: '[' + c + ']')))
print_header(3, 'config strings')
print_header(4, unicode(cfg))
print(cfg._config_string('A'))
print(cfg._config_string(' '))
print(cfg._config_string('Z'))
print(cfg._config_string('K'))

print_header(3, 'config strings internal')
cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', 'UX.MO.KZ.AY.EF.PL', '03.17.04.11')
print_header(4, "{0} and '{1}'".format(cfg, 'Q'))
print(cfg._config_string_internal('Q'))
print_header(4, "{0} and '{1}'".format(cfg, ' '))
print(cfg._config_string_internal(' '))

#print(cfg.enigma_mapping_list())
print_header(3, 'operation')
print_header(4, "{0} using '{1}'".format(cfg, '[..]'))
cfg.print_operation('ABCDE', lambda c: '[' + c + ']')

print_header(3, 'operation internal')
print_header(4, "{0} using '{1}'".format(cfg, '(..)'))
cfg.print_operation_internal('ABCDE', lambda c: '(' + c + ')')
#print(EnigmaConfig._marked_mapping(LETTERS, 2, lambda c: c + '[' + c + ']'))
#print(cfg.config_string_internal('G', lambda c: '[' + c + ']'))

print_header(3, 'historical encoding')
print_header(4, 'p-1030681')
cfg = EnigmaConfig.config_enigma('c-β-V-VI-VIII', EnigmaConfig.config_enigma('c-β-V-VI-VIII', 'NAEM', 'AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW', '05.16.05.12').enigma_encoding('QEOB'), 'AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW', '05.16.05.12')
cfg.print_encoding("KRKR ALLE XX FOLGENDES IST SOFORT BEKANNTZUGEBEN XX ICH HABE FOLGELNBE BEFEHL ERHALTEN XX J ANSTERLE DES BISHERIGXN REICHSMARSCHALLS J GOERING J SETZT DER FUEHRER SIE Y HVRR GRZSSADMIRAL Y ALS SEINEN NACHFOLGER EIN X SCHRIFTLSCHE VOLLMACHT UNTERWEGS X ABSOFORT SOLLEN SIE SAEMTLICHE MASSNAHMEN VERFUEGEN Y DIE SICH AUS DER GEGENWAERTIGEN LAGE ERGEBEN X GEZ X REICHSLEITEI KK TULPE KK J BORMANN J XX OB.D.MMM DURNH FKST.KOM.ADM.UUU BOOIE.KP")
# TBD - Assertion for this <<<

# print_header(1, 'profiling')
# cfg = EnigmaConfig.config_enigma('c-β-V-VI-VIII', EnigmaConfig.config_enigma('c-β-V-VI-VIII', 'NAEM', 'AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW', '05.16.05.12').enigma_encoding('QEOB'), 'AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW', '05.16.05.12')
# cProfile.run("cfg.enigma_encoding('KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP')")
# cProfile.run('[str(ec.windows()) for ec in cfg.stepped_configs(10000)]')


print_header(3, 'operation again')
cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', 'UX.MO.KZ.AY.EF.PL', '03.17.04.11')
print_header(4, "()")
cfg.print_operation()
print_header(4, "(message='ABC')")
cfg.print_operation(message='ABC')
print_header(4, "(message='ABC', format='windows')")
cfg.print_operation(message='ABC', format='windows')
print_header(4, "(message='ABC', format='internal')")
cfg.print_operation(message='ABC', format='internal')
print_header(4, "(message='ABC', steps=2)")
cfg.print_operation(message='ABC', steps=2)
print_header(4, "(message='ABC', steps=1)")
cfg.print_operation(message='ABC', steps=1)
print_header(4, "(message='ABC', steps=0)")
cfg.print_operation(message='ABC', steps=0)
print_header(4, "(message='ABC', steps=10)")
cfg.print_operation(message='ABC', steps=10)
print_header(4, "(message='', steps=10)")
cfg.print_operation(message='', steps=10)
print_header(4, "(steps=10)")
cfg.print_operation(steps=10)
print_header(4, "(message='ABC', steps=10, initial=False)")
cfg.print_operation(message='ABC', steps=10, initial=False)
print_header(4, "(message='ABC', steps=1, initial=False)")
cfg.print_operation(message='ABC', steps=1, initial=False)
print_header(4, "(message='ABC', steps=0, initial=False)")
cfg.print_operation(message='ABC', steps=0, initial=False)
print_header(4, "(message='', steps=0, initial=False)")
cfg.print_operation(message='', steps=0, initial=False)
print_header(4, "(message='', steps=10, initial=False)")
cfg.print_operation(message='', steps=10, initial=False)
print_header(4, "(steps=10, initial=False)")
cfg.print_operation(steps=10, initial=False)
print_header(4, "(steps=10, initial=False, overwrite=True)")
cfg.print_operation(steps=10, initial=False, overwrite=True)
print_header(4, "(message='ABCDEFGHIJKL', initial=False, overwrite=True, format='internal')")
cfg.print_operation(message='ABCDEFGHIJKL', initial=False, overwrite=True, format='internal')
print_header(4, "(message='ABCD EFGH IJK    L', steps=10, initial=False)")
cfg.print_operation(message='ABCD EFGH IJK    L', steps=10, initial=False)
print_header(4, "(message='ABCD EFGH IJK    L', initial=False)")
cfg.print_operation(message='ABCD EFGH IJK    L', initial=False)
# print(EnigmaConfig.postprocess("KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNB"))
# print(EnigmaConfig.postprocess("123456"))

# import sys, time
#
# for progress in range(0,101):
#     sys.stdout.write("Download progress: %d%% \r" % (progress) )
#     sys.stdout.flush()
#     time.sleep(0.2)
#     print ("")

# print(num_A0(' '))
# for let in LETTERS:
#     print(num_A0(let))
# print(ec.windows())
# for i in range(99):
#     ec.step()
#     print(ec.windows())



#
# import euler
# cProfile.run('euler.euler046()')

#import sys
#for p in sys.path:
#    print p

# TBD - Add function to format sections and pad with == or --, etc.
# TBD - Loop through keys here and in test