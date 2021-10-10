import requests
from bs4 import BeautifulSoup
import os
import constants

def nt_notify():
    with requests.get("https://newtoki107.com/toki_free", headers=constants.headers) as req:
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.select("#list-body > li")
        for i in range(1, 10):
            if posts[i].select("div.wr-num.hidden-xs")[0].text not in ["", "*"]:
                constants.latest_number = i
                break
        number = posts[constants.latest_number].select("div.wr-num.hidden-xs")[0].text
        time = posts[constants.latest_number].select("div.wr-date.hidden-xs")[0].text[1:].rstrip()
        downloads = posts[constants.latest_number].select("div.wr-down.hidden-xs")[0].text[1:].rstrip()
        title = posts[constants.latest_number].select("div.wr-subject > a")[0].text[9:-3].replace("	", "").lstrip().rstrip()
        member = posts[constants.latest_number].select("div.wr-name.hidden-xs > a > span")[0].text.lstrip()
        category = posts[constants.latest_number].select("div.wr-subject > a > span.tack-icon")[0].text
        link = posts[constants.latest_number].select("div.wr-subject > a")[0]['href']

        print(title)

        print("첫번째:", number, time, downloads, title, member, category, link)

        with open(os.path.join(constants.BASE_DIR, 'latest.txt'), 'r+') as f_read:
            before_number = f_read.readline()
            if before_number != number:
                with open(os.path.join(constants.BASE_DIR, "latest.txt"), "w+") as f_write:
                    f_write.write(number)
                    f_write.close()

                if before_number <= number:
                    print(number, "번째", "새 글이 올라옴", "|", "제목:", title)

                    if category == "공유" and not (time[-2] == '분' and int(time[:-2]) > 1):
                        constants.bot.sendMessage(constants.chat_id,
                                                  text=time + ": " + member + "님의 " + str(number) +
                                                       "번째 새 글이 올라왔어요!" + "\n" + "분류: 공유, " +  "다운로드 수" + ": " + downloads)
                        print(number, "번째", "새 공유탭 글이 올라옴")

            if 50 > int(downloads) > 0 and link not in constants.history and category != "공유":
                constants.history.insert(0, link)
                constants.history.pop()
                print(constants.history)
                constants.bot.sendMessage(constants.chat_id,
                                          text=time + ": " + member + "님의 "
                                               + str(number) + "번째 새 글이 올라왔어요!" + "\n" +
                                               "첫번째 글, " + "분류: " + category + ", " + "다운로드 수" + ": " + downloads
                                               + "\n" + "제목: " + title)
                print(number, "번째", "새 공유탭에 없는 공유글이 올라옴(1번째글)", "분류: ", category)

            number = posts[constants.latest_number+1].select("div.wr-num.hidden-xs")[0].text
            time = posts[constants.latest_number+1].select("div.wr-date.hidden-xs")[0].text[1:].rstrip()
            downloads = posts[constants.latest_number+1].select("div.wr-down.hidden-xs")[0].text[1:].rstrip()
            title = posts[constants.latest_number+1].select("div.wr-subject > a")[0].text[9:-3].replace("	", "").lstrip().rstrip()
            member = posts[constants.latest_number+1].select("div.wr-name.hidden-xs > a > span")[0].text.lstrip()
            category = posts[constants.latest_number+1].select("div.wr-subject > a > span.tack-icon")[0].text
            link = posts[constants.latest_number+1].select("div.wr-subject > a")[0]['href']

            print("두번째:", number, time, downloads, title, member, category, link)

            if 50 > int(downloads) > 0 and link not in constants.history and category != "공유" and not (
                    time[-2] == '분' and int(time[:-2]) > 10):
                constants.history.insert(0, link)
                constants.history.pop()
                print(constants.history)
                constants.bot.sendMessage(constants.chat_id,
                                          text=time + ": " + member + "님의 "
                                               + str(number) + "번째 새 글이 올라왔어요!" + "\n" +
                                               "두번째 글, " + "분류: " + category + ", " + "다운로드 수" + ": " + downloads
                                               + "\n" + "제목: " + title)

                print(number, "번째", "새 공유탭에 없는 공유글이 올라옴(2번째글)", "분류: ", category)

def main():
    try:
        nt_notify()

    except requests.exceptions.ChunkedEncodingError:
        print("에러가 발생했습니다. (ChunkedEncodingError) 다시 연결하는 중...")

    except IndexError:
        if constants.server_state == 1:
            constants.errorcount += 1
        if constants.errorcount == 50:
            constants.bot.sendMessage(constants.chat_id,
                                      text="서버 오류/기타 문제 생김")
        constants.server_state = 1
        print("에러가 발생했습니다. (IndexError) 다시 연결하는 중...", constants.errorcount)

    else:
        if constants.server_state == 1:
            constants.errorcount = 0
            if constants.errorcount >= 50:
                constants.bot.sendMessage(constants.chat_id, text="서버 오류/기타 문제 해결됨")

        constants.server_state = 0
