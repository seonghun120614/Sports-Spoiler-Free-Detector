import requests
import csv
import os
import re
from collections import Counter

def save_image(image_url, file_path):
    """이미지 주소에서 파일을 다운로드하는 함수"""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            return False
    except:
        return False


def save_to_csv(csv_path: str, title: str, img_url: str, local_path: str = "") -> bool:
    if not csv_path.lower().endswith(".csv"):
        csv_path += ".csv"

    dir_name = os.path.dirname(csv_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    file_exists = os.path.isfile(csv_path)
    try:
        with open(csv_path, mode='a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            if not file_exists:
                writer.writerow(["Title", "Image_URL", "Local_Path"])
            # 로컬 경로도 함께 저장하면 나중에 학습 데이터 매핑이 쉬워집니다.
            writer.writerow([title, img_url, local_path])
        return True
    except Exception as e:
        print(f"CSV 저장 오류: {e}")
        return False


def analyze_word_frequency(search_list, base_path="static/sports_spoiler_detection_data"):
    word_counts = Counter() # Counter 자료구조 사용

    for search in search_list:
        file_path = os.path.join(base_path, search, "video_metadata.csv")

        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get('Title', '')
                    if not title:
                        continue

                    # 1. 소문자 변환 및 특수문자 제거 (정규표현식)
                    # 알파벳과 숫자만 남기고 공백으로 대체
                    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())

                    # 2. 단어 분리 (Tokenization)
                    words = clean_title.split()

                    # 3. 빈도 업데이트
                    word_counts.update(words)

        except Exception as e:
            print(f"파일 읽기 오류 ({search}): {e}")

    return dict(word_counts)


def save_frequency_to_csv(data, file_path="static/analyze_word_frequency.csv"):
    """
    데이터(dict 또는 list)를 CSV 파일로 저장
    """
    # 폴더 생성 로직
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    # 만약 데이터가 딕셔너리라면 정렬을 수행하여 리스트로 변환
    if isinstance(data, dict):
        processed_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    else:
        processed_data = data

    try:
        with open(file_path, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Frequency"])
            writer.writerows(processed_data)  # 일괄 작성

        print(f"✅ 분석 결과 저장 완료: {file_path}")
        return True
    except Exception as e:
        print(f"❌ CSV 저장 중 오류 발생: {e}")
        return False