import requests
import time
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)
SAVE_FOLDER = "./youtube-api"

# [중요] 저장할 폴더가 없으면 생성하는 로직
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
    print(f"[log] 폴더 생성 완료: {SAVE_FOLDER}")

def save_image(image_url, file_path):
    """이미지 주소에서 파일을 다운로드하는 함수"""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print("[log] success")
            return True
        else:
            print("[log] failed")
            return False
    except:
        return False


def main(query, total_needed=100):
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
            save_path = os.path.join(SAVE_FOLDER, f"{video_id}.jpg")

            print(f"[log] save path: {save_path}")

            thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            if not save_image(thumb_url, save_path):
                thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                print("failed")
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
    items_size = main('Barcelona vs Atletico Madrid Goals', 30)
    end_time = time.time()

    duration = end_time - cur_time
    if items_size and items_size > 0:
        avg_time = duration / items_size
        print(f"\n총 {items_size}개를 처리하는 데 {duration:.4f}초가 걸렸습니다.")
        print(f"개당 평균 {avg_time:.4f}s 의 시간이 걸렸습니다.")