import re

import requests

__all__ = (
    'get_tag_attribute'
    'get_tag_content'
    'find_tag'
)


def save_melon():
    '''
    melon chart 받아서 html 파일에 저장
    :return: None
    '''
    response = requests.get('https://www.melon.com/chart/index.htm')
    source = response.text
    with open('melon.html' , 'wt') as f:
        f.write(source)


def get_tag_attribute(attribute_name, tag_string):
    """
    특정 tag문자열(tag_string)에서 attribute_name에 해당하는 속성의 값을 리턴하는 함수
    :param attribute_name: 태그가 가진 속성명
    :return: 속성이 가진 값
    """
    p_first_tag = re.compile(r'^.*?<.*?>', re.DOTALL)
    first_tag = re.search(p_first_tag, tag_string).group()

    # 문자열 포맷에 이름 붙이고, format()에서 키워드인수로 전달
    p = re.compile(r'^.*?<.*?{attribute_name}="(?P<value>.*?)".*?>'.format(
        attribute_name=attribute_name
    ), re.DOTALL)
    m = re.search(p, first_tag)
    if m:
        return m.group('value')
    return ''


def get_tag_content(tag_string):
    """
    특정 tag문자열(tag_string)이 가진 내용을 리턴
    tag문자열이 스스로 열고 닫는 태그 (ex: img태그)일 경우엔 공백을 반환
    :param tag_string:
    :return:
    """
    p = re.compile(r'<.*?>(?P<value>.*?)(?=</.*?>)', re.DOTALL)
    m = re.search(p, tag_string)
    if m:
        return get_tag_content(m.group('value'))
    elif re.search(r'[<>]', tag_string):
        return ''
    return tag_string

def find_tag(tag, tag_string, class_= None):
    """
    find tag in tag_string, return tag
    :param tag: tag to be found
    :param tag_string: source to be searched
    :return: first tag met
    """
    p = re.compile(r'.*?(<{tag}.*?{class_}.*?>.*?</{tag}>)'.format(
        tag=tag,
        class_=f'class=".*{class_}.*?"' if class_ else '',
    ), re.DOTALL)

    m = re.search(p, tag_string)
    if m:
        return m.group(1)
    return None