import pandas as pd


def 정제(df):
    # 원본 데이터를 변경하지 않도록 복사본 만들기
    df = df.copy()
    print("시작:", len(df))

    # 1단계: 점수가 비어 있는 행 삭제
    df = df.dropna(subset=["점수"])
    print("빈칸 제거 후:", len(df))

    # 2단계: 모든 열이 완전히 같은 중복 행 삭제
    df = df.drop_duplicates()
    print("중복 제거 후:", len(df))

    # 3단계: 반과 과목 이름의 앞뒤 공백 제거
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거 후:", len(df))

    # 4단계: 점수가 0~100 범위를 벗어난 행 삭제
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거 후:", len(df))

    return df


# CSV 파일 불러오기
df = pd.read_csv("scores_2026.csv")

# 데이터 정제 함수 실행
clean_df = 정제(df)
# STEP 3-① 필터링

# 1. 수학 과목인 행만 선택
math_df = clean_df[clean_df["과목"] == "수학"]
print("수학 과목 행 수:", len(math_df))

# 2. 1반이면서 90점 이상인 행만 선택
high_df = clean_df[
    (clean_df["반"] == "1반") & (clean_df["점수"] >= 90)
]
print("1반 90점 이상 행 수:", len(high_df))
# STEP 3-② 그룹화

# 1. 반별 평균 점수 계산
class_mean = clean_df.groupby("반")["점수"].mean()
print("반별 평균 점수:")
print(class_mean)

# 2. 과목별·반별 평균 점수 계산
subject_class_mean = clean_df.groupby(["과목", "반"])["점수"].mean()
print("과목별·반별 평균 점수:")
print(subject_class_mean)
# STEP 3-③ 통계 분석

# 반별 개수, 평균, 중앙값, 최댓값을 한 표로 계산
class_stats = clean_df.groupby("반")["점수"].agg(
    ["count", "mean", "median", "max"]
).round(2)

print("반별 통계:")
print(class_stats)


# 반별 평균을 반환하는 함수
def 반별평균(df):
    return df.groupby("반")["점수"].mean().round(2)
# STEP 3 검증 ②: 합계와 개수 일치 확인

# 반별 점수 합계를 다시 합한 값
group_sum = clean_df.groupby("반")["점수"].sum().sum()

# 전체 데이터의 점수 합계
total_sum = clean_df["점수"].sum()

print("그룹별 점수 합계:", group_sum)
print("전체 점수 합계:", total_sum)

# 반별 데이터 개수를 다시 합한 값
group_count = clean_df.groupby("반")["점수"].count().sum()

# 전체 데이터 개수
total_count = len(clean_df)

print("그룹별 데이터 개수:", group_count)
print("전체 데이터 개수:", total_count)
# 검증 ④: 1반 수학 점수 스팟 체크
check_scores = clean_df[
    (clean_df["반"] == "1반") &
    (clean_df["과목"] == "수학")
]["점수"]

print("1반 수학 점수:")
print(check_scores.to_list())

print("1반 수학 데이터 개수:", len(check_scores))
print("1반 수학 점수 합계:", check_scores.sum())
print("1반 수학 평균:", check_scores.mean())
# STEP 4: mini.csv 손계산 결과 검증

# mini.csv 파일 불러오기
mini_df = pd.read_csv("mini.csv")

# 기존 정제 함수로 데이터 정제
mini_clean = 정제(mini_df)

# 정제 후 행 수 확인
print("mini.csv 정제 후 행 수:", len(mini_clean))

# 반별 평균 계산
mini_mean = 반별평균(mini_clean)

print("mini.csv 반별 평균:")
print(mini_mean)