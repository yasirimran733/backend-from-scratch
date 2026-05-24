# A generator is a function that returns an iterator.
# It is defined like a normal function but uses thr yield statement 
# to return a value. Each time the generator's next function is called, the generator resumes where it left off (it remembers all the data values and which statement was last executed). An example of a generator is:
def count():
    yield 1
    yield 2
    yield 3

#  Why generators are powerful

#  memory efficient
#  fast for large data
#  used in streaming APIs, logs, pipelines
#  backbone of async thinking
c = count()
print(next(c))
print(next(count()))
print(next(c))

# Output:
# 5
# 4
# 3

def demo():
    print("A")
    yield 1

    print("B")
    yield 2

g = demo()

print(next(g))
print(next(g))