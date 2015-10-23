#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)
""" Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run "test" in PyCharm.
"""

import cProfile
#
# import euler
# cProfile.run('euler.euler046()')

#import sys
#for p in sys.path:
#    print p

import enigma

print(enigma.component(u'UX.MI'))
print(enigma.component(u'I'))

# Component rotation
assert "EKMFLGDQVZNTOWYHXUSPAIBRCJ" == enigma._comps["I"].mapping(1, enigma.FWD)
assert "QGCLFMUKTWZDNJYVOESIBPRAHX" == enigma._comps["II"].mapping(-1, enigma.FWD)
assert "CEGIKBOQSWUYMXDHVFZJLTRPNA"== enigma._comps["III"].mapping(2, enigma.FWD)
assert "PZEHVRYSCMDBTXLUKAOQIWJNGF" == enigma._comps["IV"].mapping(-2, enigma.FWD)

assert "RVHKXCSFBUMPJWNEGZYDIQOTLA" == enigma._comps["VIII"].mapping(11, enigma.REV)
assert "XZVROSMPJIWNGLEHUDFYQCKATB" == enigma._comps["B"].mapping(-12, enigma.REV)
assert "DUEACLXWRVPFZTSKYIONBJHGQM" == enigma._comps["C"].mapping(17, enigma.REV)
assert "MTPRJAYQKZLHUGFNWOCIXBVESD" == enigma._comps["V"].mapping(-8, enigma.REV)

assert "c-γ-I-VIII-III UYZO UX.MI 03.22.04.09" == unicode(enigma.EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09"))
assert "b-β-I-II-III AAAA UX.LU.QW.MI 01.11.14.04" == unicode(enigma.EnigmaConfig.config_enigma( "b-β-I-II-III", "AAAA", "UX.LU.QW.MI", "01.11.14.04"))

# EnigmaConfig.config_enigma stepping
cfg = enigma.EnigmaConfig.config_enigma("B-III-VI-VII", "EZU", "", "14.22.11")
assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ["EZU","FAV","FAW","FAX","FAY","FAZ","FBA","FBB","FBC","FBD","FBE","FBF","FBG","FBH","FBI","FBJ","FBK","FBL","FBM","FCN","FCO","FCP","FCQ","FCR","FCS","FCT","FCU","FCV","FCW","FCX","FCY","FCZ","FDA","FDB","FDC","FDD","FDE","FDF","FDG","FDH","FDI","FDJ","FDK","FDL","FDM","FEN","FEO","FEP","FEQ","FER","FES","FET","FEU","FEV","FEW","FEX","FEY","FEZ","FFA","FFB","FFC","FFD","FFE","FFF","FFG","FFH","FFI","FFJ","FFK","FFL","FFM","FGN","FGO","FGP","FGQ","FGR","FGS","FGT","FGU","FGV","FGW","FGX","FGY","FGZ","FHA","FHB","FHC","FHD","FHE","FHF","FHG","FHH","FHI","FHJ","FHK","FHL","FHM","FIN","FIO","FIP"]
cfg = enigma.EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ["UYZO","UZAP","UZAQ","UZAR","UZAS","UZAT","UZAU","UZAV","UZBW","UZBX","UZBY","UZBZ","UZBA","UZBB","UZBC","UZBD","UZBE","UZBF","UZBG","UZBH","UZBI","UZBJ","UZBK","UZBL","UZBM","UZBN","UZBO","UZBP","UZBQ","UZBR","UZBS","UZBT","UZBU","UZBV","UZCW","UZCX","UZCY","UZCZ","UZCA","UZCB","UZCC","UZCD","UZCE","UZCF","UZCG","UZCH","UZCI","UZCJ","UZCK","UZCL","UZCM","UZCN","UZCO","UZCP","UZCQ","UZCR","UZCS","UZCT","UZCU","UZCV","UZDW","UZDX","UZDY","UZDZ","UZDA","UZDB","UZDC","UZDD","UZDE","UZDF","UZDG","UZDH","UZDI","UZDJ","UZDK","UZDL","UZDM","UZDN","UZDO","UZDP","UZDQ","UZDR","UZDS","UZDT","UZDU","UZDV","UZEW","UZEX","UZEY","UZEZ","UZEA","UZEB","UZEC","UZED","UZEE","UZEF","UZEG","UZEH","UZEI","UZEJ"]
cfg = enigma.EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LEZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ["LEZO","LFAP","LFAQ","LFAR","LFAS","LFAT","LFAU","LFAV","LFAW","LFAX","LFAY","LFAZ","LFAA","LFAB","LFAC","LFAD","LFAE","LFBF","LFBG","LFBH","LFBI","LFBJ","LFBK","LFBL","LFBM","LFBN","LFBO","LFBP","LFBQ","LFBR","LFBS","LFBT","LFBU","LFBV","LFBW","LFBX","LFBY","LFBZ","LFBA","LFBB","LFBC","LFBD","LFBE","LFCF","LFCG","LFCH","LFCI","LFCJ","LFCK","LFCL","LFCM","LFCN","LFCO","LFCP","LFCQ","LFCR","LFCS","LFCT","LFCU","LFCV","LFCW","LFCX","LFCY","LFCZ","LFCA","LFCB","LFCC","LFCD","LFCE","LFDF","LFDG","LFDH","LFDI","LFDJ","LFDK","LFDL","LFDM","LFDN","LFDO","LFDP","LFDQ","LFDR","LFDS","LFDT","LFDU","LFDV","LFDW","LFDX","LFDY","LFDZ","LFDA","LFDB","LFDC","LFDD","LFDE","LFEF","LFEG","LFEH","LFEI","LFEJ"]


cfg = enigma.EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAQ", "", "03.17.04.11")
assert cfg.stage_mapping_list() == ["ABCDEFGHIJKLMNOPQRSTUVWXYZ","LORVFBQNGWKATHJSZPIYUDXEMC","BJYINTKWOARFEMVSGCUDPHZQLX","ILHXUBZQPNVGKMCRTEJFADOYSW","YDSKZPTNCHGQOMXAUWJFBRELVI","ENKQAUYWJICOPBLMDXZVFTHRGS","PUIBWTKJZSDXNHMFLVCGQYROAE","UFOVRTLCASMBNJWIHPYQEKZDXG","JARTMLQVDBGYNEIUXKPFSOHZCW","LFZVXEINSOKAYHBRGCPMUDJWTQ","ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
assert cfg.enigma_mapping() == "LOYWFEZPNVSAXIBHTUKQRJDMCG"
assert cfg.enigma_encoding("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == "LGWLXXIYXCIEACMGMJECRORTHO"
cfg = enigma.EnigmaConfig.config_enigma("c-γ-I-III-II", "MAMA", "", "12.01.16.05")
assert cfg.stage_mapping_list() == ["ABCDEFGHIJKLMNOPQRSTUVWXYZ","JZSIENHOWMVYBFPLAXQGUKDRTC","VTREGIKMOFSUWAYCQBHLZJDNPX","EKMFLGDQVZNTOWYHXUSPAIBRCJ","RNJZMTDQGLASHXBVKPOYWUFICE","RDOBJNTKVEHMLFCWZAXGYIPSUQ","KOYGZWIMXCQJEBSRHALFVPUNTD","UWYGADFPVZBECKMTHXSLRINQOJ","NRPWDJESFVGTHXIYQCKBLAMZOU","QMZWENTGDAVPJFHOSXCYUKIRLB","ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
assert cfg.enigma_mapping() == "GZOVLUAKQRHESYCXIJMWFDTPNB"
assert cfg.enigma_encoding("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == "MLMFRBAWUVQBREFCGTQOLXYJHP"
cfg = enigma.EnigmaConfig.config_enigma("c-γ-V-VIII-III", "MFIQ", "ML.IO.QW.AG.DS.ZR", "13.19.02.16")
assert cfg.stage_mapping_list() == ["GBCSEFAHOJKMLNIPWZDTUVQXYR","CEGIKBOQSWUYMXDHVFZJLTRPNA","HVUCLIWSKTFXPGBNRZOYDJAMEQ","UYKNJZWDBSRPXIMOETVGLHCFQA","FSOKANUERHMBTIYCWLQPZXVGJD","RDOBJNTKVEHMLFCWZAXGYIPSUQ","ELPZHAXJNYDRKFCTSIBMGWQVOU","ZIWHQXTVNECUODPLYKJRASGMBF","WODUYKNAFVIEXPSMZQHJCBGLTR","ZFAOBRCPDTEUMYGXHWIVKQJNLS","GBCSEFAHOJKMLNIPWZDTUVQXYR"]
assert cfg.enigma_mapping() == "FCBXGAEVSWYTRONZUMILQHJDKP"
assert cfg.enigma_encoding("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ") == "YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE"

cfg = enigma.EnigmaConfig.config_enigma("c-β-V-VI-VIII", enigma.EnigmaConfig.config_enigma("c-β-V-VI-VIII", "NAEM", "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12").enigma_encoding("QEOB"), "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12")
assert cfg.enigma_encoding("KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP") == "LANOTCTOUARBBFPMHPHGCZXTDYGAHGUFXGEWKBLKGJWLQXXTGPJJAVTOCKZFSLPPQIHZFXOEBWIIEKFZLCLOAQJULJOYHSSMBBGWHZANVOIIPYRBRTDJQDJJOQKCXWDNBBTYVXLYTAPGVEATXSONPNYNQFUDBBHHVWEPYEYDOHNLXKZDNWRHDUWUJUMWWVIIWZXIVIUQDRHYMNCYEFUAPNHOTKHKGDNPSAKNUAGHJZSMJBMHVTREQEDGXHLZWIFUSKDQVELNMIMITHBHDBWVHDFYHJOQIHORTDJDBWXEMEAYXGYQXOHFDMYUXXNOJAZRSGHPLWMLRECWWUTLRTTVLBHYOORGLGOWUXNXHMHYFAACQEKTHSJW"
assert cfg.enigma_encoding("KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP") == "LANOTCTOUARBBFPMHPHGCZXTDYGAHGUFXGEWKBLKGJWLQXXTGPJJAVTOCKZFSLPPQIHZFXOEBWIIEKFZLCLOAQJULJOYHSSMBBGWHZANVOIIPYRBRTDJQDJJOQKCXWDNBBTYVXLYTAPGVEATXSONPNYNQFUDBBHHVWEPYEYDOHNLXKZDNWRHDUWUJUMWWVIIWZXIVIUQDRHYMNCYEFUAPNHOTKHKGDNPSAKNUAGHJZSMJBMHVTREQEDGXHLZWIFUSKDQVELNMIMITHBHDBWVHDFYHJOQIHORTDJDBWXEMEAYXGYQXOHFDMYUXXNOJAZRSGHPLWMLRECWWUTLRTTVLBHYOORGLGOWUXNXHMHYFAACQEKTHSJW"

ec = enigma.EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
print(ec.components)
print(ec.rings)
print(ec.positions)
print(ec.stages)
# print(ec._window_letter(1))
# print(ec._window_letter(2))
# print(ec._window_letter(3))
# st = 2
# print(ec._window_letter(st))
# print(enigma.component(ec.components[st]).turnovers)
# print(ec._window_letter(st) in enigma.component(ec.components[st]).turnovers)
print(ec.windows())
print(ec.step().windows())
print(ec.step().step().windows())
print(ec.windows())

print(enigma._comps["II"].mapping(7, enigma.FWD))
#print([str(ec.windows())] + [str(ec.step().windows()) for _ in xrange (99)])
cfg = enigma.EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAQ", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print(cfg.positions)
print(cfg)
for m in cfg.stage_mapping_list():
    print(m)

cfg = enigma.EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
print(cfg)

print([str(ec.windows()) for ec in cfg.stepped_configs(0)])
print([str(ec.windows()) for ec in cfg.stepped_configs(99)])


print(enigma._comps["I"].mapping(1, enigma.FWD))
print(enigma._comps["II"].mapping(-1, enigma.FWD))
print(enigma._comps["III"].mapping(2, enigma.FWD))
print(enigma._comps["IV"].mapping(-2, enigma.FWD))

print(enigma._comps["VIII"].mapping(11, enigma.REV))
print(enigma._comps["B"].mapping(-12, enigma.REV))
print(enigma._comps["C"].mapping(17, enigma.REV))
print(enigma._comps["V"].mapping(-8, enigma.REV))


print([str(ec[1].windows()) for ec in zip("ABCDEFG",cfg.stepped_configs())])
cfg = enigma.EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LEZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print([ec[1].windows() for ec in zip([1, 2, 3],cfg.stepped_configs())])
cfg = enigma.EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LEZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print([ec[1].windows() for ec in zip([1, 2, 3],[i for i in cfg.stepped_configs(3)])])

# cfg = enigma.EnigmaConfig.config_enigma("c-β-V-VI-VIII", enigma.EnigmaConfig.config_enigma("c-β-V-VI-VIII", "NAEM", "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12").enigma_encoding("QEOB"), "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12")
# cProfile.run('cfg.enigma_encoding("KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP")')
# cProfile.run('[str(ec.windows()) for ec in cfg.stepped_configs(10000)]')

# print(enigma.num_A0(' '))
# for let in enigma.LETTERS:
#     print(enigma.num_A0(let))
# print(ec.windows())
# for i in range(99):
#     ec.step()
#     print(ec.windows())
