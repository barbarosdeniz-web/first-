class Person:
    adress="none"
    def __init__(self,name,year):
        self.name=name
        self.year=year

p1= Person("deniz",2005)
p2=Person("barbaros",2026)
print(f"person 1 name is {p1.name}, year is {p1.year}")
print(f"person 2 name is {p2.name}, year is {p2.year}")
