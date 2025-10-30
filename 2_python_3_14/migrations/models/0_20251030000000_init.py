from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);

-- DB Triggers 추가

-- 1. modified_at 자동 업데이트 트리거
CREATE OR REPLACE FUNCTION update_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_users_modified_at ON users;
CREATE TRIGGER set_users_modified_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_modified_at();

-- 2. 이메일 검증 트리거
CREATE OR REPLACE FUNCTION validate_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS validate_users_email ON users;
CREATE TRIGGER validate_users_email
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION validate_email();

-- 3. audit_logs 테이블 및 트리거
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_users_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (table_name, record_id, action, new_value)
    VALUES ('users', NEW.id, 'INSERT',
            'username: ' || NEW.username || ', email: ' || NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION audit_users_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (table_name, record_id, action, old_value, new_value)
    VALUES ('users', NEW.id, 'UPDATE',
            'email: ' || OLD.email,
            'email: ' || NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION audit_users_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (table_name, record_id, action, old_value)
    VALUES ('users', OLD.id, 'DELETE',
            'username: ' || OLD.username || ', email: ' || OLD.email);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_users_insert_trigger ON users;
CREATE TRIGGER audit_users_insert_trigger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION audit_users_insert();

DROP TRIGGER IF EXISTS audit_users_update_trigger ON users;
CREATE TRIGGER audit_users_update_trigger
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_users_update();

DROP TRIGGER IF EXISTS audit_users_delete_trigger ON users;
CREATE TRIGGER audit_users_delete_trigger
BEFORE DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_users_delete();
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlm1vmzAQx78K4lUmdVXL0gftHc0yNdOSTC3dplYVcsAhVoxNsVkbVfnu9RmIgTyomT"
    "a1kfIO/neH734H3D3bMQ8xFYc3Aqf2Z+vZZijG6qKmH1g2ShKjgiDRiGrHTHloBY2ETFEg"
    "lThGVGAlhVgEKUkk4UypLKMURB4oR8IiI2WMPGTYlzzCcqITubtXMmEhfsKivE2m/phgGt"
    "byJCGcrXVfzhKt9Zj8qh3htJEfcJrFzDgnMznhbOFNmAQ1wgynSGJ4vEwzSB+yK8osK8oz"
    "NS55ipWYEI9RRmWl3FcyCDgDfioboQuM4JSPznH7rH3+6bR9rlx0JgvlbJ6XZ2rPAzWBgW"
    "fPtR1JlHtojIYbtE1fL9HrTFC6Gl81pgFRpd6EWCLbRLEUDEbz6vwjjjF68ilmkZyo2+Oj"
    "ow3UfrpXnUv3qqW8PkA1XL3O+Us+KExObgO0BiWOEaHbcFwE7CZE5+TkFRCV11qI2laHGK"
    "QYSvaRXCb5RVkkifFqmvXIBtKwCD0sL94pYFVDOGR0VvxINvD1ev3utef2f0AlsRAPVCNy"
    "vS5YHK3OGmrrtNGKxUOsXz3v0oJb63Y46GqCXMgo1ScaP+/WhpxQJrnP+KOPwso/r1RLML"
    "XGqpFBVB1/09lG6L61b9panTzM4fG0MlFAGKFg+ojS0F+ycIev8102xU7cVBBDke4KsIUs"
    "i7XExSkJJqsWlsKycWVBxme/s+zQzvJHbZqQ0hajthKyH7YLkPBpbAGxcN9NgP9l5VMnSs"
    "xWDLRv18PBmjXFhDRA3jBV4F1IAnlgUSLk/fvEuoEiVF2bWSW8Vt/93eTa+T68aA4jeMCF"
    "Yvym42X+An/ay/4="
)
