import requests

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