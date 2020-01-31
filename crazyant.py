import requests
from bs4 import BeautifulSoup
import pprint  # 打印漂亮格式用
import json


# ########## 下载所有的页面HTML###########
def dowload_all_htmls():
    # htmls用于存放页面,有27页，循环27次
    htmls = []
    for idx in range(2):
        url = f"http://www.crazyant.net/page/{idx + 1}"
        print("craw html:", url)
        r = requests.get(url)
        # 成功状态码为200
        if r.status_code != 200:
            raise Exception("Hey,there is Error!")
        # 把html文本存储到列表中
        htmls.append(r.text)
    return htmls


# 执行爬取
htmls = dowload_all_htmls()


# ##########解析单个HTML页面得到数据###########
def parse_single_html(html):
    '''
    解析，得到数据
    return list({"link","title",[label]})
    '''
    # 将字符串串起来，用parser解析
    soup = BeautifulSoup(html, 'html.parser')
    # 返回article标签里的所有元素
    articles = soup.find_all("article")
    datas = []
    for article in articles:
        # 查找超链接
        title_node = (
            # article下方的a元素只有一个，因此用find，如多个用find_all
            # 下划线如def，class可以解决关键字冲突
            article
                .find("h2", class_="entry-title")
                .find("a")
        )
        title = title_node.get_text()
        link = title_node["href"]
        # 查找标签列表
        tag_nodes = (
            article
                .find("footer", class_="entry-footer")
                .find("span", class_="tags-links")
                .find_all("a")
        )
        # 对应每个tag_node，获取他的名字，也就是tag_node.get_text()
        tags = [tag_node.get_text() for tag_node in tag_nodes]
        datas.append(
            {"title:": title, "link:": link, "tags:": tags}
        )
    return datas


# 打印爬取的内容
# pprint.pprint(parse_single_html(htmls[0]))

# 执行所有的HTML页面解析
all_datas = []
for html in htmls:
    '''
    append可以是元素和数组
    extend扩展原来的列表
    '''
    all_datas.extend(parse_single_html(html))

# 查看长度
print("len:", len(all_datas))

# 将结果输出存储  ①mysql  ②本地json
with open("all_article_links.json", "w") as fout:
    for data in all_datas:
        fout.write(json.dumps(data, ensure_ascii=False) + "\n")
