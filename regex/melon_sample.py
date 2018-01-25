import re

source = '''<tr class="lst50" id="lst50" data-song-no="30851703">




    <td><div class="wrap t_right"><input type="checkbox" title="다른사람을 사랑하고 있어 곡 선택" class="input_check " name="input_check" value="30851703"></div></td>
    <td><div class="wrap t_center"><span class="rank ">1</span><span class="none">위</span></div></td>


        <!-- 차트순위 추가 -->
        <td><div class="wrap">




                <span title="순위 동일" class="rank_wrap">
                    <span class="bullet_icons rank_static"><span class="none">순위 동일</span></span>
                    <span class="none">0</span>
                </span>




        </div></td>


    <td><div class="wrap">
        <a href="javascript:melon.link.goAlbumDetail('10131396');" title="Faces of Love" class="image_typeAll">
            <img onerror="WEBPOCIMG.defaultAlbumImg(this);" width="60" height="60" src="http://cdnimg.melon.co.kr/cm/album/images/101/31/396/10131396_500.jpg/melon/resize/120/quality/80/optimize" alt="Faces of Love - 페이지 이동">
            <span class="bg_album_frame"></span>
        </a>
    </div></td>
    <td><div class="wrap">
        <a href="javascript:melon.link.goSongDetail('30851703');" title="다른사람을 사랑하고 있어 곡정보" class="btn button_icons type03 song_info"><span class="none">곡정보</span></a>
    </div></td>
    <td><div class="wrap">
        <div class="wrap_song_info">
            <div class="ellipsis rank01"><span>






                <a href="javascript:melon.play.playSong('19030101',30851703);" title="다른사람을 사랑하고 있어 재생">다른사람을 사랑하고 있어</a>
            </span></div><br>
            <div class="ellipsis rank02">


                <a href="javascript:melon.link.goArtistDetail('514741');" title="수지 (SUZY) - 페이지 이동">수지 (SUZY)</a><span class="checkEllipsis" style="display: none;"><a href="javascript:melon.link.goArtistDetail('514741');" title="수지 (SUZY) - 페이지 이동">수지 (SUZY)</a></span>
            </div>

        </div>
    </div></td>
    <td><div class="wrap">
        <div class="wrap_song_info">
            <div class="ellipsis rank03">
                <a href="javascript:melon.link.goAlbumDetail('10131396');" title="Faces of Love - 페이지 이동">Faces of Love</a>
            </div>
        </div>
    </div></td>
    <td><div class="wrap">
        <button type="button" class="button_etc like" title="다른사람을 사랑하고 있어 좋아요" data-song-no="30851703" data-song-menuid="19030101"><span class="odd_span">좋아요</span>
<span class="cnt">
<span class="none">총건수</span>
21,070</span></button>
    </div></td>
    <td><div class="wrap t_center">
        <button type="button" title="듣기" class="button_icons play " onclick="melon.play.playSong('19030101',30851703);"><span class="none">듣기</span></button>
    </div></td>
    <td><div class="wrap t_center">
        <button type="button" title="담기" class="button_icons scrap " onclick="melon.play.addPlayList('30851703');"><span class="none">담기</span></button>
    </div></td>
    <td><div class="wrap t_center">
        <button type="button" title="다운로드" class="button_icons download " onclick="melon.buy.goBuyProduct('frm', '30851703', '3C0001', '','0', '19030101');"><span class="none">다운로드</span></button>
    </div></td>
    <td><div class="wrap t_center">
        <button type="button" title="뮤직비디오" class="button_icons video " onclick="melon.link.goMvDetail('19030101', '30851703','song');"><span class="none">뮤직비디오</span></button>
    </div></td>
    <td><div class="wrap t_center">
        <button type="button" title="링/벨" class="button_icons bell disabled" disabled="disabled" onclick="melon.buy.popPhoneDecorate('0010000000000000','30851703')"><span class="none">링/벨</span></button>
    </div></td>
</tr>'''


# div class="list50" > 4 th td > div class="wrap" > a class="image_typeALL > img
# div class="list50" > 6 th td > div class="wrap" > div class="wrap_song_info"
#   > div class="ellipsis rank01" > span > a > title


# PATTERN_IMG_01 = re.compile(r'class="image_typeAll">(.*?)</a>', re.DOTALL)
# img_container = re.search(PATTERN_IMG_01, source).group(1)
# print(img_container)
#
# PATTERN_IMG = re.compile(r'src="(.*?)"', re.DOTALL)
# img_src = re.search(PATTERN_IMG, img_container).group(1)
# print(img_src)

# td 태그 단위로 나누기
PATTERN_TD = re.compile(r'<td.*?>.*?</td>', re.DOTALL)
td_list = re.findall(PATTERN_TD, source)
# 나눈 td 단위의 요소를 리스트에 인덱스를 붙여 생성
for index, td in enumerate(td_list):
    td_strip = re.sub(r'[\n\t]+|\s{2,}', '', td)
    print(f'{index:02}: {td_strip}')

# list w/ index containing img src = list[3]
td_img_cover = td_list[3]
# extract img src inside tag <img>
PATTERN_IMG = re.compile(r'<img.*?src="(.*?)".*?>', re.DOTALL)
# group(1) is the first element in the group, group(0) or group() means entire group w/ every elements
url_img_cover = re.search(PATTERN_IMG, source).group(1)
print(url_img_cover)


# list w/ index containing album title = list[5]
td_title_author = td_list[5]
PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">(.*?)</div>', re.DOTALL)
PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>', re.DOTALL)
div_rank01 = re.search(PATTERN_DIV_RANK01, td_title_author).group()
title = re.search(PATTERN_A_CONTENT, div_rank01).group(1)
print(title)

"""
print(chart)
[
    {'rank' : ??, 'title' : ??, 'artist' : ??, 좋아요까지}
]

"""