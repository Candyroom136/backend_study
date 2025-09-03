import pytest


def pytest_addoption(parser):
    """커스텀 명령행 옵션 추가"""
    parser.addoption(
        "--fast",
        action="store_true",
        default=False,
        help="빠른 테스트 실행 (느린 테스트 스킵)"
    )


def pytest_collection_modifyitems(config, items):
    """테스트 수집 후 자동 마킹"""
    for item in items:
        # 특정 조건에 따라 스킵
        if "slow" in item.keywords and config.getoption("--fast"):
            item.add_marker(pytest.mark.skip(reason="--fast 옵션으로 스킵"))