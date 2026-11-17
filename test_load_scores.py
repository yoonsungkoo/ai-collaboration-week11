import pytest
from load_scores import load_scores

def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    
    
def test_빈_줄은_건너뛴다(tmp_path):
    # 테스트에 사용할 임시 CSV 파일 생성
    file = tmp_path / "빈줄.csv"

    # 학생 데이터 사이에 빈 줄 추가
    file.write_text(
        "name,score\n민수,90\n\n지연,85\n",
        encoding="utf-8"
    )

    # CSV 파일 읽기
    kept, skipped = load_scores(file)

    # 빈 줄을 제외한 학생 2명이 정상적으로 읽혔는지 확인
    assert kept == [("민수", 90), ("지연", 85)]

    # 빈 줄은 건너뛴 기록에도 남지 않아야 함
    assert skipped == []   
    
    
def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    # 테스트용 CSV 파일 생성
    file = tmp_path / "쉼표이름.csv"

    # 이름에 쉼표가 포함된 학생 데이터 작성
    file.write_text(
        'name,score\n"김,민수",90\n이지연,85\n',
        encoding="utf-8"
    )

    # CSV 파일 읽기
    kept, skipped = load_scores(file)

    # 쉼표가 포함된 이름이 정상적으로 처리되는지 확인
    assert kept == [("김,민수", 90), ("이지연", 85)]

    # 건너뛴 데이터가 없어야 함
    assert skipped == []   
    
    
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")  
        
def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")

    assert kept == []
    assert skipped == []     
    
@pytest.mark.parametrize("score, valid", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, score, valid):
    # 테스트용 CSV 파일 생성
    file = tmp_path / "경계값.csv"

    # 학생의 점수를 CSV 파일에 저장
    file.write_text(
        f"name,score\n민수,{score}\n",
        encoding="utf-8"
    )

    # CSV 파일 읽기
    kept, skipped = load_scores(file)

    # 유효한 점수인지 확인
    assert (len(kept) == 1) == valid

    # 잘못된 점수는 skipped에 기록되어야 함
    assert (len(skipped) == 1) == (not valid)         
    
def test_이름이_비어_있으면_건너뛴다(tmp_path):
    file = tmp_path / "이름없음.csv"

    file.write_text(
        "name,score\n,85\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == [(2, ",85", "이름이 비어 있음")]
    
    
    
@pytest.mark.parametrize("score, valid", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, score, valid):
    # 테스트용 CSV 파일 생성
    file = tmp_path / "경계값.csv"

    # 학생의 점수를 CSV 파일에 저장
    file.write_text(
        f"name,score\n민수,{score}\n",
        encoding="utf-8"
    )

    # CSV 파일 읽기
    kept, skipped = load_scores(file)

    # 유효한 점수인지 확인
    assert (len(kept) == 1) == valid

    # 잘못된 점수는 skipped에 기록되어야 함
    assert (len(skipped) == 1) == (not valid)