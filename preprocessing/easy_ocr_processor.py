import easyocr

def ocr_detect(image_path: str):
    reader = easyocr.Reader(['ko', 'en'])
    return reader.readtext(image_path)

# For Test
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2

    image_path = "static/example_image.png"

    result = ocr_detect(image_path)

    # 이미지 로드 (OpenCV)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 결과가 없을 경우 대비
    if not result:
        print("텍스트가 감지되지 않았습니다.")
        exit(0)

    # 결과 순회하며 이미지 위에 그리기
    for (bbox, text, prob) in result:
        # EasyOCR의 좌표 형태를 numpy 배열 정수형으로 변환
        pts = np.array(bbox, np.int32)

        # [옵션 A] 테두리만 그리기 (시각화 확인용)
        cv2.polylines(image, [pts], isClosed=True, color=(255, 0, 0), thickness=3)

        # [옵션 B] 스포일러 방지를 위해 영역 채우기 (마스킹)
        # 만약 특정 키워드만 가리고 싶다면: if "승" in text: 같은 조건문 추가
        # cv2.fillPoly(image, [pts], color=(0, 0, 0))

        print(f"Detected: {text} ({prob:.2f})")

    # 결과 출력
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.title(f"OCR Result: {image_path}")
    plt.axis('off')
    plt.show()