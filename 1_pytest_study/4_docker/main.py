import os
from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
import asyncpg

app = FastAPI(title="User Service")

# 데이터베이스 연결 설정
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/testdb")

# 간단한 사용자 데이터 (실제로는 DB에서 가져옴)
users = [
    {"id": 1, "name": "김철수", "email": "kim@example.com"},
    {"id": 2, "name": "이영희", "email": "lee@example.com"},
    {"id": 3, "name": "박민수", "email": "park@example.com"}
]

@app.on_event("startup")
async def startup_event():
    """앱 시작 시 DB 연결 및 테이블 생성"""
    try:
        # DB 연결 테스트
        conn = await asyncpg.connect(DATABASE_URL)
        
        # 테이블 생성 (마이그레이션)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # 초기 데이터 삽입 (테스트용)
        await conn.execute('DELETE FROM users')  # 기존 데이터 정리
        for user in users:
            await conn.execute(
                'INSERT INTO users (id, name, email) VALUES ($1, $2, $3)',
                user["id"], user["name"], user["email"]
            )
        print(f"✅ 초기 데이터 {len(users)}개 삽입 완료")
        
        await conn.close()
        print(f"✅ 데이터베이스 연결 성공: {DATABASE_URL}")
        print("✅ 테이블 생성 및 초기 데이터 삽입 완료")
        
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        raise

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "service": "user-service", "database": "connected"}

@app.get("/")
async def root():
    return {"message": "User Service API", "database_url": DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else "masked"}

@app.get("/users")
async def get_users():
    """모든 사용자 조회 (실제 DB에서)"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        rows = await conn.fetch('SELECT id, name, email FROM users ORDER BY id')
        await conn.close()
        
        users = [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in rows]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """특정 사용자 조회"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        row = await conn.fetchrow('SELECT id, name, email FROM users WHERE id = $1', user_id)
        await conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"user": {"id": row["id"], "name": row["name"], "email": row["email"]}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/users")
async def create_user(user_data: dict):
    """사용자 생성"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # 현재 최대 ID 값 조회
        max_id = await conn.fetchval("SELECT COALESCE(MAX(id), 0) FROM users")
        next_id = max_id + 1
        
        # 명시적으로 ID를 지정하여 삽입
        row = await conn.fetchrow(
            'INSERT INTO users (id, name, email) VALUES ($1, $2, $3) RETURNING id, name, email',
            next_id, user_data["name"], user_data["email"]
        )
        await conn.close()
        
        return {"user": {"id": row["id"], "name": row["name"], "email": row["email"]}, "message": "User created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)