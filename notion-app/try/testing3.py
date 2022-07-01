import re

length = 3
pattern = r'(.{%s})' % length
string = 'aerofijaerfoieajfroeifj aerfiuh\n aerfiuhaerifuha aerifuh'
print(len(string))
lst2 = [x for x in re.split(pattern, string) if x]
print(lst2)