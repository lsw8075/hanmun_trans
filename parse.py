from konlpy.tag import Kkma
from konlpy.utils import pprint
kkma = Kkma()
sentence = '태조가 수창궁(壽昌宮)에서 왕위에 올랐다. 이보다 먼저 이달 12일에 공양왕(恭讓王)이 장차 태조의 사제(私第)로 거둥하여 술자리를 베풀고 태조와 더불어 동맹(同盟)하려고 하여 의장(儀仗)이 이미 늘어섰는데, 시중(侍中) 배극렴(裵克廉) 등이 왕대비(王大妃)에게 아뢰었다.'
pprint(kkma.pos(sentence))

test_id = 'kaa_10107020_003'

'''
    korean_raw = raw[0].find_all('p', {'class': 'paragraph'})
    korean_text = ''
    for paragraph in korean_raw:
        pconts = paragraph.contents
        for pcont in pconts:
            if type(pcont) == Tag:
                child = pcont.contents[0]
                if type(child) == Tag:
                    child = child.contents[0]
                korean_text += child
            else:
                korean_text += ' ' + str(pcont).strip() + ' '
    hanmun_raw = raw[1].find_all('p', {'class': 'paragraph'})
    hanmun_text = ''

    for paragraph in hanmun_raw:
        print(paragraph)
        print("========")
        
        for pcont in pconts:
            if type(pcont) == Tag:
                print(pcont)
                child = pcont.contents[0]
                if type(child) == Tag:
                    child = child.contents[0]
                hanmun_text += child
            else:
                hanmun_text += ' ' + str(pcont).strip() + ' '
    print(hanmun_text)
'''
