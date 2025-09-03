from fastapi import FastAPI, HTTPException

app = FastAPI()

users_db = [
    {"id": 1, "name": "김철수", "email": "kim@example.com"},
    {"id": 2, "name": "이영희", "email": "lee@example.com"}
]

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

@app.post("/users")
async def create_user(user: dict):
    new_id = max(u["id"] for u in users_db) + 1
    new_user = {"id": new_id, **user}
    users_db.append(new_user)
    return new_user

@app.get("/users")
async def get_users():
    return users_db