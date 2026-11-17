import logging

import pytest

from load_scores import load_scores


def write_csv(tmp_path, content):
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_정상_데이터의_순서와_중복을_유지한다(tmp_path):
    path = write_csv(
        tmp_path,
        "name,score\n민수,90\n지연,85\n민수,70\n",
    )

    assert load_scores(path) == [("민수", 90), ("지연", 85), ("민수", 70)]


def test_정상_데이터가_없으면_빈_목록을_반환한다(tmp_path):
    path = write_csv(tmp_path, "name,score\n")

    assert load_scores(path) == []


def test_파일이_없으면_FileNotFoundError를_발생시킨다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize("header", ["score,name", "name", "name,score,extra"])
def test_잘못된_헤더면_ValueError를_발생시킨다(tmp_path, header):
    path = write_csv(tmp_path, f"{header}\n민수,90\n")

    with pytest.raises(ValueError):
        load_scores(path)


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        ("0", [("민수", 0)]),
        ("100", [("민수", 100)]),
        ("-1", []),
        ("101", []),
        ("abc", []),
        ("1.5", []),
        ("", []),
        ("   ", []),
    ],
)
def test_점수_유효성_및_경계값(tmp_path, score, expected):
    path = write_csv(tmp_path, f"name,score\n민수,{score}\n")

    assert load_scores(path) == expected


def test_잘못된_행은_건너뛰고_정상_데이터와_경고를_유지한다(
    tmp_path, caplog
):
    path = write_csv(
        tmp_path,
        "name,score\n"
        "정상,100\n"
        "열부족\n"
        "열초과,80,비고\n"
        ",80\n"
        "점수없음,\n"
        "공백점수,   \n"
        "문자점수,abc\n"
        "하한미만,-1\n"
        "상한초과,101\n"
        "마지막,0\n",
    )

    with caplog.at_level(logging.WARNING):
        result = load_scores(path)

    assert result == [("정상", 100), ("마지막", 0)]

    warning_messages = [record.getMessage() for record in caplog.records]
    assert len(warning_messages) == 8
    for line_number in range(3, 11):
        assert any(str(line_number) in message for message in warning_messages)