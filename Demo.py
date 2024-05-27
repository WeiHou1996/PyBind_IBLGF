import example
p = example.Dog("Molly")
print(p.name)
print(p.bark())

c = example.sparse_mat()
c.resizing_row(5)
c.add_element(1,1,2.0)
print(c.numRow_loc())

ll = example.VecDog(p, 3)
for i in range(0, 3):
    print(ll.names[i].bark())

d = example.sparse_mat()
d.resizing_row(5)
d.add_element(3,4,2.0)
print(d.numRow_loc())

e = c+d
print(e.numRow_loc())
for i in range(1,e.numRow_loc() + 1):
    e.print_row_full(i)

tmp = e.get_CSR()
print(tmp)

f = example.sparse_mat()
f.resizing_row(5)
f.add_element(1,1,10)
f.add_element(1,2,20)
f.add_element(2,2,30)
f.add_element(2,4,40)
f.add_element(3,3,50)
f.add_element(3,4,60)
f.add_element(3,5,70)
f.add_element(4,6,80)

print(f.numRow_loc())
for i in range(1,f.numRow_loc() + 1):
    f.print_row_full(i, 7)

tmp = f.get_CSR()
print(tmp)