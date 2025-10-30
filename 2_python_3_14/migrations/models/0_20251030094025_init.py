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
);"""


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
