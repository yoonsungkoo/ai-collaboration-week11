
# CSV 성적 처리 프로그램 테스트

## ① What — 무엇을 하는 프로그램인가?
CSV 파일에서 학생 이름과 점수를 읽어 유효한 데이터와 건너뛴 데이터를 구분하는 프로그램이다.

## ② Why — 왜 만들었는가?
[작성표 ②에서 직접 작성한 Why 내용을 여기에 옮겨 적기]

## ③ How — 설치 및 실행 방법

### 필요한 프로그램
- Python 3.14
- pytest 9.2.0
- pytest-cov 7.1.0

### 설치 명령어
```powershell
python -m pip install pytest pytest-cov
```

### 프로그램 실행
```powershell
python load_scores.py scores.csv
```

## ④ 테스트 — pytest 실행 방법과 결과

### 직접 작성한 테스트
```powershell
python -m pytest test_load_scores.py -v
```

실행 결과: 12 passed

### 코드 커버리지 확인
```powershell
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
```

실행 결과: 커버리지 80%

### AI 테스트 비교 결과

| 구분 | 통과 | 실패 | 커버리지 |
|---|---:|---:|---:|
| 직접 작성 | 12 | 0 | 80% |
| AI 실험 A | 18 | 0 | 80% |
| AI 실험 B | 1 | 14 | 78% |

AI 실험 B의 실패는 제공한 명세와 현재 구현의 차이가 영향을 주었다.

### 테스트 실행 화면
[pytest 테스트 통과 결과](pytest_result.png)

## ⑤ 파일 구성 — 각 파일의 역할

- `load_scores.py`: CSV 성적 처리 프로그램
- `test_load_scores.py`: 직접 작성한 단위 테스트
- `test_ai_A.py`: 구현 코드를 제공해 생성한 AI 테스트
- `test_ai_B.py`: 명세를 제공해 생성한 AI 테스트
- `bug3_logic.py`: 논리 오류가 포함된 실험용 코드
- `test_bug3_logic.py`: 논리 오류 검출을 위한 AI 테스트
- `README.md`: 프로젝트 설명 문서
- `LICENSE`: 라이선스
- `prompts.txt`: 실습 프롬프트 자료

## ⑥ 만든 사람

- 이름: [구윤성]
- 학번: [2026101046]
- AI 사용 도구: GitHub Copilot
- AI 사용 위치: `test_ai_A.py`, `test_ai_B.py`, `test_bug3_logic.py` 테스트 생성
