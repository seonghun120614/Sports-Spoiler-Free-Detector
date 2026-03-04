

# 🚀 시작하기 (Environment Setup)

이 프로젝트는 빠르고 효율적인 패키지 관리를 위해 **uv**를 사용합니다.

## uv 설치

본인의 운영체제에 맞는 명령어를 터미널에 입력하여 설치해 주세요.

#### Windows (PowerShell)
```powershell
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

#### macOS / Linux / WSL

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

---

## 프로젝트 실행

설치가 완료되면 **터미널을 반드시 재시작**한 뒤, 프로젝트 폴더에서 아래 명령어를 입력하여 실행합니다.

```bash
uv run main.py
```

## IDE 세팅

IDE 가 uv 가상 환경을 읽지 못할 때가 있습니다. 다음 메뉴얼을 따라주세요.

1. IDE Setting
2. Search `Python > Interpreter`
3. Click Add Interpreter
4. Virtual Environment 가 있다면 선택 -> 이미 존재하는 가상환경을 선택하기 위해 Existing 라디오 버튼 클릭
5. 프로젝트 루트에 있는 (Mac OS) `.venv/bin/python` 혹은 (Window) `.venv/bin/python.exe` 을 찾아 선택

## uv 패키지 관리 기능

`pyproject.toml` 을 사용하면 `uv run (경로)` 가 먹히지 않을 때가 있다. 다음 명령어를 통해 루트 폴더 자체가 글로벌 모듈 경로로 등록되며, 이후에는 파일의 위치와 상관 없이 어디서 스크립트를 실행하든 루트 경로가 기준이 된다.

```bash
uv pip install -e .

uv run (python 파일 경로)
```