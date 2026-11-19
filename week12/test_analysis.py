import pandas as pd
from analysis import 정제, 반별평균

# 원본 데이터와 mini.csv를 정제
본 = 정제(pd.read_csv("scores_2026.csv"))
미니 = 정제(pd.read_csv("mini.csv"))


# 테스트 ① 정제 후 100행이 남는지 확인
def test_정제하면_100행이_남는다():
    assert len(본) == 100


# 테스트 ② 반 이름이 1반과 2반만 남는지 확인
def test_반은_두_종류만_남는다():
    assert sorted(본["반"].unique()) == ["1반", "2반"]


# 테스트 ③ 그룹별 합계와 전체 합계가 같은지 확인
def test_그룹합이_전체합과_같다():
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()


# 테스트 ④ mini.csv의 1반 평균이 80점인지 확인
def test_손계산과_일치한다():
    assert 반별평균(미니)["1반"] == 80.0