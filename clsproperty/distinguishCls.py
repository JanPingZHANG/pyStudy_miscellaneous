class A:                                                                                               
	a = 1
   
c1 = A()
c2 = A()
print(c1.a)
print(c2.a)
c1.a = 2
print('c1.a=2,   c1.a:',c1.a,'c2.a:',c2.a)
A.a = 3
print('A.a=3,    c1.a:',c1.a,'c2.a:',c2.a)
c3 = A()
print('c3=A(),   c3.a: ',c3.a)
c2.a = 4
A.a = 8
print('c2.a=4,A.a=8,    c1.a:',c1.a,'  c2.a:',c2.a,'   c3.a:',c3.a)

