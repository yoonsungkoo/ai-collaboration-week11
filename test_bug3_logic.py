import pytest

from bug3_logic import count_pass, find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 95),
        ([10, 20, 30], 30),
        ([95, 85, 70, 60], 95),
        ([42], 42),
    ],
)
def test_find_max_점수_목록에서_최고점을_찾는다(scores, expected):
    assert find_max(scores) == expected


def test_find_max_빈_목록이면_IndexError가_발생한다():
    with pytest.raises(IndexError):
        find_max([])


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 4),
        ([70, 85, 95], 3),
        ([60, 60, 59], 2),
        ([], 0),
    ],
)
def test_count_pass_기본_cutoff_경계값을_포함해_센다(scores, expected):
    assert count_pass(scores) == expected


def test_count_pass_사용자_cutoff와_같은_점수도_합격으로_센다():
    assert count_pass([49, 50, 69, 70], cutoff=70) == 1
