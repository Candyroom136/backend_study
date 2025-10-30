-- DB Trigger 테스트용 초기화 스크립트

-- users 테이블 생성 (modified_at 포함)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    modified_at TIMESTAMPTZ DEFAULT NOW()
);

-- 테스트 데이터 삽입
INSERT INTO users (username, email) VALUES
    ('admin', 'admin@example.com'),
    ('john', 'john@example.com'),
    ('jane', 'jane@example.com');

-- 권한 설정
GRANT ALL PRIVILEGES ON DATABASE triggerdb TO triggeruser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO triggeruser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO triggeruser;
