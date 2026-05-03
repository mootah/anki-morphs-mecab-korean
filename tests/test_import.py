from __future__ import annotations

import importlib
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_ROOT = REPO_ROOT / "addon"

if str(ADDON_ROOT) not in sys.path:
    sys.path.insert(0, str(ADDON_ROOT))

MODULE_NAME = "anki_morphs_mecab_korean.reading"


def test_import_companion_addon():
    module = importlib.import_module(MODULE_NAME)

    assert module is not None


def test_mecab_ko_is_vendored():
    module = importlib.import_module(MODULE_NAME)

    parser = module.MecabKoreanController()

    parsed = parser.parse("프로그래밍을 못해서 문송합니다.")

    assert parsed is not None

def test_mecab_ko_get_morphs():
    module = importlib.import_module(MODULE_NAME)

    parser = module.MecabKoreanController()

    morphs = parser.get_morphs("프로그래밍을 못해서 문송합니다.")

    assert morphs is not None
    assert len(morphs) > 0
    
    for morph in morphs:
        assert isinstance(morph, tuple)
        lemma, surface, pos, sub_pos = morph
        assert isinstance(lemma, str)
        assert isinstance(surface, str)
        assert isinstance(pos, str)
        assert isinstance(sub_pos, str)
