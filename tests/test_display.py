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
# USE - Haskell output for first and last lines needs to be trimmed to match; marked output needs \818\773 replaced with ̲̅
# TBD - Marked configs (e.g. with alternate marking)


def test_config_strings():
    cfg = EnigmaConfig.config_enigma('c-β-V-II-III', 'KFIE', 'IO.QW.AG.DX.ZR', '11.19.21.16')
    assert cfg.config_string(' ') == '    OGUSZKBIHVFPXTALWYDNCJQMRE  KFIE  01 14 15 16'
    assert cfg.config_string(' ', mark_func=lambda c: '[' + c + ']') == '     OGUSZKBIHVFPXTALWYDNCJQMRE   KFIE  01 14 15 16'
    assert cfg.config_string('J') == 'J > OGUSZKBIHV̲̅FPXTALWYDNCJQMRE  KFIE  01 14 15 16'
    assert cfg.config_string_internal(' ').split('\n') == ['    ABCDEFGHIJKLMNOPQRSTUVWXYZ', '  P GBCXEFAHOJKLMNIPWZSTUVQDYR         IO.QW.AG.DX.ZR', '  1 PTHRLVXFDBZMOQSUWNACEIGKYJ  E  16  III', '  2 YOCSLZBKRHAQMVPWEUDGJNXTIF  I  15  II', '  3 UYKNJZWDBSRPXIMOETVGLHCFQA  F  14  V', '  4 LEYJVCNIXWPBQMDRTAKZGFUHOS  K  01  β', '  R RDOBJNTKVEHMLFCWZAXGYIPSUQ         c', '  4 RLFOBVUXHDSANGYKMPZQWEJICT         β', '  3 ZIWHQXTVNECUODPLYKJRASGMBF         V', '  2 KGCSQZTJYUHEMVBOLIDXRNPWAF         II', '  1 SJTIUHWCVZXELRMANDOBPFQGYK         III', '  P GBCXEFAHOJKLMNIPWZSTUVQDYR         IO.QW.AG.DX.ZR', '    OGUSZKBIHVFPXTALWYDNCJQMRE']
    assert cfg.config_string_internal('Y').split('\n') == ['Y > ABCDEFGHIJKLMNOPQRSTUVWXY̲̅Z', '  P GBCXEFAHOJKLMNIPWZSTUVQDY̲̅R         IO.QW.AG.DX.ZR', '  1 PTHRLVXFDBZMOQSUWNACEIGKY̲̅J  E  16  III', '  2 YOCSLZBKRHAQMVPWEUDGJNXTI̲̅F  I  15  II', '  3 UYKNJZWDB̲̅SRPXIMOETVGLHCFQA  F  14  V', '  4 LE̲̅YJVCNIXWPBQMDRTAKZGFUHOS  K  01  β', '  R RDOBJ̲̅NTKVEHMLFCWZAXGYIPSUQ         c', '  4 RLFOBVUXHD̲̅SANGYKMPZQWEJICT         β', '  3 ZIWH̲̅QXTVNECUODPLYKJRASGMBF         V', '  2 KGCSQZTJ̲̅YUHEMVBOLIDXRNPWAF         II', '  1 SJTIUHWCVZ̲̅XELRMANDOBPFQGYK         III', '  P GBCXEFAHOJKLMNIPWZSTUVQDYR̲̅         IO.QW.AG.DX.ZR', 'R < OGUSZKBIHVFPXTALWYDNCJQMR̲̅E']
    assert cfg.config_string_internal('L', mark_func=lambda c: '[' + c + ']').split('\n') == [u'L > ABCDEFGHIJK[L]MNOPQRSTUVWXYZ', u'  P GBCXEFAHOJK[L]MNIPWZSTUVQDYR         IO.QW.AG.DX.ZR', u'  1 PTHRLVXFDBZ[M]OQSUWNACEIGKYJ  E  16  III', u'  2 YOCSLZBKRHAQ[M]VPWEUDGJNXTIF  I  15  II', u'  3 UYKNJZWDBSRP[X]IMOETVGLHCFQA  F  14  V', u'  4 LEYJVCNIXWPBQMDRTAKZGFU[H]OS  K  01  β', u'  R RDOBJNT[K]VEHMLFCWZAXGYIPSUQ         c', u'  4 RLFOBVUXHD[S]ANGYKMPZQWEJICT         β', u'  3 ZIWHQXTVNECUODPLYK[J]RASGMBF         V', u'  2 KGCSQZTJY[U]HEMVBOLIDXRNPWAF         II', u'  1 SJTIUHWCVZXELRMANDOB[P]FQGYK         III', u'  P GBCXEFAHOJKLMNI[P]WZSTUVQDYR         IO.QW.AG.DX.ZR', u'P < OGUSZKBIHVF[P]XTALWYDNCJQMRE']
    assert cfg.config_string_internal('L', mark_func=lambda c: 'β' + c + ']').split('\n') == [u'L > ABCDEFGHIJKβL]MNOPQRSTUVWXYZ', u'  P GBCXEFAHOJKβL]MNIPWZSTUVQDYR         IO.QW.AG.DX.ZR', u'  1 PTHRLVXFDBZβM]OQSUWNACEIGKYJ  E  16  III', u'  2 YOCSLZBKRHAQβM]VPWEUDGJNXTIF  I  15  II', u'  3 UYKNJZWDBSRPβX]IMOETVGLHCFQA  F  14  V', u'  4 LEYJVCNIXWPBQMDRTAKZGFUβH]OS  K  01  β', u'  R RDOBJNTβK]VEHMLFCWZAXGYIPSUQ         c', u'  4 RLFOBVUXHDβS]ANGYKMPZQWEJICT         β', u'  3 ZIWHQXTVNECUODPLYKβJ]RASGMBF         V', u'  2 KGCSQZTJYβU]HEMVBOLIDXRNPWAF         II', u'  1 SJTIUHWCVZXELRMANDOBβP]FQGYK         III', u'  P GBCXEFAHOJKLMNIβP]WZSTUVQDYR         IO.QW.AG.DX.ZR', u'P < OGUSZKBIHVFβP]XTALWYDNCJQMRE']
    cfg = EnigmaConfig.config_enigma('C-I-III-VIII', 'ALO', 'GH.QW.LK.ZM.XN.CV', '01.21.01')
    assert cfg.config_string(' ') == '    YEHSBIOCFTPVRZGKXMDJWLUQAN  ALO  01 18 15'
    assert cfg.config_string('') == '    YEHSBIOCFTPVRZGKXMDJWLUQAN  ALO  01 18 15'
    assert cfg.config_string() == '    YEHSBIOCFTPVRZGKXMDJWLUQAN  ALO  01 18 15'
    #assert cfg.config_string('E') ==
    assert cfg.config_string_internal(' ').split('\n') == ['    ABCDEFGHIJKLMNOPQRSTUVWXYZ', '  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV', '  1 LDMYQIZUGKSHRWCTFXJAONVEBP  O  15  VIII', '  2 FPJTVDBZXKMOQSULYACGEIWHNR  L  18  III', '  3 EKMFLGDQVZNTOWYHXUSPAIBRCJ  A  01  I', '  R FVPJIAOYEDRZXWGCTKUQSBNMHL         C', '  3 UWYGADFPVZBECKMTHXSLRINQOJ         I', '  2 RGSFUATXVCJPKYLBMZNDOEWIQH         III', '  1 TYOBXQILFSJACVUZEMKPHWNRDG         VIII', '  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV', '    YEHSBIOCFTPVRZGKXMDJWLUQAN']
    assert cfg.config_string_internal('').split('\n') == ['    ABCDEFGHIJKLMNOPQRSTUVWXYZ', '  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV', '  1 LDMYQIZUGKSHRWCTFXJAONVEBP  O  15  VIII', '  2 FPJTVDBZXKMOQSULYACGEIWHNR  L  18  III', '  3 EKMFLGDQVZNTOWYHXUSPAIBRCJ  A  01  I', '  R FVPJIAOYEDRZXWGCTKUQSBNMHL         C', '  3 UWYGADFPVZBECKMTHXSLRINQOJ         I', '  2 RGSFUATXVCJPKYLBMZNDOEWIQH         III', '  1 TYOBXQILFSJACVUZEMKPHWNRDG         VIII', '  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV', '    YEHSBIOCFTPVRZGKXMDJWLUQAN']
    assert cfg.config_string_internal().split('\n') == ['    ABCDEFGHIJKLMNOPQRSTUVWXYZ', '  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV', '  1 LDMYQIZUGKSHRWCTFXJAONVEBP  O  15  VIII', '  2 FPJTVDBZXKMOQSULYACGEIWHNR  L  18  III', '  3 EKMFLGDQVZNTOWYHXUSPAIBRCJ  A  01  I', '  R FVPJIAOYEDRZXWGCTKUQSBNMHL         C', '  3 UWYGADFPVZBECKMTHXSLRINQOJ         I', '  2 RGSFUATXVCJPKYLBMZNDOEWIQH         III', '  1 TYOBXQILFSJACVUZEMKPHWNRDG         VIII', '  P ABVDEFHGIJLKZXOPWRSTUCQNYM         GH.QW.LK.ZM.XN.CV', '    YEHSBIOCFTPVRZGKXMDJWLUQAN']
   #assert cfg.config_string_internal('A').split('\n') ==
    # TBD - Add assertions above <<<


