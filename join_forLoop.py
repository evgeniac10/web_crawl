# 100만 개의 요소를 가진 리스트
data = ["a"] * 1000000

# ''.join() 방식
import time
start = time.time()
result = ''.join(data)
print("join:", time.time() - start)

# 문자열 덧셈 방식
start = time.time()
result = ""
for i in data:
    result += i
print("loop:", time.time() - start)
