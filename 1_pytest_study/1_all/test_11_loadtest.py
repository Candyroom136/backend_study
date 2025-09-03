import asyncio
import aiohttp
import pytest

@pytest.mark.asyncio
async def test_api_load():
    """동시 요청 부하 테스트"""
    async def make_request(session, url):
        async with session.get(url) as response:
            return response.status
    
    async with aiohttp.ClientSession() as session:
        # 100개 동시 요청
        tasks = [
            make_request(session, "http://localhost:8081/")
            for _ in range(100)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # 모든 요청이 성공했는지 확인
        success_count = sum(1 for status in results if status == 200)
        assert success_count >= 95  # 95% 이상 성공