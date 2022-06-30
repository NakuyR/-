import pandas as pd

from searchNewsOfKeyword import findNewsOfKeyword
from crawlingNewsInfo import getNewsInfo
from time import time
from TopicModeling import mainmodeling

t = time()

keyword = "CJ"

newsUrlList = findNewsOfKeyword(keyword)

result = getNewsInfo(newsUrlList)

df = pd.DataFrame.from_records(result)

df.to_excel(keyword + '_' + 'result.xlsx', encoding="utf-8-sig")

mainmodeling(keyword,df)

print("total time : ", time() - t, "sec")