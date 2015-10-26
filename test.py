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

from enigma import *

# Comparing output with output generated from Haskell version
# USE - Replace greek letters in Haskell-generated output

# Component names
assert rotors == sorted(["I","II","III","IV","V","VI","VII","VIII",'β','γ'])
assert reflectors == sorted(["A","B","C","b","c"])

# Component rotation
assert "EKMFLGDQVZNTOWYHXUSPAIBRCJ" == component("I").mapping(1, FWD)
assert "QGCLFMUKTWZDNJYVOESIBPRAHX" == component("II").mapping(-1, FWD)
assert "CEGIKBOQSWUYMXDHVFZJLTRPNA"== component("III").mapping(2, FWD)
assert "PZEHVRYSCMDBTXLUKAOQIWJNGF" == component("IV").mapping(-2, FWD)

assert "RVHKXCSFBUMPJWNEGZYDIQOTLA" == component("VIII").mapping(11, REV)
assert "XZVROSMPJIWNGLEHUDFYQCKATB" == component("B").mapping(-12, REV)
assert "DUEACLXWRVPFZTSKYIONBJHGQM" == component("C").mapping(17, REV)
assert "MTPRJAYQKZLHUGFNWOCIXBVESD" == component("V").mapping(-8, REV)

assert "c-γ-I-VIII-III UYZO UX.MI 03.22.04.09" == unicode(EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09"))
assert "b-β-I-II-III AAAA UX.LU.QW.MI 01.11.14.04" == unicode(EnigmaConfig.config_enigma( "b-β-I-II-III", "AAAA", "UX.LU.QW.MI", "01.11.14.04"))

# EnigmaConfig stepping
cfg = EnigmaConfig.config_enigma("B-III-VI-VII", "EZU", "", "14.22.11")
assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ["EZU","FAV","FAW","FAX","FAY","FAZ","FBA","FBB","FBC","FBD","FBE","FBF","FBG","FBH","FBI","FBJ","FBK","FBL","FBM","FCN","FCO","FCP","FCQ","FCR","FCS","FCT","FCU","FCV","FCW","FCX","FCY","FCZ","FDA","FDB","FDC","FDD","FDE","FDF","FDG","FDH","FDI","FDJ","FDK","FDL","FDM","FEN","FEO","FEP","FEQ","FER","FES","FET","FEU","FEV","FEW","FEX","FEY","FEZ","FFA","FFB","FFC","FFD","FFE","FFF","FFG","FFH","FFI","FFJ","FFK","FFL","FFM","FGN","FGO","FGP","FGQ","FGR","FGS","FGT","FGU","FGV","FGW","FGX","FGY","FGZ","FHA","FHB","FHC","FHD","FHE","FHF","FHG","FHH","FHI","FHJ","FHK","FHL","FHM","FIN","FIO","FIP"]
assert [cfg.rings == cfg.rings for ec in cfg.stepped_configs(99)]
assert [cfg.components == cfg.components for ec in cfg.stepped_configs(99)]
cfg = EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ["UYZO","UZAP","UZAQ","UZAR","UZAS","UZAT","UZAU","UZAV","UZBW","UZBX","UZBY","UZBZ","UZBA","UZBB","UZBC","UZBD","UZBE","UZBF","UZBG","UZBH","UZBI","UZBJ","UZBK","UZBL","UZBM","UZBN","UZBO","UZBP","UZBQ","UZBR","UZBS","UZBT","UZBU","UZBV","UZCW","UZCX","UZCY","UZCZ","UZCA","UZCB","UZCC","UZCD","UZCE","UZCF","UZCG","UZCH","UZCI","UZCJ","UZCK","UZCL","UZCM","UZCN","UZCO","UZCP","UZCQ","UZCR","UZCS","UZCT","UZCU","UZCV","UZDW","UZDX","UZDY","UZDZ","UZDA","UZDB","UZDC","UZDD","UZDE","UZDF","UZDG","UZDH","UZDI","UZDJ","UZDK","UZDL","UZDM","UZDN","UZDO","UZDP","UZDQ","UZDR","UZDS","UZDT","UZDU","UZDV","UZEW","UZEX","UZEY","UZEZ","UZEA","UZEB","UZEC","UZED","UZEE","UZEF","UZEG","UZEH","UZEI","UZEJ"]
assert [cfg.rings == cfg.rings for ec in cfg.stepped_configs(99)]
assert [cfg.components == cfg.components for ec in cfg.stepped_configs(99)]
cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LEZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
assert [str(ec.windows()) for ec in cfg.stepped_configs(99)] == ["LEZO","LFAP","LFAQ","LFAR","LFAS","LFAT","LFAU","LFAV","LFAW","LFAX","LFAY","LFAZ","LFAA","LFAB","LFAC","LFAD","LFAE","LFBF","LFBG","LFBH","LFBI","LFBJ","LFBK","LFBL","LFBM","LFBN","LFBO","LFBP","LFBQ","LFBR","LFBS","LFBT","LFBU","LFBV","LFBW","LFBX","LFBY","LFBZ","LFBA","LFBB","LFBC","LFBD","LFBE","LFCF","LFCG","LFCH","LFCI","LFCJ","LFCK","LFCL","LFCM","LFCN","LFCO","LFCP","LFCQ","LFCR","LFCS","LFCT","LFCU","LFCV","LFCW","LFCX","LFCY","LFCZ","LFCA","LFCB","LFCC","LFCD","LFCE","LFDF","LFDG","LFDH","LFDI","LFDJ","LFDK","LFDL","LFDM","LFDN","LFDO","LFDP","LFDQ","LFDR","LFDS","LFDT","LFDU","LFDV","LFDW","LFDX","LFDY","LFDZ","LFDA","LFDB","LFDC","LFDD","LFDE","LFEF","LFEG","LFEH","LFEI","LFEJ"]
assert [cfg.rings == cfg.rings for ec in cfg.stepped_configs(99)]
assert [cfg.components == cfg.components for ec in cfg.stepped_configs(99)]

# EnigmaConfig mappings and simple encoding
cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAQ", "", "03.17.04.11")
assert cfg.stage_mapping_list() == ["ABCDEFGHIJKLMNOPQRSTUVWXYZ","LORVFBQNGWKATHJSZPIYUDXEMC","BJYINTKWOARFEMVSGCUDPHZQLX","ILHXUBZQPNVGKMCRTEJFADOYSW","YDSKZPTNCHGQOMXAUWJFBRELVI","ENKQAUYWJICOPBLMDXZVFTHRGS","PUIBWTKJZSDXNHMFLVCGQYROAE","UFOVRTLCASMBNJWIHPYQEKZDXG","JARTMLQVDBGYNEIUXKPFSOHZCW","LFZVXEINSOKAYHBRGCPMUDJWTQ","ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
assert cfg.enigma_mapping_list() == ["ABCDEFGHIJKLMNOPQRSTUVWXYZ","LORVFBQNGWKATHJSZPIYUDXEMC","FVCHTJGMKZRBDWAUXSOLPIQNEY","BDHQFNZKVWELXOIAYJCGRPTMUS","DKNUPMIGREZQLXCYVHSTWAFOBJ","QCBFMPJYXASDORKGTWZVHEULNI","LIUTNFSAOPCBMVDKGREYJWQXHZ","BAEQJTYUWIOFNKVMLPRXSZHDCG","AJMXBFCSHDILEGONYUKZPWVTRQ","LOYWFEZPNVSAXIBHTUKQRJDMCG","LOYWFEZPNVSAXIBHTUKQRJDMCG"]
assert cfg.enigma_mapping() == "LOYWFEZPNVSAXIBHTUKQRJDMCG"
assert cfg.enigma_encoding("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == "LGWLXXIYXCIEACMGMJECRORTHO"
assert cfg.enigma_encoding(cfg.enigma_encoding("GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE")) == "GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE"
cfg = EnigmaConfig.config_enigma("b-γ-IV-III-II", "XLMA", "LM.OR.TK.SC.FZ.QE", "11.01.06.01")
assert cfg.stage_mapping_list() == ["ABSDQZGHIJTMLNRPEOCKUVWXYF","AJDKSIRUXBLHWTMCQGZNPYFVOE","IKMQOSGRXBPZTDFNLJHUWYACEV","XGWMACUIVZSRBLQTHDKEOYPNFJ","VLPJYDCMKITWQSFBXNAHREUZOG","ENKQAUYWJICOPBLMDXZVFTHRGS","SPGFVOZTJDIBHRYCMUNKWALQEX","EMFRTYBQHZSNDXUWOLKPGICAVJ","WJXNYOGSARBQCPEKDHFMTZUIVL","AJPCZWRLFBDKOTYUQGENHXMIVS","ABSDQZGHIJTMLNRPEOCKUVWXYF"]
assert cfg.enigma_mapping_list() == ["ABSDQZGHIJTMLNRPEOCKUVWXYF","AJZKQERUXBNWHTGCSMDLPYFVOI","IBVPLOJWCKDARUGMHTQZNESYFX","VGYTRQZPWSMXDOUBIEHJLAKFCN","ECOHNXGBUAQZJFRLKYMIWVTDPS","AKLWBRYNFEDSIUXOCGPJHTVQMZ","SIBLPUEROVFNJWQYGZCDTKAMHX","KHMNWGTLUIYXZCOVBJFRPSEDQA","BSCPUGMQTAVILXEZJROHKFYNDW","JEPUHROQNAXFKIZSBGYLDWVTCM","JQPUHORENAXZTIFCBGYMDWVKSL"]
assert cfg.enigma_mapping() == "JQPUHORENAXZTIFCBGYMDWVKSL"
assert cfg.enigma_encoding("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == "HKNOIVPIQQDIUEPANGFXOOOCWH"
assert cfg.enigma_encoding(cfg.enigma_encoding("GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE")) == "GENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE"
cfg = EnigmaConfig.config_enigma("c-γ-V-VIII-III", "MFIQ", "ML.IO.QW.AG.DS.ZR", "13.19.02.16")
assert cfg.stage_mapping_list() == ["GBCSEFAHOJKMLNIPWZDTUVQXYR","CEGIKBOQSWUYMXDHVFZJLTRPNA","HVUCLIWSKTFXPGBNRZOYDJAMEQ","UYKNJZWDBSRPXIMOETVGLHCFQA","FSOKANUERHMBTIYCWLQPZXVGJD","RDOBJNTKVEHMLFCWZAXGYIPSUQ","ELPZHAXJNYDRKFCTSIBMGWQVOU","ZIWHQXTVNECUODPLYKJRASGMBF","WODUYKNAFVIEXPSMZQHJCBGLTR","ZFAOBRCPDTEUMYGXHWIVKQJNLS","GBCSEFAHOJKMLNIPWZDTUVQXYR"]
assert cfg.enigma_mapping_list() == ["GBCSEFAHOJKMLNIPWZDTUVQXYR","OEGZKBCQDWUMYXSHRAIJLTVPNF","BLWQFVURCADPEMOSZHKTXYJNGI","YPCEZHLTKUNOJXMVADRGFQSIWB","JCOADEBPMZIYHGTXFKLUNWQRVS","EOCRBJDWLQVUKTGSNHMYFPZAIX","HCPILYZQRSWGDMXBFJKOATUENV","VWLNUBFYKJGTHOMIXECPZRAQDS","BGEPCOKTIVNJASXFLYDMRQWZUH","FCBXAGEVDQYTZINRULOMWHJSKP","FCBXGAEVSWYTRONZUMILQHJDKP"]
assert cfg.enigma_mapping() == "FCBXGAEVSWYTRONZUMILQHJDKP"
assert cfg.enigma_encoding("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ") == "YGMHCRNJJFADFQWMYGZEVSQJDGHAYWFZMBKBVUOABSFBUAJKZLKE"
assert cfg.enigma_encoding(cfg.enigma_encoding("HLERHALTENXXJANSTERLEDESBISHERIGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE")) == "HLERHALTENXXJANSTERLEDESBISHERIGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBE"

# EnigmaConfig historical message encoding
msg = "KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP"
enc = "LANOTCTOUARBBFPMHPHGCZXTDYGAHGUFXGEWKBLKGJWLQXXTGPJJAVTOCKZFSLPPQIHZFXOEBWIIEKFZLCLOAQJULJOYHSSMBBGWHZANVOIIPYRBRTDJQDJJOQKCXWDNBBTYVXLYTAPGVEATXSONPNYNQFUDBBHHVWEPYEYDOHNLXKZDNWRHDUWUJUMWWVIIWZXIVIUQDRHYMNCYEFUAPNHOTKHKGDNPSAKNUAGHJZSMJBMHVTREQEDGXHLZWIFUSKDQVELNMIMITHBHDBWVHDFYHJOQIHORTDJDBWXEMEAYXGYQXOHFDMYUXXNOJAZRSGHPLWMLRECWWUTLRTTVLBHYOORGLGOWUXNXHMHYFAACQEKTHSJW"
cfg = EnigmaConfig.config_enigma("c-β-V-VI-VIII", EnigmaConfig.config_enigma("c-β-V-VI-VIII", "NAEM", "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12").enigma_encoding("QEOB"), "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12")
assert cfg.enigma_encoding(msg) == enc
assert cfg.enigma_encoding(cfg.enigma_encoding(msg)) == msg
assert cfg.enigma_encoding(msg) == enc

# TBD - Marked configs (e.g. with alternate marking)
# USE - Haskell output for first and last lines needs to be trimmed to match; marked output needs \818\773 replaced with ̲̅
cfg = EnigmaConfig.config_enigma("c-β-V-II-III", "KFIE", "IO.QW.AG.DX.ZR", "11.19.21.16")
assert cfg.config_string(' ') == "    OGUSZKBIHVFPXTALWYDNCJQMRE  KFIE  01 14 15 16"
assert cfg.config_string('J') == "J > OGUSZKBIHV̲̅FPXTALWYDNCJQMRE  KFIE  01 14 15 16" #J > OGUSZKBIHV̲̅FPXTALWYDNCJQMRE  KFIE  01 14 15 16
assert cfg.config_string_internal(' ').split('\n') == ["    ABCDEFGHIJKLMNOPQRSTUVWXYZ","  P GBCXEFAHOJKLMNIPWZSTUVQDYR         IO.QW.AG.DX.ZR","  1 PTHRLVXFDBZMOQSUWNACEIGKYJ  E  16  III","  2 YOCSLZBKRHAQMVPWEUDGJNXTIF  I  15  II","  3 UYKNJZWDBSRPXIMOETVGLHCFQA  F  14  V","  4 LEYJVCNIXWPBQMDRTAKZGFUHOS  K  01  β","  R RDOBJNTKVEHMLFCWZAXGYIPSUQ         c","  4 RLFOBVUXHDSANGYKMPZQWEJICT         β","  3 ZIWHQXTVNECUODPLYKJRASGMBF         V","  2 KGCSQZTJYUHEMVBOLIDXRNPWAF         II","  1 SJTIUHWCVZXELRMANDOBPFQGYK         III","  P GBCXEFAHOJKLMNIPWZSTUVQDYR         IO.QW.AG.DX.ZR","    OGUSZKBIHVFPXTALWYDNCJQMRE"]
assert cfg.config_string_internal('Y').split('\n') == ["Y > ABCDEFGHIJKLMNOPQRSTUVWXY̲̅Z","  P GBCXEFAHOJKLMNIPWZSTUVQDY̲̅R         IO.QW.AG.DX.ZR","  1 PTHRLVXFDBZMOQSUWNACEIGKY̲̅J  E  16  III","  2 YOCSLZBKRHAQMVPWEUDGJNXTI̲̅F  I  15  II","  3 UYKNJZWDB̲̅SRPXIMOETVGLHCFQA  F  14  V","  4 LE̲̅YJVCNIXWPBQMDRTAKZGFUHOS  K  01  β","  R RDOBJ̲̅NTKVEHMLFCWZAXGYIPSUQ         c","  4 RLFOBVUXHD̲̅SANGYKMPZQWEJICT         β","  3 ZIWH̲̅QXTVNECUODPLYKJRASGMBF         V","  2 KGCSQZTJ̲̅YUHEMVBOLIDXRNPWAF         II","  1 SJTIUHWCVZ̲̅XELRMANDOBPFQGYK         III","  P GBCXEFAHOJKLMNIPWZSTUVQDYR̲̅         IO.QW.AG.DX.ZR","R < OGUSZKBIHVFPXTALWYDNCJQMR̲̅E"]
print(["Y > ABCDEFGHIJKLMNOPQRSTUVWXY̲̅Z","  P GBCXEFAHOJKLMNIPWZSTUVQDY̲̅R         IO.QW.AG.DX.ZR","  1 PTHRLVXFDBZMOQSUWNACEIGKY̲̅J  E  16  III","  2 YOCSLZBKRHAQMVPWEUDGJNXTI̲̅F  I  15  II","  3 UYKNJZWDB̲̅SRPXIMOETVGLHCFQA  F  14  V","  4 LE̲̅YJVCNIXWPBQMDRTAKZGFUHOS  K  01  \946","  R RDOBJ̲̅NTKVEHMLFCWZAXGYIPSUQ         c","  4 RLFOBVUXHD̲̅SANGYKMPZQWEJICT         \946","  3 ZIWH̲̅QXTVNECUODPLYKJRASGMBF         V","  2 KGCSQZTJ̲̅YUHEMVBOLIDXRNPWAF         II","  1 SJTIUHWCVZ̲̅XELRMANDOBPFQGYK         III","  P GBCXEFAHOJKLMNIPWZSTUVQDYR̲̅         IO.QW.AG.DX.ZR","R < OGUSZKBIHVFPXTALWYDNCJQMR̲̅E"])
cfg = EnigmaConfig.config_enigma("C-I-III-VIII", "ALO", "GH.QW.LK.ZM.XN.CV", "01.21.01")
assert cfg.config_string(' ') == "    YEHSBIOCFTPVRZGKXMDJWLUQAN  ALO  01 18 15"
#assert cfg.config_string('E') ==
assert cfg.config_string_internal(' ').split('\n') == ["    ABCDEFGHIJKLMNOPQRSTUVWXYZ","  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV","  1 LDMYQIZUGKSHRWCTFXJAONVEBP  O  15  VIII","  2 FPJTVDBZXKMOQSULYACGEIWHNR  L  18  III","  3 EKMFLGDQVZNTOWYHXUSPAIBRCJ  A  01  I","  R FVPJIAOYEDRZXWGCTKUQSBNMHL         C","  3 UWYGADFPVZBECKMTHXSLRINQOJ         I","  2 RGSFUATXVCJPKYLBMZNDOEWIQH         III","  1 TYOBXQILFSJACVUZEMKPHWNRDG         VIII","  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV","    YEHSBIOCFTPVRZGKXMDJWLUQAN"]
#assert cfg.config_string_internal('A').split('\n') ==
# TBD - Add assertions above <<<

# print(cfg.config_string_internal(' ').split('\n'))
# print(["    ABCDEFGHIJKLMNOPQRSTUVWXYZ","  P GBCXEFAHOJKLMNIPWZSTUVQDYR         IO.QW.AG.DX.ZR","  1 PTHRLVXFDBZMOQSUWNACEIGKYJ  E  16  III","  2 YOCSLZBKRHAQMVPWEUDGJNXTIF  I  15  II","  3 UYKNJZWDBSRPXIMOETVGLHCFQA  F  14  V","  4 LEYJVCNIXWPBQMDRTAKZGFUHOS  K  01  β","  R RDOBJNTKVEHMLFCWZAXGYIPSUQ         c","  4 RLFOBVUXHDSANGYKMPZQWEJICT         β","  3 ZIWHQXTVNECUODPLYKJRASGMBF         V","  2 KGCSQZTJYUHEMVBOLIDXRNPWAF         II","  1 SJTIUHWCVZXELRMANDOBPFQGYK         III","  P GBCXEFAHOJKLMNIPWZSTUVQDYR         IO.QW.AG.DX.ZR","    OGUSZKBIHVFPXTALWYDNCJQMRE"])


print('---------------------')

print()
print('Components:')
print(component(u'UX.MI'))
print(component(u'I'))

ec = EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
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

print(component("II").mapping(7, FWD))
#print([str(ec.windows())] + [str(ec.step().windows()) for _ in xrange (99)])
cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAQ", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print(cfg.positions)
print(cfg)
for m in cfg.stage_mapping_list():
    print(m)

cfg = EnigmaConfig.config_enigma("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
print(cfg)

print([str(ec.windows()) for ec in cfg.stepped_configs(0)])
print([str(ec.windows()) for ec in cfg.stepped_configs(99)])


print(component("I").mapping(1, FWD))
print(component("II").mapping(-1, FWD))
print(component("III").mapping(2, FWD))
print(component("IV").mapping(-2, FWD))

print(component("VIII").mapping(11, REV))
print(component("B").mapping(-12, REV))
print(component("C").mapping(17, REV))
print(component("V").mapping(-8, REV))


print([str(ec[1].windows()) for ec in zip("ABCDEFG",cfg.stepped_configs())])
cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LEZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print([ec[1].windows() for ec in zip([1, 2, 3],cfg.stepped_configs())])
cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LEZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print([ec[1].windows() for ec in zip([1, 2, 3],[i for i in cfg.stepped_configs(3)])])

print(EnigmaConfig._marked_mapping(LETTERS, 3))
print(EnigmaConfig._marked_mapping(LETTERS, 0))
print(EnigmaConfig._marked_mapping(LETTERS, 10))
print(EnigmaConfig._marked_mapping(LETTERS, 25))
print(EnigmaConfig._marked_mapping(LETTERS, 25, lambda c: '[' + c + ']'))

print(len(LETTERS))
print(len(EnigmaConfig._marked_mapping(LETTERS, 3)))
print(len(EnigmaConfig._marked_mapping(LETTERS, 25, lambda c: '[' + c + ']')))

print(cfg)
print(cfg.config_string('A'))
print(cfg.config_string(' '))
print(cfg.config_string('Z'))
print(cfg.config_string('K'))
print()
cfg.print_operation("ABCDE")
cfg.print_operation_internal("ABCDE")
cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAQ", "UX.MO.KZ.AY.EF.PL", "03.17.04.11")
print(cfg.enigma_mapping_list())
print(cfg.config_string_internal('Q'))
print(cfg.config_string_internal(' '))



cfg = EnigmaConfig.config_enigma("c-β-V-VI-VIII", EnigmaConfig.config_enigma("c-β-V-VI-VIII", "NAEM", "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12").enigma_encoding("QEOB"), "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12")
cProfile.run('cfg.enigma_encoding("KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP")')
cProfile.run('[str(ec.windows()) for ec in cfg.stepped_configs(10000)]')

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
