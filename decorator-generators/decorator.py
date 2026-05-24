# Decorators is a fucntion that takes another function as an argument and extends the behavior of the latter function without explicitly modifying it.
# Mean without changin code of latter fucntion addd something into it.


def decorator(func):
    def wrapper():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return wrapper

@decorator
def say_hello():
    print("Hello!")


s = decorator(say_hello)
s()

# s()
# │
# ├── outer wrapper
# │   ├── print Before
# │   ├── call inner wrapper
# │   │    ├── print Before
# │   │    ├── Hello!
# │   │    ├── print After
# │   │
# │   ├── print After

