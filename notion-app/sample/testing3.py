import re

length = 3
pattern = r'(.{%s})' % length
string = 'aerofijaerfoieajfroeifj aerfiuh\n aerfiuhaerifuha aerifuh'
print(len(string))
lst2 = [x for x in re.split(pattern, string) if x]
print(lst2)

def test_func(a: int, b: int) -> int:
    return a - b

print(test_func(b=2, a=1))


