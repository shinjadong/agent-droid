# 🎯 Agent-Droid

> **OpenManus와 DroidRun을 통합한 AI 에이전트 자동화 프로젝트**

웹 리서치부터 모바일 앱 자동화까지, 하나의 자연어 명령으로 모든 것을 자동화합니다.

---

## 📋 프로젝트 개요

이 프로젝트는 두 개의 강력한 AI 에이전트 프레임워크를 통합합니다:

- **[OpenManus](https://github.com/FoundationAgents/OpenManus)**: 범용 AI 에이전트 프레임워크 (웹 자동화, 코드 실행, 파일 편집 등)
- **[DroidRun](https://github.com/droidrun/droidrun)**: 모바일 특화 AI 에이전트 (Android/iOS 자동화)

### 🎯 할 수 있는 것

```python
# 한 줄의 명령으로:
"구글에서 강남 맛집 검색하고, 정보 수집해서 블로그 글 작성한 다음, 
 네이버 블로그 모바일 앱으로 자동 발행해줘"

# 시스템이 자동으로:
1. 웹 브라우저 열어서 검색 ✅
2. 상위 블로그 크롤링 ✅
3. AI로 콘텐츠 생성 ✅
4. Android 기기로 네이버 블로그 앱 실행 ✅
5. 글 작성 및 발행 ✅
```

---

## 📚 문서

### 📖 완전 가이드 (3,173줄 상세 설명)

**[docs/project-complete-guide.md](./docs/project-complete-guide.md)** - 프로젝트의 모든 것을 담은 완벽한 가이드

**포함 내용:**
- ✅ OpenManus 완전 분석 (아키텍처, 클래스, 도구, 실행 흐름)
- ✅ DroidRun 완전 분석 (Manager, Executor, Reflection, ADB/Portal)
- ✅ 두 프로젝트 통합 전략 (DroidRunAdapter 구현)
- ✅ 실전 활용 가이드 (환경 설정, 예제 프로젝트, 문제 해결)
- ✅ 모든 전문 용어를 쉬운 비유와 메커니즘으로 설명
- ✅ 복사-붙여넣기 가능한 실제 코드

**특징:**
- 📖 초보자도 이해할 수 있는 쉬운 설명
- 🔧 전문가도 만족할 깊이 있는 기술 분석
- 💻 바로 실행 가능한 코드 예시
- 🎨 시각적 다이어그램 풍부

---

## 🚀 빠른 시작

### 1. 필수 요구사항

- Python 3.12+
- Android 기기 (또는 에뮬레이터) with ADB
- OpenAI/Anthropic API 키

### 2. 설치

```bash
# 1. OpenManus 설치
cd OpenManus
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
playwright install

# 2. DroidRun 설치
cd ../droidrun
pip install -e .

# 3. ADB 설치
# Mac: brew install android-platform-tools
# Ubuntu/WSL: sudo apt install android-tools-adb
```

### 3. 설정

```bash
# OpenManus 설정
cp OpenManus/config/config.example.toml OpenManus/config/config.toml
# config.toml에 API 키 입력
```

### 4. 실행

```python
# 웹 자동화
python OpenManus/main.py

# 모바일 자동화
droidrun "네이버 블로그 앱 열어서 글쓰기"

# 통합 자동화 (설정 후)
# 완전 가이드 참조: docs/project-complete-guide.md
```

---

## 📁 프로젝트 구조

```
agent/
├── docs/
│   ├── project-complete-guide.md  # 📖 완전 가이드 (3,173줄)
│   ├── chat-claude-1.md           # 초기 분석 문서
│   └── chat-claude-2.md           # 구현 계획 문서
│
├── OpenManus/                     # 범용 AI 에이전트
│   ├── app/
│   │   ├── agent/                 # 에이전트 코어
│   │   ├── tool/                  # 도구 모음
│   │   └── llm.py                 # LLM 클라이언트
│   ├── config/
│   └── main.py
│
└── droidrun/                      # 모바일 특화 에이전트
    ├── droidrun/
    │   ├── agent/                 # DroidAgent, Manager, Executor
    │   └── tools/                 # ADB, Portal
    └── setup.py
```

---

## 💡 예제 프로젝트

### 1. 일간 뉴스 자동 요약 & 전송

```python
# 매일 아침 뉴스를 자동으로 요약해서 카카오톡 전송
from app.agent.manus import Manus

agent = await Manus.create()
await agent.run("""
1. 네이버 뉴스에서 주요 뉴스 5개 수집
2. 각 뉴스를 50자로 요약
3. Android 카카오톡으로 나에게 전송
""")
```

### 2. 인스타그램 자동 포스팅

```python
# 여행 사진 + AI 생성 캡션으로 자동 포스팅
await agent.run("""
1. 이미지 분석: /path/to/photo.jpg
2. 감성적인 캡션 생성 (해시태그 10개 포함)
3. 인스타그램 앱으로 포스팅
""")
```

### 3. 블로그 자동화 (웹 리서치 + 모바일 발행)

```python
# 완전 자동화된 블로그 운영
await agent.run("""
1. 구글에서 "강남 맛집" 검색 및 정보 수집
2. 1500자 블로그 글 작성
3. 네이버 블로그 모바일 앱으로 발행
""")
```

더 많은 예제는 **[완전 가이드](./docs/project-complete-guide.md#54-실전-프로젝트-예시)** 참조

---

## 🛠️ 주요 기능

### OpenManus
- ✅ 웹 브라우저 자동화 (Playwright + LLM)
- ✅ Python 코드 실행
- ✅ 파일 편집 및 관리
- ✅ MCP (Model Context Protocol) 지원
- ✅ 다양한 LLM 지원 (GPT-4o, Claude, Gemini)
- ✅ ReAct 패러다임으로 단계적 사고

### DroidRun
- ✅ Android/iOS 네이티브 앱 제어
- ✅ Manager + Executor 이중 구조
- ✅ Reflection으로 실패에서 학습
- ✅ ADB + Portal 통합
- ✅ UI hierarchy 자동 분석
- ✅ LLM agnostic (모든 LLM 지원)

### 통합 시스템
- ✅ 웹과 모바일을 하나의 워크플로우로 연결
- ✅ 자연어 하나로 전체 자동화
- ✅ 앱별 가이드 문서 시스템
- ✅ 확장 가능한 도구 아키텍처

---

## 📈 성능

- **DroidRun**: AndroidWorld 벤치마크 43% 성공률 (1위)
- **OpenManus**: MetaGPT 팀이 3시간 만에 프로토타입 제작
- **통합**: 웹 리서치 → 콘텐츠 생성 → 모바일 발행까지 5분 이내

---

## 🤝 기여

이 프로젝트는 다음 오픈소스 프로젝트들을 기반으로 합니다:

- **OpenManus**: https://github.com/FoundationAgents/OpenManus
- **DroidRun**: https://github.com/droidrun/droidrun

버그 리포트, 기능 제안, PR 환영합니다!

---

## 📄 라이선스

MIT License

---

## 🔗 참고 자료

### OpenManus
- 공식 문서: https://github.com/FoundationAgents/OpenManus
- Discord: https://discord.gg/DYn29wFk9z
- 데모: https://huggingface.co/spaces/lyh-917/OpenManusDemo

### DroidRun
- 공식 문서: https://docs.droidrun.ai
- Discord: https://discord.gg/ZZbKEZZkwK
- 벤치마크: https://droidrun.ai/benchmark

### 관련 기술
- ReAct: https://react-lm.github.io/
- MCP: https://modelcontextprotocol.io/
- Browser-Use: https://github.com/browser-use/browser-use

---

**📖 더 자세한 내용은 [완전 가이드](./docs/project-complete-guide.md)를 참조하세요!**

---

Made with ❤️ for AI Agent Automation

