import pandas as pd
import konlpy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis.sklearn

# tokenization 함수를 만들어둠
def tokenize_korean_text(text):
    text = re.sub(r'[^,.?!\w\s]','', str(text))  ## ,.?!와 문자+숫자+_(\w)와 공백(\s)만 남김  
    okt = konlpy.tag.Okt()
    Okt_morphs = okt.pos(text) 
    
    words = []
    for word, pos in Okt_morphs:
        if pos == 'Adjective' or pos == 'Verb' or pos == 'Noun':  # 이 경우에는 형용사, 동사, 명사만 남김
            words.append(word)

    words_str = ' '.join(words)
    return words_str


# df['요약']를 하나씩 tokenize해서 list로 저장
tokenized_list = []
drop_corpus = []

def topic_modeling(txt):
    for text in txt['요약']:
        tokenized_list.append(tokenize_korean_text(text))

    for index in range(len(tokenized_list)):
        corpus = tokenized_list[index]
        if len(set(corpus.split())) < 3:   # 같은 단어 1-2개만 반복되는 corpus도 지우기 위해 set()을 사용
            txt.drop(index, axis='index', inplace=True)
            drop_corpus.append(corpus)
    
    for corpus in drop_corpus:
        tokenized_list.remove(corpus)

    txt.reset_index(drop=True, inplace=True)


def mainmodeling(keyword, txt):
    topic_modeling(txt)
    #LDA 는 Count기반의 Vectorizer만 적용 
    count_vectorizer = CountVectorizer(max_df=0.1, max_features=1000, min_df=2, ngram_range=(1,2))
    # 2개의 문서 미만으로 등장하는 단어는 제외, 전체의 10% 이상으로 자주 등장하는 단어는 제외
    # bigram도 포함

    feat_vect = count_vectorizer.fit_transform(tokenized_list)

    lda = LatentDirichletAllocation(n_components=6)  # 토픽 수는 6개로 설정
    lda.fit(feat_vect)

    vis = pyLDAvis.sklearn.prepare(lda, feat_vect, count_vectorizer)
    pyLDAvis.save_html(vis, keyword+'_lda.html')


