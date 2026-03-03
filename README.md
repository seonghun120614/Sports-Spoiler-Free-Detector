

# 🚀 시작하기 (Environment Setup)

이 프로젝트는 빠르고 효율적인 패키지 관리를 위해 **uv**를 사용합니다.

## 1. uv 설치

본인의 운영체제에 맞는 명령어를 터미널에 입력하여 설치해 주세요.

### Windows (PowerShell)
```powershell
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

### macOS / Linux / WSL

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

---

## 2. 프로젝트 실행

설치가 완료되면 **터미널을 반드시 재시작**한 뒤, 프로젝트 폴더에서 아래 명령어를 입력하여 실행합니다.

```bash
uv run main.py
```

