from __future__ import annotations

import mecab_ko as MeCab
import openkorpos_dic


POS_MAP = {
    "NNG":  ("名詞", "一般"),
    "NNP":  ("名詞", "固有名詞"),
    "NNB":  ("名詞", "依存名詞"),
    "NNBC": ("名詞", "単位名詞"),
    "NR":   ("名詞", "数詞"),
    "NP":   ("名詞", "代名詞"),
    "VV":   ("用言", "動詞"),
    "VA":   ("用言", "形容詞"),
    "VX":   ("用言", "補助用言"),
    "VCP":  ("用言", "指定詞"),
    "VCN":  ("用言", "否定指定詞"),
    "MM":   ("冠形詞", "冠形詞"),
    "MAG":  ("副詞", "一般副詞"),
    "MAJ":  ("副詞", "接続副詞"),
    "IC":   ("感動詞", "感動詞"),
    "JKS":  ("助詞", "主格助詞"),
    "JKC":  ("助詞", "補格助詞"),
    "JKG":  ("助詞", "冠形格助詞"),
    "JKO":  ("助詞", "目的格助詞"),
    "JKB":  ("助詞", "副詞格助詞"),
    "JKV":  ("助詞", "呼格助詞"),
    "JKQ":  ("助詞", "引用格助詞"),
    "JX":   ("助詞", "補助詞"),
    "JC":   ("助詞", "接続助詞"),
    "EP":   ("語尾", "先語末語尾"),
    "EF":   ("語尾", "終止語尾"),
    "EC":   ("語尾", "接続語尾"),
    "ETN":  ("語尾", "名詞形語尾"),
    "ETM":  ("語尾", "冠形形語尾"),
    "XPN":  ("接頭辞", "接頭辞"),
    "XSN":  ("接尾辞", "名詞接尾辞"),
    "XSV":  ("接尾辞", "動詞接尾辞"), 
    "XSA":  ("接尾辞", "形容詞接尾辞"),
    "XR":   ("語根", "語根"),
    "SF":   ("記号", "句読点"),
    "SP":   ("記号", "句読点"),
    "SC":   ("記号", "句読点"),
    "SS":   ("記号", "括弧"),
    "SE":   ("記号", "記号"),
    "SO":   ("記号", "記号"),
    "SY":   ("記号", "記号"),
    "SL":   ("その他", "外国文字"),
    "SH":   ("その他", "漢字"),
    "SN":   ("その他", "数字")
}

class MecabKoreanController:
    def __init__(self) -> None:
        self._mecab = MeCab.Tagger(openkorpos_dic.MECAB_ARGS)

    def parse(self, text: str):
        return self._mecab.parse(text)

    def get_morphs(self, text: str) -> list[dict[str, str]]:
        node = self._mecab.parseToNode(text)
        morphs = []
        
        while node:
            surface = node.surface
            if surface:
                features = node.feature.split(',')
                lemma = surface
                
                raw_pos = features[0] if len(features) > 0 else ""
                base_pos = raw_pos.split('+')[0]
                pos, sub_pos = POS_MAP.get(base_pos, ("不明", raw_pos))
                
                if len(features) >= 8 and features[7] != '*':
                    lemma = features[7].split('+')[0].split('/')[0]
                elif len(features) >= 4 and features[3] != '*':
                    lemma = features[3]
                    
                morphs.append((lemma, surface, pos, sub_pos))
                
            node = node.next
            
        return morphs


if __name__ == "__main__":
    import sys
    from rich import print
    parser = MecabKoreanController()
    text = sys.argv[1]
    print(parser.get_morphs(text))
