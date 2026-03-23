import time
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from crawling.util import save_to_csv, analyze_word_frequency, save_frequency_to_csv

load_dotenv()

api_key = os.getenv("YOUTUBE_DATA_API_V3_KEY")
print("API_KEY:", api_key)
youtube = build("youtube", "v3", developerKey=api_key)


def youtube_api_crawl(query,
                      save_path="static/sports_spoiler_detection_data",
                      total_needed=100,
                      initial_id=0):
    all_items_count = initial_id
    next_page_token = None
    target_total = initial_id + total_needed

    # CSV 파일 경로는 저장 폴더 내에 생성
    csv_log_path = os.path.join(save_path, "video_metadata.csv")

    while all_items_count < target_total:
        fetch_count = min(50, target_total - all_items_count)

        request = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=fetch_count,
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()
        items = response.get("items", [])


        for item in items:
            video_id = item.get("id", {}).get("videoId")
            video_title = item.get("snippet", {}).get("title")  # 제목 추출

            if not video_id:
                continue

            all_items_count += 1
            # file_path = os.path.join(save_path, f"{all_items_count}_{video_id}.jpg")

            # 썸네일 URL 설정 및 이미지 저장
            thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            # if not save_image(thumb_url, file_path):
            #     thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            #     save_image(thumb_url, file_path)

            # 2. CSV에 데이터 기록 (제목과 썸네일 URL)
            save_to_csv(csv_log_path, video_title, thumb_url)

            if all_items_count >= target_total:
                break

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return all_items_count

def test():
    total_time = 0.
    cur_time = time.time()
    items_size = youtube_api_crawl(query='soccer highlight',
                                   save_path="static/sports_spoiler_detection_data",
                                   total_needed=10,
                                   initial_id=10)
    end_time = time.time()

    duration = end_time - cur_time
    if items_size and items_size > 0:
        avg_time = duration / items_size
        print(f"\n총 {items_size}개를 처리하는 데 {duration:.4f}초가 걸렸습니다.")
        print(f"개당 평균 {avg_time:.4f}s 의 시간이 걸렸습니다.")

if __name__ == "__main__":
    search_list = [
        "Soccer match highlights", "Premier League goals today", "Champions League full highlights",
        "La Liga match results", "Bundesliga weekly goals", "Serie A highlights 2026",
        "Last minute winning goal soccer", "All goals and highlights today", "Extended match highlights",
        "Penalty shootout highlights", "Hat-trick goals video", "Every goal this weekend",
        "Soccer match replay full", "Final score highlights", "Comeback victory soccer",
        "Shock defeat highlights", "Best goals of the month", "Top saves this week soccer",
        "Full time match review", "Goal of the season contender", "Matchday roundup football",
        "Weekly football recap", "Sudden death penalty soccer", "Injury time goals highlights",
        "Own goal highlights soccer", "EPL matchday results", "Champions League RO16 highlights",
        "Europa League goals today", "FA Cup match highlights", "World Cup Qualifiers goals",
        "Asian Cup match results", "K League match highlights", "MLS weekly highlights",
        "Ligue 1 goals and results", "Carabao Cup highlights", "Nations League soccer goals",
        "Copa America highlights", "Euro 2024 classic highlights", "Club World Cup results",
        "Transfer window official news", "League table update today", "Relegation battle soccer",
        "Title race highlights", "Derby match highlights", "El Clasico highlights 2026",
        "Post-match reaction soccer", "Football breaking news today", "Manager interview after match",
        "Player ratings after game", "Press conference highlights soccer", "Match analysis and reaction",
        "Starting XI news today", "Injury update soccer news", "Transfer rumors confirmed",
        "Here we go transfer news", "Football debate live", "Match preview vs prediction",
        "VAR controversy highlights", "Red card incident video", "Fan reaction at the stadium",
        "Watchalong soccer live", "Angry fan reaction soccer", "Pitch invader highlights",
        "Referee decision analysis", "Dressing room celebration video", "Soccer tactical analysis",
        "Formation breakdown football", "High press tactics explained", "Tiki-taka tactical review",
        "Counter attack goals analysis", "Defensive organization soccer", "Set piece routine analysis",
        "Build up play football", "Scouting report young player", "Player performance analysis",
        "Midfield masterclass video", "False 9 tactics analysis", "Gegenpressing tactical review",
        "Wing back roles analysis", "Football coaching points", "Son Heung-min goals today",
        "Erling Haaland hat-trick", "Kylian Mbappe speed highlights", "Lionel Messi inter miami goals",
        "Cristiano Ronaldo Al Nassr goals", "Jude Bellingham performance", "Vinicius Jr skills video",
        "Kevin De Bruyne assists", "Best solo goals soccer", "Top 50 football skills",
        "Iconic football moments", "Legendary goals history", "Football career tribute",
        "Best free kicks of all time", "Long range goals soccer", "Dribbling skills compilation",
        "Goalkeeper save compilation", "Defensive tackles highlights", "Nutmeg skills soccer",
        "Football legends highlights"
    ]

    # Crawling Meta Data
    # for search in search_list:
    #     try:
    #         items_size = youtube_api_crawl(query=search,
    #                                        save_path=f"static/sports_spoiler_detection_data/{search}",
    #                                        total_needed=50)
    #     except HttpError as e:
    #         if e.resp.status == 403:
    #             print("💡 할당량 초과, 현재까지의 데이터를 저장하고 종료합니다.")
    #             exit()

    # Analysis Frequency
    # frequency_dict = analyze_word_frequency(search_list)
    # sorted_freq = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    # save_frequency_to_csv(sorted_freq)

    import csv
    with open('static/analyze_word_frequency.csv', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        # 'Frequency' 컬럼의 값을 정수로 변환하여 모두 더함
        total_word_count = sum(int(row['Frequency']) for row in reader)

    print(f"전체 단어 빈도수 합계: {total_word_count}")