#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''

from crypto_enigma.machine import *


# Comparing output with output generated from Haskell version
# USE - Replace greek letters in Haskell-generated output


def test_config_encoding_simple():
    # EnigmaConfig mappings and simple encoding
    cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
    assert cfg.enigma_encoding('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 'LGWLXXIYXCIEACMGMJECRORTHO'
    assert cfg.enigma_encoding(cfg.enigma_encoding('GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE')) == 'GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE'
    cfg = EnigmaConfig.config_enigma('b-γ-IV-III-II', 'XLMA', 'LM.OR.TK.SC.FZ.QE', '11.01.06.01')
    assert cfg.enigma_encoding('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 'HKNOIVPIQQDIUEPANGFXOOOCWH'
    assert cfg.enigma_encoding(cfg.enigma_encoding('GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE')) == 'GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE'
    assert cfg.enigma_encoding('                ') == ''
    assert cfg.enigma_encoding(' ') == ''
    assert cfg.enigma_encoding('') == ''
    cfg = EnigmaConfig.config_enigma('c-γ-V-VIII-III', 'MFIQ', 'ML.IO.QW.AG.DS.ZR', '13.19.02.16')
    assert cfg.enigma_encoding('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ') == 'YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE'
    assert cfg.enigma_encoding(cfg.enigma_encoding('HLERHALTENXXJANSTERLEDESBISHERIGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE')) == 'HLERHALTENXXJANSTERLEDESBISHERIGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE'
    assert cfg.enigma_encoding('aBCDEfGHIJKLMNOPQRSTUVWXYZABCDEfghIJKLMNOPQRStuvwXYZ') == 'YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE'
    assert cfg.enigma_encoding('aBCD Ef GHIJK LMNOPQRS TUVWXYZA BCDEfghIJK LMNOPQ RStuvwXYZ') == 'YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE'
    assert cfg.enigma_encoding('aBCD Ef& GHIJK LMNOPQRS TUV|WXYZA BCDEfghIJK LM@NOPQ RStuvwXYZ') == 'YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE'
    assert cfg.enigma_encoding('βaBCD Ef& GHIJK LMNOγPQRS TUV|WXYZA BβCγDEfghIJK LM@NOPQ RStuγvwXYZβ') == 'YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE'
    assert cfg.enigma_encoding('βaBCD Ef& GHI<K LMNOγPQRS TUV|W!YZA BβCγDEfghIJK LM@NOPQ RStuγvwX,Zβ') == 'YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE'


def test_encoding_stepped_start():
    cfg = EnigmaConfig.config_enigma('b-γ-IV-VIII-V', 'JOAW', 'UE.BN.ZA.PD', '04.11.04.16')
    msg = "FJUGFHFHIRVBNAFOQIWUFHFBABJSIQHFFJDSISQNSBFJKDIFFDHDHAJSJSJS"
    for i in range(len(msg)):
        assert list(cfg.stepped_configs(i))[-1].enigma_encoding(msg[i:]) == cfg.enigma_encoding(msg)[i:]


def test_config_encoding_historical():
    # EnigmaConfig historical message encoding
    cfg = EnigmaConfig.config_enigma('c-β-V-VI-VIII', EnigmaConfig.config_enigma('c-β-V-VI-VIII', 'NAEM', 'AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW', '05.16.05.12').enigma_encoding('QEOB'), 'AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW', '05.16.05.12')
    enc = 'LANOTCTOUARBBFPMHPHGCZXTDYGAHGUFXGEWKBLKGJWLQXXTGPJJAVTOCKZFSLPPQIHZFXOEBWIIEKFZLCLOAQJULJOYHSSMBBGWHZANVOIIPYRBRTDJQDJJOQKCXWDNBBTYVXLYTAPGVEATXSONPNYNQFUDBBHHVWEPYEYDOHNLXKZDNWRHDUWUJUMWWVIIWZXIVIUQDRHYMNCYEFUAPNHOTKHKGDNPSAKNUAGHJZSMJBMHVTREQEDGXHLZWIFUSKDQVELNMIMITHBHDBWVHDFYHJOQIHORTDJDBWXEMEAYXGYQXOHFDMYUXXNOJAZRSGHPLWMLRECWWUTLRTTVLBHYOORGLGOWUXNXHMHYFAACQEKTHSJW'
    msg = 'KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP'
    assert cfg.enigma_encoding(msg) == enc
    assert cfg.enigma_encoding(cfg.enigma_encoding(msg)) == EnigmaConfig.make_message(msg)
    assert cfg.enigma_encoding(cfg.enigma_encoding(msg)) == msg
    msg = 'KRKR ALLE XX FOLGENDES IST SOFORT BEKANNTZUGEBEN XX ICH HABE FOLGELNBE BEFEHL ERHALTEN XX J ANSTERLE DES BISHERIGXN REICHSMARSCHALLS J GOERING J SETZT DER FUEHRER SIE Y HVRR GRZSSADMIRAL Y ALS SEINEN NACHFOLGER EIN X SCHRIFTLSCHE VOLLMACHT UNTERWEGS X ABSOFORT SOLLEN SIE SAEMTLICHE MASSNAHMEN VERFUEGEN Y DIE SICH AUS DER GEGENWAERTIGEN LAGE ERGEBEN X GEZ X REICHSLEITEI KK TULPE KK J BORMANN J XX OB.D.MMM DURNH FKST.KOM.ADM.UUU BOOIE.KP'
    assert cfg.enigma_encoding(msg) == enc
    assert cfg.enigma_encoding(cfg.enigma_encoding(msg)) == EnigmaConfig.make_message(msg)
