__author__ = 'tixie'

SearchEngines = {
    'alibaba': 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={0}&start={1}',
    'amazon': 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={0}&page={1}',
    'baidu': 'http://www.baidu.com/s?wd={0}&pn={1}'
}


SearchEngineResultSelectors= {
    'alibaba': '//h3/a/@href',
    'amazon':'//h2/a/@href',
    'baidu':'//h3/a/@href',
}
