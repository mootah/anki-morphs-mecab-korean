from __future__ import annotations
import os
from pathlib import Path
from aqt import mw
import mecab_ko as MeCab
import openkorpos_dic
from . import constants

class NameLoader:
    def __init__(self):
        self._names = None
        self._mtime = None

        if mw:
            profile_path = Path(mw.pm.profileFolder())
            self._path = profile_path / constants.NAMES_TXT_FILE_NAME
        else:
            self._path = Path(__file__).resolve().parent / "names.txt"
            
    def get_names(self) -> set[str]:
        if not self._path.exists():
            return set()

        mtime = os.path.getmtime(self._path)

        if self._mtime == mtime and self._names is not None:
            return self._names
        
        self._mtime = mtime

        with open(self._path, mode="r", encoding="utf-8") as f:
            self._names = set(filter(None, (line.strip().lower() for line in f)))

        return self._names


def has_jongseong(text: str) -> bool:
    if not text:
        return False
    codepoint = ord(text[-1])
    if 0xAC00 <= codepoint <= 0xD7A3:
        return (codepoint - 0xAC00) % 28 > 0
    return False


class MecabKoreanController:
    def __init__(self) -> None:
        args = openkorpos_dic.MECAB_ARGS
        user_dic_path = Path(__file__).resolve().parent / "user_nnp.dic"
        if user_dic_path.exists():
            args += f' -u "{user_dic_path}"'
        self._mecab = MeCab.Tagger(args)
        self._name_loader = NameLoader()

    def parse(self, text: str):
        return self._mecab.parse(text)

    def get_morphs(self, text: str) -> list[dict[str, str]]:
        replaced_names = []
        names = self._name_loader.get_names()
        
        if names:
            import re
            sorted_names = sorted(names, key=len, reverse=True)
            escaped_names = [re.escape(name) for name in sorted_names]
            pattern = re.compile(f"({'|'.join(escaped_names)})", flags=re.IGNORECASE)
            
            def replacer(match):
                name = match.group(0)
                replaced_names.append(name)
                return "PROPNT" if has_jongseong(name) else "PROPNF"
                
            text = pattern.sub(replacer, text)

        node = self._mecab.parseToNode(text)
        morphs = []
        
        while node:
            surface = node.surface
            if surface:
                features = node.feature.split(',')
                lemma = surface
                
                if surface in ("PROPNT", "PROPNF") and replaced_names:
                    original_name = replaced_names.pop(0)
                    lemma = original_name
                    surface = original_name
                    pos = "名詞"
                    sub_pos = "固有名詞"
                else:
                    raw_pos = features[0] if len(features) > 0 else ""
                    base_pos = raw_pos.split('+')[0]
                    pos, sub_pos = constants.POS_MAP.get(base_pos, ("不明", raw_pos))
                    
                    if len(features) >= 5 and features[4] == 'Compound':
                        lemma = features[3] if len(features) >= 4 and features[3] != '*' else surface
                    elif len(features) >= 8 and features[7] != '*':
                        lemma = features[7].split('+')[0].split('/')[0]
                    elif len(features) >= 4 and features[3] != '*':
                        lemma = features[3]
                    
                morphs.append((lemma, surface, pos, sub_pos, node.feature))
                
            node = node.next
            
        return morphs

