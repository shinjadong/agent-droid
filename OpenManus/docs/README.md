# OpenManus 문서

OpenManus 프레임워크의 전체 문서입니다.

## 문서 구조

```
docs/
├── index.mdx                 # 문서 메인 페이지
├── overview.mdx             # 프로젝트 개요
├── quickstart.mdx           # 빠른 시작 가이드
├── mint.json                # 문서 시스템 설정
├── concepts/                # 핵심 개념
│   ├── architecture.mdx     # 시스템 아키텍처
│   ├── agents.mdx          # 에이전트 시스템
│   ├── tools.mdx           # 도구 시스템
│   ├── memory.mdx          # 메모리 관리
│   ├── flows.mdx           # 워크플로우
│   └── sandbox.mdx         # 샌드박스 실행
├── features/                # 주요 기능
│   ├── mcp-integration.mdx  # MCP 통합
│   ├── browser-automation.mdx # 브라우저 자동화
│   ├── data-analysis.mdx   # 데이터 분석
│   ├── web-search.mdx      # 웹 검색
│   └── file-editing.mdx    # 파일 편집
├── guides/                  # 가이드
│   ├── getting-started.mdx  # 시작하기
│   ├── building-custom-agent.mdx # 커스텀 에이전트
│   └── multi-agent-workflows.mdx # 멀티 에이전트
└── api/                     # API 참조
    ├── agents.mdx          # Agents API
    ├── tools.mdx           # Tools API
    ├── flows.mdx           # Flows API
    ├── config.mdx          # Config API
    └── schema.mdx          # Schema API
```

## 문서 시스템

이 문서는 [Mintlify](https://mintlify.com) 문서 시스템을 사용합니다.

### 로컬에서 문서 보기

```bash
# Mintlify CLI 설치
npm i -g mintlify

# 문서 서버 실행
cd docs
mintlify dev
```

문서는 `http://localhost:3000`에서 확인할 수 있습니다.

## 문서 작성 가이드

### 파일 형식

모든 문서는 MDX(Markdown + JSX) 형식으로 작성됩니다.

### Frontmatter

각 문서 파일은 다음과 같은 frontmatter로 시작해야 합니다:

```mdx
---
title: '문서 제목'
description: '문서 설명'
---
```

### 코드 블록

코드 예제는 언어를 명시하여 작성합니다:

````mdx
```python
from app.agent.manus import Manus

agent = Manus()
result = await agent.run("작업 설명")
```
````

### 개념 설명 박스

핵심 개념을 설명할 때는 다음 형식을 사용합니다:

```mdx
## 📖 [개념 이름]

**정의**
> 개념의 정확한 정의

**쉬운 비유**
> 일상적인 비유로 설명

**메커니즘**
> 동작 원리 설명

**존재 이유**
> 왜 필요한가에 대한 설명
```

### 카드 그룹

관련 링크를 그룹화할 때:

```mdx
<CardGroup cols={2}>
  <Card title="제목" icon="아이콘" href="/경로">
    설명
  </Card>
  <Card title="제목" icon="아이콘" href="/경로">
    설명
  </Card>
</CardGroup>
```

### 탭

여러 옵션을 보여줄 때:

```mdx
<Tabs>
  <Tab title="옵션 1">
    내용 1
  </Tab>
  <Tab title="옵션 2">
    내용 2
  </Tab>
</Tabs>
```

### 단계별 가이드

```mdx
<Steps>
  <Step title="1단계">
    내용
  </Step>
  <Step title="2단계">
    내용
  </Step>
</Steps>
```

### 경고 및 팁

```mdx
<Warning>
경고 메시지
</Warning>

<Tip>
팁 메시지
</Tip>

<Info>
정보 메시지
</Info>
```

## 문서 기여하기

### 새 문서 추가

1. 적절한 카테고리 폴더에 `.mdx` 파일 생성
2. frontmatter 작성
3. 내용 작성
4. `mint.json`의 `navigation`에 추가

### 기존 문서 수정

1. 해당 `.mdx` 파일 수정
2. 변경 사항 확인
3. Pull Request 제출

## 스타일 가이드

### 코드 스타일

- Python 코드는 Black 포맷터 스타일 사용
- 들여쓰기는 4칸 공백
- 한 줄은 최대 88자

### 문서 스타일

- 명확하고 간결한 설명
- 실용적인 예제 포함
- 단계별 가이드 제공
- 한국어와 영어 기술 용어 병기

### 예제 코드

- 완전하고 실행 가능한 코드
- 주석으로 설명 추가
- 실제 사용 사례 반영

## 문서 배포

문서는 자동으로 배포됩니다:

1. `main` 브랜치에 변경사항 푸시
2. GitHub Actions가 자동으로 빌드
3. Mintlify 호스팅에 배포

## 문서 업데이트 체크리스트

새 기능 추가 시:

- [ ] 개념 문서 업데이트
- [ ] API 참조 추가/수정
- [ ] 사용 예제 작성
- [ ] 가이드 업데이트 (필요시)
- [ ] 빠른 시작 가이드 확인
- [ ] 변경사항 문서화

## 도움말

문서 작성에 도움이 필요하시면:

- [Mintlify 문서](https://mintlify.com/docs)
- [MDX 문법](https://mdxjs.com/)
- [GitHub Discussions](https://github.com/gpt-open/OpenManus/discussions)

## 라이선스

이 문서는 OpenManus 프로젝트의 일부로 MIT 라이선스 하에 배포됩니다.
