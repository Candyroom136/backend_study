-- 테스트용 users 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 테스트 데이터 삽입
INSERT INTO users (username, password, email) VALUES
    ('admin', 'admin123', 'admin@example.com'),
    ('john', 'john456', 'john@example.com'),
    ('jane', 'jane789', 'jane@example.com');

-- 권한 설정
GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO testuser;
