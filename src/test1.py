import random

result = []
for i in range(100000):
    s = [random.choice("0123456789") for i in range(1)]

    t = [random.choice("012345679") for i in range(1)]

    m = [random.choice("0123456789") for i in range(1)]

    n = [random.choice("0123456789") for i in range(1)]

    tmp_num_str = '88' + s[0] + t[0] + m[0] + n[0]
    tmp_num = int(tmp_num_str)
    if tmp_num not in result and len(result) < 100:
        result.append(tmp_num)
    else:
        break
print(result)