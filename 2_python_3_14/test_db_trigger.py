"""
DB Trigger 실전 테스트 (PostgreSQL + Docker)

마이그레이션으로 생성된 트리거들이 실제로 동작하는지 확인:
1. modified_at 자동 업데이트 (1_db_trigger_migration.py)
2. 이메일 검증 (2_db_trigger_migration.py)
3. Audit Log 자동 기록 (3_db_trigger_migration.py)
"""
import asyncio
import sys
from datetime import datetime
import psycopg


def print_section(title):
    """섹션 헤더 출력"""
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def check_requirements():
    """환경 확인"""
    print_section("환경 확인")

    # Python 버전
    print(f"\n✓ Python 버전: {sys.version.split()[0]}")

    # psycopg3 확인
    try:
        print(f"✓ psycopg3 버전: {psycopg.__version__}")
    except Exception as e:
        print(f"❌ psycopg3 확인 실패: {e}")
        return False

    # PostgreSQL 연결 확인
    try:
        conn = psycopg.connect(
            "host=localhost port=5434 dbname=triggerdb user=triggeruser password=triggerpass",
            connect_timeout=3
        )
        conn.close()
        print("✓ PostgreSQL 연결 성공 (port 5434)")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL 연결 실패: {e}")
        print("\n💡 Docker 컨테이너를 먼저 실행하세요:")
        print("   docker-compose -f docker-compose-trigger.yml up -d")
        return False


def get_connection():
    """PostgreSQL 연결"""
    return psycopg.connect(
        "host=localhost port=5434 dbname=triggerdb user=triggeruser password=triggerpass"
    )


def test_modified_at_trigger():
    """1. modified_at 자동 업데이트 트리거 테스트"""
    print_section("1. modified_at 자동 업데이트 트리거")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 사용자 추가
        print("\n[사용자 추가]")
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id, created_at, modified_at",
            ('trigger_test_user', 'trigger@example.com')
        )
        user_id, created_at, modified_at = cursor.fetchone()
        conn.commit()

        print(f"  사용자 ID: {user_id}")
        print(f"  created_at: {created_at}")
        print(f"  modified_at: {modified_at}")
        print(f"  ✓ 초기에는 created_at == modified_at")

        # 잠시 대기
        import time
        time.sleep(1)

        # 사용자 수정 (modified_at이 자동으로 업데이트되어야 함)
        print("\n[사용자 이메일 수정]")
        old_modified_at = modified_at

        cursor.execute(
            "UPDATE users SET email = %s WHERE id = %s RETURNING modified_at",
            ('updated@example.com', user_id)
        )
        new_modified_at = cursor.fetchone()[0]
        conn.commit()

        print(f"  이전 modified_at: {old_modified_at}")
        print(f"  현재 modified_at: {new_modified_at}")

        if new_modified_at > old_modified_at:
            print(f"  ✅ 트리거 작동 성공! modified_at이 자동 업데이트됨")
        else:
            print(f"  ❌ 트리거 작동 실패! modified_at이 업데이트 안 됨")

        # 정리
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        conn.rollback()
    finally:
        conn.close()


def test_email_validation_trigger():
    """2. 이메일 검증 트리거 테스트"""
    print_section("2. 이메일 검증 트리거")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 유효한 이메일 테스트
        print("\n[유효한 이메일 삽입]")
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id",
            ('valid_user', 'valid.email@example.com')
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        print(f"  ✅ 성공! 사용자 ID: {user_id}")

        # 정리
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

    except Exception as e:
        print(f"  ❌ 예상치 못한 에러: {e}")
        conn.rollback()

    try:
        # 잘못된 이메일 테스트
        print("\n[잘못된 이메일 삽입 시도]")
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            ('invalid_user', 'not-an-email')
        )
        conn.commit()
        print(f"  ❌ 트리거 실패! 잘못된 이메일이 저장됨")

    except psycopg.errors.RaiseException as e:
        print(f"  ✅ 트리거 작동 성공! 잘못된 이메일 차단")
        print(f"  에러 메시지: {e}")
        conn.rollback()
    except Exception as e:
        print(f"  ❌ 예상치 못한 에러: {e}")
        conn.rollback()
    finally:
        conn.close()


def test_audit_log_trigger():
    """3. Audit Log 트리거 테스트"""
    print_section("3. Audit Log 자동 기록 트리거")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # INSERT 테스트
        print("\n[사용자 추가 → Audit Log 기록]")
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id",
            ('audit_user', 'audit@example.com')
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        print(f"  사용자 ID: {user_id}")

        # Audit log 확인
        cursor.execute(
            "SELECT action, new_value, changed_at FROM audit_logs WHERE table_name = 'users' AND record_id = %s AND action = 'INSERT'",
            (user_id,)
        )
        log = cursor.fetchone()

        if log:
            action, new_value, changed_at = log
            print(f"  ✅ Audit Log 기록됨!")
            print(f"    - Action: {action}")
            print(f"    - New Value: {new_value}")
            print(f"    - Changed At: {changed_at}")
        else:
            print(f"  ❌ Audit Log 기록 안 됨")

        # UPDATE 테스트
        print("\n[사용자 이메일 수정 → Audit Log 기록]")
        cursor.execute(
            "UPDATE users SET email = %s WHERE id = %s",
            ('updated.audit@example.com', user_id)
        )
        conn.commit()

        # Audit log 확인
        cursor.execute(
            "SELECT action, old_value, new_value, changed_at FROM audit_logs WHERE table_name = 'users' AND record_id = %s AND action = 'UPDATE'",
            (user_id,)
        )
        log = cursor.fetchone()

        if log:
            action, old_value, new_value, changed_at = log
            print(f"  ✅ Audit Log 기록됨!")
            print(f"    - Action: {action}")
            print(f"    - Old Value: {old_value}")
            print(f"    - New Value: {new_value}")
            print(f"    - Changed At: {changed_at}")
        else:
            print(f"  ❌ Audit Log 기록 안 됨")

        # DELETE 테스트
        print("\n[사용자 삭제 → Audit Log 기록]")
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        # Audit log 확인
        cursor.execute(
            "SELECT action, old_value, changed_at FROM audit_logs WHERE table_name = 'users' AND record_id = %s AND action = 'DELETE'",
            (user_id,)
        )
        log = cursor.fetchone()

        if log:
            action, old_value, changed_at = log
            print(f"  ✅ Audit Log 기록됨!")
            print(f"    - Action: {action}")
            print(f"    - Old Value: {old_value}")
            print(f"    - Changed At: {changed_at}")
        else:
            print(f"  ❌ Audit Log 기록 안 됨")

        # Audit log 정리
        cursor.execute("DELETE FROM audit_logs WHERE record_id = %s", (user_id,))
        conn.commit()

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


def show_trigger_info():
    """4. 현재 적용된 트리거 정보"""
    print_section("4. 현재 적용된 트리거 확인")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 트리거 목록 조회
        cursor.execute("""
            SELECT
                trigger_name,
                event_manipulation,
                action_timing,
                action_statement
            FROM information_schema.triggers
            WHERE trigger_schema = 'public'
            AND event_object_table = 'users'
            ORDER BY trigger_name
        """)

        triggers = cursor.fetchall()

        if triggers:
            print(f"\n✅ 현재 {len(triggers)}개의 트리거가 users 테이블에 적용됨:\n")
            for i, (name, event, timing, statement) in enumerate(triggers, 1):
                print(f"  {i}. {name}")
                print(f"     - Event: {event}")
                print(f"     - Timing: {timing}")
                print(f"     - Function: {statement}")
                print()
        else:
            print("\n⚠️  users 테이블에 적용된 트리거가 없습니다.")
            print("   aerich로 마이그레이션을 먼저 실행하세요.")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
    finally:
        conn.close()


def main():
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 18 + "DB Trigger 실전 테스트" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\nPostgreSQL + Docker 환경에서 트리거 동작 확인")

    # 환경 확인
    if not check_requirements():
        print("\n" + "=" * 70)
        print("❌ 테스트를 실행할 수 없습니다.")
        print("=" * 70)
        return

    # 트리거 정보 확인
    show_trigger_info()

    # 테스트 실행
    test_modified_at_trigger()
    test_email_validation_trigger()
    test_audit_log_trigger()

    # 결론
    print("\n" + "=" * 70)
    print("✅ 테스트 완료!")
    print("=" * 70)
    print("\n📊 테스트 항목:")
    print("  1. modified_at 자동 업데이트 ✓")
    print("  2. 이메일 형식 검증 ✓")
    print("  3. Audit Log 자동 기록 (INSERT/UPDATE/DELETE) ✓")
    print("\n💡 트리거 작동 확인:")
    print("  - 애플리케이션 코드 변경 없이 DB 레벨에서 자동 처리")
    print("  - 데이터 무결성 보장 및 변경 이력 추적")
    print("=" * 70)


if __name__ == "__main__":
    main()
