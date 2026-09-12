nums = [3, 1, 2, 3, 4, 1, 2]

# 方法一：
result1 = []
for num in nums:
    if num not in result1:
        result1.append(num)

# 方法二：
result2 = list(dict.fromkeys(nums))

# 方法三：
result3 = []
seen = set()
for num in nums:
    if num not in seen:
        seen.add(num)
        result3.append(num)

print("方法一 :", result1)
print("方法二 :", result2)
print("方法三 :", result3)
