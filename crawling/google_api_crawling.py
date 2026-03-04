import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from matplotlib import patches

def visualize_detections(image_path, results):
    # 1. 이미지 로드
    image = Image.open(image_path).convert("RGB")
    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(image)

    # 2. 결과 반복문 돌며 박스 그리기
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        # box: [xmin, ymin, xmax, ymax]
        xmin, ymin, xmax, ymax = box.tolist()

        # 박스 너비와 높이 계산
        width = xmax - xmin
        height = ymax - ymin

        # 사각형 패치 생성 (Edgecolor는 눈에 잘 띄는 lime 추천)
        rect = patches.Rectangle(
            (xmin, ymin), width, height,
            linewidth=2, edgecolor='lime', facecolor='none'
        )
        ax.add_patch(rect)

        # 라벨 및 신뢰도 표시
        plt.text(
            xmin, ymin - 5,
            f"{label}: {score:.2f}",
            color='white', fontweight='bold',
            bbox=dict(facecolor='lime', alpha=0.5)
        )

    plt.axis('off')
    plt.show()