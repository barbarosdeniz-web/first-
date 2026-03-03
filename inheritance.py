#super() -> same as 
#super() dersek self kullanmaya gerek kalmaz, gönderilen parametreler yazılır paranteze sadece
#pass -> fonksiyonu boş geçmek
class Person:
    def __init__(self, fname, lname):
        self.firstName = fname
        self.lastName = lname
    def hello(self):
        print("hello i am a person")
    

class Student(Person):
    def __init__(self, fname, lname,number):
        super().__init__(fname, lname)  # üst sınıfın init'ini çağırıyoruz
        self.studentNumber=number

class teacher(Person):
    def __init__(self,fname,lname,branch):
        super().__init__(fname,lname)
        self.teacherBranch=branch
    def who_am_i(self):
        print(f"i am a {self.teacherBranch} teacher")

p1 = Person(fname="Deniz", lname="Küçük")
s1 = Student("Özgür", "Küçük",223969)
t1= teacher("kemal","atatürk","math")
p1.hello()
t1.who_am_i()
print(t1.firstName,t1.lastName,t1.teacherBranch)
print(p1.firstName, p1.lastName)  # Deniz Küçük
print(s1.firstName, s1.lastName,s1.studentNumber)  # Özgür Küçük