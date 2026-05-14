import mecab_ko as MeCab
import openkorpos_dic

mecab = MeCab.Tagger(openkorpos_dic.MECAB_ARGS)
node = mecab.parseToNode("다다르다")
while node:
    print(node.surface, node.feature)
    node = node.next
