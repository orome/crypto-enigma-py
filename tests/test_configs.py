#!/usr/bin/env python
# encoding: utf8
#from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''

import pytest

from crypto_enigma.machine import *
from crypto_enigma.exceptions import *


# Comparing output with output generated from Haskell version
# USE - Replace greek letters in Haskell-generated output

def test_config_constructor():
    with pytest.raises(EnigmaValueError) as e:
        cfg = EnigmaConfig.config_enigma('B-XX-VI-VII', 'AZU', '', '14.22.11')
    assert "Bad configuration - Invalid rotor name, XX" in str(e)
    with pytest.raises(EnigmaValueError) as e:
        cfg = EnigmaConfig.config_enigma('B-III-VI-VII', 'aZU', '', '14.22.11')
    assert "Bad configuration: window letter, a" in str(e)
    with pytest.raises(EnigmaValueError) as e:
        cfg = EnigmaConfig.config_enigma('B-III-VI-VII', 'AZU', '', '99.22.11')
    assert "Bad configuration: invalid ring position number, 99" in str(e)
    with pytest.raises(EnigmaValueError) as e:
        cfg = EnigmaConfig.config_enigma('B-III-VI-VII', 'AU', '', '14.22.11')
    assert "Bad configuration: number rotors (3), rings (3), and window letters (2) must match" in str(e)

    with pytest.raises(EnigmaValueError) as e:
        cfg = EnigmaConfig.config_enigma_from_string('B-III-VI-VII AU 14.22.11')
    assert "Bad string - ['B-III-VI-VII', 'AU', '14.22.11'] should have 4 elements" in str(e)


def test_config_stepping():
    # EnigmaConfig stepping
    cfg = EnigmaConfig.config_enigma('B-III-VI-VII', 'EZU', '', '14.22.11')
    assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ['EZU','FAV','FAW','FAX','FAY','FAZ','FBA','FBB','FBC','FBD','FBE','FBF','FBG','FBH','FBI','FBJ','FBK','FBL','FBM','FCN','FCO','FCP','FCQ','FCR','FCS','FCT','FCU','FCV','FCW','FCX','FCY','FCZ','FDA','FDB','FDC','FDD','FDE','FDF','FDG','FDH','FDI','FDJ','FDK','FDL','FDM','FEN','FEO','FEP','FEQ','FER','FES','FET','FEU','FEV','FEW','FEX','FEY','FEZ','FFA','FFB','FFC','FFD','FFE','FFF','FFG','FFH','FFI','FFJ','FFK','FFL','FFM','FGN','FGO','FGP','FGQ','FGR','FGS','FGT','FGU','FGV','FGW','FGX','FGY','FGZ','FHA','FHB','FHC','FHD','FHE','FHF','FHG','FHH','FHI','FHJ','FHK','FHL','FHM','FIN','FIO','FIP']
    assert [cfg.rings == cfg.rings for ec in cfg.stepped_configs(99)]
    assert [cfg.components == cfg.components for ec in cfg.stepped_configs(99)]
    cfg = EnigmaConfig.config_enigma('c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09')
    assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ['UYZO','UZAP','UZAQ','UZAR','UZAS','UZAT','UZAU','UZAV','UZBW','UZBX','UZBY','UZBZ','UZBA','UZBB','UZBC','UZBD','UZBE','UZBF','UZBG','UZBH','UZBI','UZBJ','UZBK','UZBL','UZBM','UZBN','UZBO','UZBP','UZBQ','UZBR','UZBS','UZBT','UZBU','UZBV','UZCW','UZCX','UZCY','UZCZ','UZCA','UZCB','UZCC','UZCD','UZCE','UZCF','UZCG','UZCH','UZCI','UZCJ','UZCK','UZCL','UZCM','UZCN','UZCO','UZCP','UZCQ','UZCR','UZCS','UZCT','UZCU','UZCV','UZDW','UZDX','UZDY','UZDZ','UZDA','UZDB','UZDC','UZDD','UZDE','UZDF','UZDG','UZDH','UZDI','UZDJ','UZDK','UZDL','UZDM','UZDN','UZDO','UZDP','UZDQ','UZDR','UZDS','UZDT','UZDU','UZDV','UZEW','UZEX','UZEY','UZEZ','UZEA','UZEB','UZEC','UZED','UZEE','UZEF','UZEG','UZEH','UZEI','UZEJ']
    assert [cfg.rings == cfg.rings for ec in cfg.stepped_configs(99)]
    assert [cfg.components == cfg.components for ec in cfg.stepped_configs(99)]
    cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LEZO', 'UX.MO.KZ.AY.EF.PL', '03.17.04.11')
    assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ['LEZO','LFAP','LFAQ','LFAR','LFAS','LFAT','LFAU','LFAV','LFAW','LFAX','LFAY','LFAZ','LFAA','LFAB','LFAC','LFAD','LFAE','LFBF','LFBG','LFBH','LFBI','LFBJ','LFBK','LFBL','LFBM','LFBN','LFBO','LFBP','LFBQ','LFBR','LFBS','LFBT','LFBU','LFBV','LFBW','LFBX','LFBY','LFBZ','LFBA','LFBB','LFBC','LFBD','LFBE','LFCF','LFCG','LFCH','LFCI','LFCJ','LFCK','LFCL','LFCM','LFCN','LFCO','LFCP','LFCQ','LFCR','LFCS','LFCT','LFCU','LFCV','LFCW','LFCX','LFCY','LFCZ','LFCA','LFCB','LFCC','LFCD','LFCE','LFDF','LFDG','LFDH','LFDI','LFDJ','LFDK','LFDL','LFDM','LFDN','LFDO','LFDP','LFDQ','LFDR','LFDS','LFDT','LFDU','LFDV','LFDW','LFDX','LFDY','LFDZ','LFDA','LFDB','LFDC','LFDD','LFDE','LFEF','LFEG','LFEH','LFEI','LFEJ']
    assert [cfg.rings == cfg.rings for ec in cfg.stepped_configs(99)]
    assert [cfg.components == cfg.components for ec in cfg.stepped_configs(99)]


def test_config_mapping():
    # EnigmaConfig mappings
    cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
    assert cfg.stage_mapping_list() == ['ABCDEFGHIJKLMNOPQRSTUVWXYZ','LORVFBQNGWKATHJSZPIYUDXEMC','BJYINTKWOARFEMVSGCUDPHZQLX','ILHXUBZQPNVGKMCRTEJFADOYSW','YDSKZPTNCHGQOMXAUWJFBRELVI','ENKQAUYWJICOPBLMDXZVFTHRGS','PUIBWTKJZSDXNHMFLVCGQYROAE','UFOVRTLCASMBNJWIHPYQEKZDXG','JARTMLQVDBGYNEIUXKPFSOHZCW','LFZVXEINSOKAYHBRGCPMUDJWTQ','ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    assert cfg.enigma_mapping_list() == ['ABCDEFGHIJKLMNOPQRSTUVWXYZ','LORVFBQNGWKATHJSZPIYUDXEMC','FVCHTJGMKZRBDWAUXSOLPIQNEY','BDHQFNZKVWELXOIAYJCGRPTMUS','DKNUPMIGREZQLXCYVHSTWAFOBJ','QCBFMPJYXASDORKGTWZVHEULNI','LIUTNFSAOPCBMVDKGREYJWQXHZ','BAEQJTYUWIOFNKVMLPRXSZHDCG','AJMXBFCSHDILEGONYUKZPWVTRQ','LOYWFEZPNVSAXIBHTUKQRJDMCG','LOYWFEZPNVSAXIBHTUKQRJDMCG']
    assert cfg.enigma_mapping() == 'LOYWFEZPNVSAXIBHTUKQRJDMCG'
    cfg = EnigmaConfig.config_enigma('b-γ-IV-III-II', 'XLMA', 'LM.OR.TK.SC.FZ.QE', '11.01.06.01')
    assert cfg.stage_mapping_list() == ['ABSDQZGHIJTMLNRPEOCKUVWXYF','AJDKSIRUXBLHWTMCQGZNPYFVOE','IKMQOSGRXBPZTDFNLJHUWYACEV','XGWMACUIVZSRBLQTHDKEOYPNFJ','VLPJYDCMKITWQSFBXNAHREUZOG','ENKQAUYWJICOPBLMDXZVFTHRGS','SPGFVOZTJDIBHRYCMUNKWALQEX','EMFRTYBQHZSNDXUWOLKPGICAVJ','WJXNYOGSARBQCPEKDHFMTZUIVL','AJPCZWRLFBDKOTYUQGENHXMIVS','ABSDQZGHIJTMLNRPEOCKUVWXYF']
    assert cfg.enigma_mapping_list() == ['ABSDQZGHIJTMLNRPEOCKUVWXYF','AJZKQERUXBNWHTGCSMDLPYFVOI','IBVPLOJWCKDARUGMHTQZNESYFX','VGYTRQZPWSMXDOUBIEHJLAKFCN','ECOHNXGBUAQZJFRLKYMIWVTDPS','AKLWBRYNFEDSIUXOCGPJHTVQMZ','SIBLPUEROVFNJWQYGZCDTKAMHX','KHMNWGTLUIYXZCOVBJFRPSEDQA','BSCPUGMQTAVILXEZJROHKFYNDW','JEPUHROQNAXFKIZSBGYLDWVTCM','JQPUHORENAXZTIFCBGYMDWVKSL']
    assert cfg.enigma_mapping() == 'JQPUHORENAXZTIFCBGYMDWVKSL'
    cfg = EnigmaConfig.config_enigma('c-γ-V-VIII-III', 'MFIQ', 'ML.IO.QW.AG.DS.ZR', '13.19.02.16')
    assert cfg.stage_mapping_list() == ['GBCSEFAHOJKMLNIPWZDTUVQXYR','CEGIKBOQSWUYMXDHVFZJLTRPNA','HVUCLIWSKTFXPGBNRZOYDJAMEQ','UYKNJZWDBSRPXIMOETVGLHCFQA','FSOKANUERHMBTIYCWLQPZXVGJD','RDOBJNTKVEHMLFCWZAXGYIPSUQ','ELPZHAXJNYDRKFCTSIBMGWQVOU','ZIWHQXTVNECUODPLYKJRASGMBF','WODUYKNAFVIEXPSMZQHJCBGLTR','ZFAOBRCPDTEUMYGXHWIVKQJNLS','GBCSEFAHOJKMLNIPWZDTUVQXYR']
    assert cfg.enigma_mapping_list() == ['GBCSEFAHOJKMLNIPWZDTUVQXYR','OEGZKBCQDWUMYXSHRAIJLTVPNF','BLWQFVURCADPEMOSZHKTXYJNGI','YPCEZHLTKUNOJXMVADRGFQSIWB','JCOADEBPMZIYHGTXFKLUNWQRVS','EOCRBJDWLQVUKTGSNHMYFPZAIX','HCPILYZQRSWGDMXBFJKOATUENV','VWLNUBFYKJGTHOMIXECPZRAQDS','BGEPCOKTIVNJASXFLYDMRQWZUH','FCBXAGEVDQYTZINRULOMWHJSKP','FCBXGAEVSWYTRONZUMILQHJDKP']
    assert cfg.enigma_mapping() == 'FCBXGAEVSWYTRONZUMILQHJDKP'
