"""
t-string 실전 테스트 (PostgreSQL + psycopg3)

Python 3.14의 t-string을 psycopg 3.3.0.dev1로 테스트
SQL Injection 방어 및 안전한 쿼리 실행 확인
"""

import sys


def print_section(title):
    """섹션 헤더 출력"""
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def check_requirements():
    """필수 요구사항 확인"""
    print_section("환경 확인")

    # Python 버전 확인
    print(f"\n✓ Python 버전: {sys.version.split()[0]}")

    if sys.version_info < (3, 14):
        print(f"⚠️  t-string은 Python 3.14+에서만 사용 가능")
        return False

    # psycopg3 확인
    try:
        import psycopg

        print(f"✓ psycopg3 버전: {psycopg.__version__}")
    except ImportError:
        print("❌ psycopg3가 설치되지 않았습니다.")
        return False

    # PostgreSQL 연결 확인
    try:
        conn = psycopg.connect(
            "host=localhost port=5433 dbname=testdb user=testuser password=testpass",
            connect_timeout=3,
        )
        conn.close()
        print("✓ PostgreSQL 연결 성공")
    except Exception as e:
        print(f"❌ PostgreSQL 연결 실패: {e}")
        return False

    return True


def test_sql_injection_comparison():
    """1. SQL Injection 비교 (f-string vs parameterized)"""
    print_section("1. SQL Injection 공격 비교")

    import psycopg

    conn = psycopg.connect(
        "host=localhost port=5433 dbname=testdb user=testuser password=testpass"
    )

    malicious_username = "admin' OR '1'='1"
    malicious_password = "anything"

    # f-string 방식 (취약!)
    print("\n[❌ f-string 방식 - 공격 성공]")
    print(f'  악의적 입력: username="{malicious_username}"')

    query = f"SELECT id, username, email FROM users WHERE username = '{malicious_username}' AND password = '{malicious_password}'"
    print(f"  실제 쿼리: {query}")

    cursor = conn.execute(query)
    results = cursor.fetchall()

    print(f"  결과: 💀 공격 성공! {len(results)}명의 사용자 정보 유출:")
    for row in results:
        print(f"    - {row[1]} ({row[2]})")

    print("\n" + "-" * 70)

    # Parameterized query (안전!)
    print("\n[✅ Parameterized Query - 공격 차단]")
    print(f'  악의적 입력: username="{malicious_username}"')
    print(f"  쿼리: SELECT ... WHERE username = %s AND password = %s")
    print(f"  파라미터: ['{malicious_username}', '{malicious_password}']")

    cursor = conn.execute(
        "SELECT id, username, email FROM users WHERE username = %s AND password = %s",
        (malicious_username, malicious_password),
    )
    result = cursor.fetchone()

    if result:
        print(f"  결과: 로그인 성공 - {result[1]}")
    else:
        print(f"  결과: ✅ 공격 차단! 로그인 실패")

    conn.close()


def test_tstring_template_structure():
    """2. t-string Template 구조 분석"""
    print_section("2. t-string Template 구조 분석")

    username = "admin' OR '1'='1"
    password = "test123"

    # t-string Template 생성
    print(f"\n[t-string Template 생성]")
    print(f'  코드: t"SELECT * FROM users WHERE username = {{username}}..."')

    template = (
        t"SELECT * FROM users WHERE username = {username} AND password = {password}"
    )

    print(f"\n[Template 객체 정보]")
    print(f"  타입: {type(template)}")
    print(f"  repr: {template!r}")

    print(f"\n[Template 내부 구조 - 파싱 결과]")
    from string.templatelib import Interpolation

    strings_part = []
    variables_part = []

    for i, part in enumerate(template):
        if isinstance(part, str):
            strings_part.append(part)
            print(f"  [{i}] 📝 문자열: {part!r}")
        elif isinstance(part, Interpolation):
            variables_part.append(part)
            # Interpolation 객체의 실제 속성 사용
            print(f"  [{i}] 🔢 변수: {part.value!r}")

    print(f"\n[라이브러리가 변환하는 방식 (이론)]")
    print(f"  1️⃣  문자열 부분 추출:")
    print(f"      'SELECT * FROM users WHERE username = ' + ' AND password = '")
    print(f"\n  2️⃣  플레이스홀더로 대체:")
    print(f"      'SELECT * FROM users WHERE username = $1 AND password = $2'")
    print(f"\n  3️⃣  파라미터 분리:")
    print(f"      params = ['{username}', '{password}']")
    print(f"\n  4️⃣  안전한 실행:")
    print(f"      PostgreSQL이 SQL과 파라미터를 분리하여 처리")
    print(f"      → SQL Injection 차단!")




def test_tstring_with_psycopg():
    """3. t-string으로 SQL Injection 방어"""
    print_section("3. t-string으로 SQL Injection 방어")

    import psycopg

    conn = psycopg.connect(
        "host=localhost port=5433 dbname=testdb user=testuser password=testpass"
    )

    username = "admin' OR '1'='1"
    password = "test123"

    print(f"\n[t-string 사용]")
    print(f"  악의적 입력: username=\"{username}\"")
    print(f'  코드: cursor.execute(t"SELECT ... WHERE username = {{username}}...")')

    # t-string Template을 psycopg에 직접 전달
    cursor = conn.execute(
        t"SELECT id, username, email FROM users WHERE username = {username} AND password = {password}"
    )
    result = cursor.fetchone()

    print(f"\n[실행 결과]")
    if result:
        print(f"  결과: 로그인 성공 - {result[1]}")
    else:
        print(f"  결과: ✅ 공격 차단! (SQL Injection 방어 성공)")

    print(f"\n[💡 작동 원리]")
    print(f"  - psycopg가 Template 객체를 받아 자동으로 SQL과 파라미터 분리")
    print(f"  - 내부적으로 Parameterized Query로 변환하여 안전하게 실행")
    print(f"  - 개발자는 간단히 t\"...\"만 사용하면 됨!")

    conn.close()


def main():
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "t-string 실전 테스트 (psycopg 3.3)" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")

    # 환경 확인
    if not check_requirements():
        print("\n" + "=" * 70)
        print("❌ 테스트를 실행할 수 없습니다.")
        print("=" * 70)
        return

    # 테스트 실행
    try:
        test_sql_injection_comparison()
        test_tstring_template_structure()
        test_tstring_with_psycopg()

        # 결론
        print("\n" + "=" * 70)
        print("✅ 테스트 완료!")
        print("=" * 70)
        print("\n📊 핵심 정리:")
        print("  1. f-string: SQL Injection에 취약 ❌")
        print("  2. Parameterized Query: 안전하지만 가독성 낮음")
        print("  3. t-string: 안전하면서 가독성 높음 ✅")
        print("\n💡 t-string 장점:")
        print("  - 자동 SQL Injection 방어")
        print("  - f-string처럼 직관적인 문법")
        print("  - psycopg가 자동으로 안전하게 처리")
        print("\n🚀 사용법:")
        print('  cursor.execute(t"SELECT * FROM users WHERE id = {user_id}")')
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
