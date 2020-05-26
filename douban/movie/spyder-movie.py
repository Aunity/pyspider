#!/usr/bin/env python
'''
@Author ymh
@Email  maohuay@hotmail.com
@Date   2020-05-19 23:19:45
@Web    https://github.com/Aunity
'''

import re
import requests
import pandas as pd
from lxml import etree

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
def get_types_of_movie():
    url = "https://movie.douban.com/chart"
    response = requests.get(url, headers=headers)
    page_text = response.text
    html = etree.HTML(page_text)
    span_list = html.xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
    movie_types = []

    for span in span_list:
        span_text = span.xpath('./a/text()')[0]
        span_href = 'https://movie.douban.com'+span.xpath('./a/@href')[0]
        match = re.search(r'type=(\d+)&', span_href)
        type_id = match.groups(0)[0]
        movie_types.append((span_text, type_id))
    movie_types = sorted(movie_types, key=lambda x: int(x[1]))
    typefile = "douban_movie_types.txt"
    with open(typefile,'w', encoding='utf-8') as fw:
        for movie_type in movie_types:
            fw.write("%s %s\n"%(movie_type[0],movie_type[1]))
    return movie_types

def get_number_of_movies(type_id, interval_id):
    url = "https://movie.douban.com/j/chart/top_list_count"
    paras = {
      "type": str(type_id),
      "interval_id": interval_id
    }
    response = requests.get(url, params=paras, headers=headers)
    page_text = response.json()
    # print(page_text.keys())
    total = page_text["total"]
    return total

def parse_page(json_text):
    dic = {}
    keys = json_text[0].keys()
    for k in keys:
        dic[k] = []

    for node in json_text:
        for k in keys:
            v = node[k]
            if type(v)==list:
                if len(v) == 0:
                    v = ' '
                else:
                    v = ' '.join(v)
            dic[k].append(v)
    df = pd.DataFrame(dic)
    return df

def get_movies_by_interval(type_id, interval_id_0, interval_id_1):
    ### get the number of this type at the interval_id
    url = "https://movie.douban.com/j/chart/top_list"
    interval_id = "%d:%d" % (interval_id_0, interval_id_1)
    total = get_number_of_movies(type_id, interval_id)
    paras = {
      "type": str(type_id),
      "interval_id": interval_id,
      "action": "",
      "start": "0",
      "limit": str(total)
    }

    response = requests.get(url, params=paras, headers=headers)
    page_text = response.json()
    df = parse_page(page_text)
    fname = "%s-%d_%d.csv"%(str(type_id), interval_id_0, interval_id_1)
    print(fname)
    df.to_csv(fname, index=False, encoding='utf-8')

def loop_interval(type_id):
    interval_ids = [
        (100,90),(90,80),(80,70),(70,60),(60, 50),
        (50,40),(40,30),(30,20),(20,10),(10,0)
    ]
    for interval in interval_ids:
        get_movies_by_interval(type_id, *interval)
        print(" 完成%d:%d的爬取..."%interval)


def start_spaider(movie_types):
    for t,tid in movie_types:
        print("开始爬取%s类电影："%t)
        loop_interval(tid)
        print()


def main():
    movie_types = get_types_of_movie()
    start_spaider(movie_types)

if __name__ == '__main__':
    main()