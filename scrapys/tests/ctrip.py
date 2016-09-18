# a = raw_input()
# # a = [2,3,2,4]
# print len(a)
#
# a = list(a.replace(',',''))
#
# print a
# b = list()
#
# for i in a:
#     b.append(int(i))
#
# print b
#
# max_num = 0
# for i in range(0,len(b)):
#     for j in range(i,len(b)):
#         if max_num < b[j] - b[i]:
#             max_num = b[j] - b[i]
#
# print 'max:',max_num

n = int(raw_input('n:'))
print type(n)

con = list()
for i in range(0,n):
    a = raw_input('con[%s]:' %i)
    a = list(a.replace(',', ''))
    b = list()
    for i in a:
        b.append(int(i))
    con.append(b)

print con
