import requests
import re

# div class="ellipsis rank01 안의 내용
PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">(.*?)</div>', re.DOTALL)
# 위 안의 a 안의 내용
PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>', re.DOTALL)

def get_tag_attribute(attribute_name, tag_string):
    # 특정 태그 문자열 tag_string 에서 attribute_name 에 해당하는 속성의 값을 리턴하는 함수
    pattern_01 = re.compile(r'<.*? attribute_name="(.*?)">', re.DOTALL)
    return re.search(pattern_01, tag_string).group(1)

def get_tag_contetnt(tag_string):
    # 특정 tag 문자열 tag_string 이 가진 내용을 리턴
    pattern_01 = re.compile(r'<.*?>(.*?)</.*?>', re.DOTALL)
    if '</.*?>' not in tag_string:
        return ''
    else:
        return re.search(pattern_01, tag_string).group(1)

# response = requests.get('http://www.melon.com/chart/index.htm')
# print(response.text)

# f = open('melon.html', 'rt')
# source = f.read()
# f.close()

source = open('melon.html', 'rt').read()

match_list = re.finditer(PATTERN_DIV_RANK01, source)
for match_div_rank01 in match_list:
    div_rank01_content = match_div_rank01.group()

    title = re.search(PATTERN_A_CONTENT, div_rank01_content).group(1)
    print(title)

# p = re.compile(r'<a.*?</a>')
# result = re.findall(p, source)
# for index, item in enumerate(result):
#     print(index, result)

