import math
import matplotlib.pyplot as plt
import numpy as np
import cv2

from dataclasses import dataclass, field
from feature_extractor.extractor import EntityExtractor

# COCO Keypoint Index 기준
KPT_MAP = {
    'L_SHOULDER': 5, 'R_SHOULDER': 6,
    'L_ELBOW': 7, 'R_ELBOW': 8,
    'L_HIP': 11, 'R_HIP': 12
}


@dataclass
class PoseDetector(EntityExtractor):
    model_id: str = field(default="yolov8n-pose.pt")  # yolo26l-pose.pt 대신 공식 모델명 예시 사용
    threshold: float = 0.25

    def __post_init__(self):
        from ultralytics import YOLO
        self._model = YOLO(self.model_id)

    def extract(self, path: str) -> list:
        return self._model(path, conf=self.threshold)

    def calculate_angle(self, p1: tuple, p2: tuple, p3: tuple) -> float:
        """
        세 점의 좌표를 기반으로 사잇각을 계산합니다.
        p2가 꼭짓점(Vertex)이 됩니다.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        # 역탄젠트(atan2)를 사용하여 두 선분이 x축과 이루는 각도를 각각 구한 뒤 차이를 계산
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        angle = abs(angle)

        # 내각을 구하기 위해 180도 이상일 경우 보정
        if angle > 180.0:
            angle = 360.0 - angle

        return angle

    def analyze_arm_angles(self, results) -> list[dict]:
        """
        추론 결과에서 키포인트를 추출해 양팔의 벌어짐 각도를 계산합니다.
        """
        angles_list = []

        # 키포인트가 탐지되지 않은 경우 빈 리스트 반환
        if not results[0].keypoints or results[0].keypoints.xy is None:
            return angles_list

        # results[0].keypoints.xy 형태: Tensor [사람 수, 17(키포인트 수), 2(x, y)]
        for kpts in results[0].keypoints.xy:
            kpts_np = kpts.cpu().numpy()

            # 좌표가 0으로 찍힌 경우(탐지 실패)를 위한 방어 로직
            if np.all(kpts_np[KPT_MAP['L_SHOULDER']] == 0):
                continue

            # 왼쪽 팔 (어깨가 꼭짓점)
            l_angle = self.calculate_angle(
                p1=kpts_np[KPT_MAP['L_HIP']],
                p2=kpts_np[KPT_MAP['L_SHOULDER']],
                p3=kpts_np[KPT_MAP['L_ELBOW']]
            )

            # 오른쪽 팔 (어깨가 꼭짓점)
            r_angle = self.calculate_angle(
                p1=kpts_np[KPT_MAP['R_HIP']],
                p2=kpts_np[KPT_MAP['R_SHOULDER']],
                p3=kpts_np[KPT_MAP['R_ELBOW']]
            )

            angles_list.append({
                "left_arm_angle": round(l_angle, 2),
                "right_arm_angle": round(r_angle, 2)
            })

        return angles_list


if __name__ == "__main__":
    path = "static/example_image.png"
    pose_extractor = PoseDetector()

    # 1. 모델 추론
    results = pose_extractor.extract(path)

    # 2. 각도 계산
    arm_angles = pose_extractor.analyze_arm_angles(results)

    # 3. 시각화 및 텍스트 오버레이
    # YOLO 기본 시각화 이미지를 BGR 형태로 가져옴
    annotated_image = results[0].plot()

    # 탐지된 바운딩 박스와 계산된 각도를 매칭하여 텍스트 렌더링
    if results[0].boxes and results[0].boxes.xyxy is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()

        for i, (angles, box) in enumerate(zip(arm_angles, boxes)):
            if not (angles['left_arm_angle'] > 90. and angles['right_arm_angle'] < 90.):
                continue
            # 바운딩 박스의 좌상단 좌표 (x1, y1)
            x1, y1, x2, y2 = map(int, box)

            # 출력할 텍스트 구성
            text = f"P{i + 1}: L({angles['left_arm_angle']}), R({angles['right_arm_angle']})"

            # 텍스트 배경(가독성 향상) 및 텍스트 추가
            cv2.putText(
                annotated_image,
                text,
                (x1, y1 - 20),  # 바운딩 박스 약간 위
                cv2.FONT_HERSHEY_SIMPLEX,
                1,  # 폰트 크기
                (0, 200, 0),  # BGR 색상
                2  # 선 두께
            )

    # BGR을 RGB로 변환하여 Matplotlib으로 출력
    annotated_image_rgb = annotated_image[..., ::-1]

    plt.figure(figsize=(10, 8))
    plt.imshow(annotated_image_rgb)
    plt.title("Pose Estimation with Arm Angles")
    plt.axis('off')
    plt.show()