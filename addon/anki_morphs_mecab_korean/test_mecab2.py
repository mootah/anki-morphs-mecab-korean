from anki_morphs_mecab_korean.reading import MecabKoreanController
controller = MecabKoreanController()
morphs = controller.get_morphs("예쁜 꽃이 피었다")
for lemma, surface, pos, sub_pos, feature in morphs:
    print(f"surface: {surface}, lemma: {lemma}, pos: {pos}, sub_pos: {sub_pos}")
