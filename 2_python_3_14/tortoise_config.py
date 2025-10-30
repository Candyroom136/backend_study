"""
Tortoise ORM 설정 (DB Trigger 테스트용)
"""

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://triggeruser:triggerpass@localhost:5434/triggerdb"
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
