import pytest
from models import User

@pytest.mark.asyncio
async def test_user_creation(db_setup):
    """사용자 생성 테스트"""
    # 사용자 생성
    user = await User.create(name="김철수", email="kim@test.com")
    
    # 검증
    saved_user = await User.filter(email="kim@test.com").first()
    assert saved_user is not None
    assert saved_user.name == "김철수"
    assert saved_user.id == user.id

@pytest.mark.asyncio
async def test_user_email_unique(db_setup):
    """이메일 중복 테스트"""
    # 첫 번째 사용자 생성
    await User.create(name="김철수", email="test@example.com")
    
    # 같은 이메일로 두 번째 사용자 생성 시도 (실패해야 함)
    with pytest.raises(Exception):  # 실제로는 IntegrityError 등
        await User.create(name="이영희", email="test@example.com")

@pytest.mark.asyncio
async def test_user_list(db_setup):
    """사용자 목록 조회 테스트"""
    # 여러 사용자 생성
    await User.create(name="김철수", email="kim@test.com")
    await User.create(name="이영희", email="lee@test.com")
    await User.create(name="박민수", email="park@test.com")
    
    # 전체 사용자 조회
    users = await User.all()
    assert len(users) == 3
    
    # 이름으로 검색
    kim_user = await User.filter(name="김철수").first()
    assert kim_user.email == "kim@test.com"
