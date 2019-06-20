"""
爬取静态页面，使用requests,Beautiful
打印所有 主题以及其包含的标题
每个标题对应一个url，其内容就是我们要爬取的名言
设置了可以自由选取下载哪些主题下的标题的名言
同时对下载的文件进行保存和按索引命名
在输入错误时，会弹出警示并允许重新输入
"""

import requests
from bs4 import BeautifulSoup as BSP4
title_index = 0   # 给所有标题做个索引
g_url_set = set()   # 标题对应的url集合


def save_text(motto_text, num):
    """
    将下载的名言保存本地
    :param motto_soup: 名言soup
    :return:
    """
    print(motto_text)
    if num == 0:
        with open(f'files/motto_all.txt', 'w+', encoding='utf8') as f:
            f.write(motto_text)
    else:
        with open(f'files/motto_{num}.txt', 'w+',encoding='utf8') as f:
            f.write(motto_text)



def parse_url():
    """
    真正从title_url网站中下载要下载得文本内容
    :param url:
    :return:
    """
    num = input(f"请输入你要爬取的名言序号（1-{title_index}）：（输入0可以全部爬取）")
    motto_text = ''
    try:
        num = int(num)
        if num == 0:
            for url in g_url_set:
                response = requests.get(url)
                html_doc = response.content
                soup = BSP4(html_doc, 'lxml')
                motto_list = soup.select('.content p')

                for motto in motto_list:
                    motto_text += (motto.text+'\n')
                save_text(motto_text, num)
        elif num in range(1, title_index):
            url_list = list(g_url_set)
            url = url_list[num-1]
            response = requests.get(url)
            html_doc = response.content
            soup = BSP4(html_doc, 'lxml')
            motto_list = soup.select('.content p')
            for motto in motto_list:
                motto_text += (motto.text+'\n')
            save_text(motto_text, num)

            inq = input("是否继续爬取：输入1继续，其他键退出")
            if inq == '1':
                parse_url()
            else:
                pass
        else:
            print('------------------------------')
            print(f'|  请入正确的数字！（0-{title_index}）  |')
            print('------------------------------')
            parse_url()
    except ValueError:
        print('------------------------------')
        print(f'|  请入正确的数字！（0-{title_index}）  |')
        print('------------------------------')
        parse_url()




def parse_theme(theme, tbox_soup):
    """
    :param theme: tbox下得theme主题
    :param tbox_soup:  tbox_soup为了得到title_soup
    :return:
    """

    theme_name = theme.text
    print('----------------------------')
    print(f'         ' + theme_name)
    print('----------------------------')
    title_list = tbox_soup.select('dd li')
    [parse_title(title) for title in title_list]




def parse_title(title):
    """
    :param title: tbox下得标题
    :param title_index: 标记索引
    :return:
    """
    global title_index
    title_index += 1
    title_name = title.a["title"]
    print(f'{title_index}、' + title_name)
    title_href = title.a["href"]  # 这里不明白
    url = 'https://www.geyanw.com/' + title_href
    if url not in g_url_set:
        g_url_set.add(url)


def parse_tbox(tbox_soup):
    """
    对单个tbox内容处理， 一个tbox下有一个theme 以及同级得10个title
    :return:
    """
    theme_list = tbox_soup.select('dt a')
    [parse_theme(theme, tbox_soup) for theme in theme_list]


def parse(response):
    """
    对下载得页面进行处理
    :param response:
    :return:
    """
    html_doc = response.content
    soup = BSP4(html_doc, 'lxml')
    tbox_list = soup.select('.listbox dl')
    [parse_tbox(tbox) for tbox in tbox_list]


def download(url, filename='index'):
    """
    下载器，对起始url处理
    :param url:  起始url
    :param filename: 将下载得页面保存到本地
    :return:
    """
    response = requests.get(url)
    store_local_html(filename, response)
    return response


def store_local_html(filename, response):
    """
    将请求返回得html信息保存在本地
    :param filename:
    :param response:
    :return:
    """
    html_doc = response.text
    with open(f'html/job_{filename}', 'w', encoding='utf8') as f:
        f.write(html_doc)


def main():
    base_url = 'https://www.geyanw.com/'
    response = download(base_url)
    parse(response)
    parse_url()


if __name__ == '__main__':
    main()
