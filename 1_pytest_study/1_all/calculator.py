async def add(a, b):
    return a + b

async def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

async def multiply(a, b):
    return a * b
