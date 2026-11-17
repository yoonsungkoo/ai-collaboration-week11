import pytest

from load_scores import load_scores


def test_정상_파일과_공백을_읽는다(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n 민수 , 90 \n지연,85\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90), ("지연", 85)]
    assert skipped == []


def test_헤더만_있으면_빈_결과를_반환한다(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(file) == ([], [])


def test_없는_파일이면_FileNotFoundError를_올린다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("score", "expected_kept", "expected_skipped"),
    [
        ("0", [("민수", 0)], []),
        ("100", [("민수", 100)], []),
        ("-1", [], [(2, "민수,-1", "점수가 0~100 밖")]),
        ("101", [], [(2, "민수,101", "점수가 0~100 밖")]),
    ],
)
def test_점수_경계값(tmp_path, score, expected_kept, expected_skipped):
    file = tmp_path / "boundary.csv"
    file.write_text(f"name,score\n민수,{score}\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == expected_kept
    assert skipped == expected_skipped


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("민수", "열 개수가 2가 아님"),
        ("민수,90,추가", "열 개수가 2가 아님"),
        ("민수,", "점수가 비어 있음"),
        ("민수,abc", "점수가 정수가 아님"),
        ("민수,1.5", "점수가 정수가 아님"),
        ("민수,-1", "점수가 0~100 밖"),
        ("민수,101", "점수가 0~100 밖"),
        (",90", "이름이 비어 있음"),
    ],
)
def test_잘못된_행을_건너뛰고_기록한다(tmp_path, row, reason):
    file = tmp_path / "invalid.csv"
    file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == [(2, row, reason)]


def test_빈_줄은_기록하지_않고_줄번호를_유지한다(tmp_path):
    file = tmp_path / "blank.csv"
    file.write_text("name,score\n\n민수,90\n ,85\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90)]
    assert skipped == [(4, " ,85", "이름이 비어 있음")]


def test_동명이인을_모두_남긴다(tmp_path):
    file = tmp_path / "duplicates.csv"
    file.write_text("name,score\n민수,90\n민수,80\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90), ("민수", 80)]
    assert skipped == []


def test_utf8_bom이_있는_파일을_읽는다(tmp_path):
    file = tmp_path / "bom.csv"
    file.write_text("name,score\n민수,90\n", encoding="utf-8-sig")

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90)]
    assert skipped == []