import time
import os
from googleapiclient.discovery import build
from crawling.util import save_image

api_key = "AIzaSyCzt40eRU71D4BfA4TSNG4dowzTLUG0jpI"
youtube = build("youtube", "v3", developerKey=api_key)

def youtube_api_crawl(query,
                      save_path = "static/sports_spoiler_detection_data",
                      total_needed=100):
    all_items_count = 0
    next_page_token = None

    while all_items_count < total_needed:
        fetch_count = min(50, total_needed - all_items_count)

        request = youtube.search().list(
            q=query,
            part="id",
            maxResults=fetch_count,
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()
        items = response.get("items", [])

        for item in items:
            video_id = item.get("id", {}).get("videoId")

            if not video_id:
                continue

            all_items_count += 1
            save_path = os.path.join(save_path, f"{all_items_count}_{video_id}.jpg")

            thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            if not save_image(thumb_url, save_path):
                thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                save_image(thumb_url, save_path)

            # 목표 개수 도달 시 즉시 종료
            if all_items_count >= total_needed:
                break

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return all_items_count

if __name__ == "__main__":
    total_time = 0.

    cur_time = time.time()
    items_size = youtube_api_crawl(query='맨유',
                                   save_path="static/sports_spoiler_detection_data",
                                   total_needed=1)
    end_time = time.time()

    duration = end_time - cur_time
    if items_size and items_size > 0:
        avg_time = duration / items_size
        print(f"\n총 {items_size}개를 처리하는 데 {duration:.4f}초가 걸렸습니다.")
        print(f"개당 평균 {avg_time:.4f}s 의 시간이 걸렸습니다.")