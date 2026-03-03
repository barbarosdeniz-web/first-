import random

options = ["rock", "paper", "scissors"]
userPoint = 0

while True:
    # 1. input() döngünün içine alındı, böylece her elde tekrar soracak.
    # 2. lower() sonuna parantez eklendi.
    userInput = input("rock, paper, scissors or Q: ").lower()
    
    if userInput == "q":
        break
        
    if userInput not in options:
        # Kullanıcı yanlış bir şey yazarsa diye ufak bir uyarı mesajı ekledik
        print("Geçersiz bir giriş yaptın, lütfen tekrar dene.\n")
        continue
        
    random_number = random.randint(0, 2)
    computer_pick = options[random_number]
    
    print("computer picked:", computer_pick)
    
    if userInput == "rock" and computer_pick == "scissors":
        userPoint += 1
        print("Sen kazandın!\n")
    elif userInput == "paper" and computer_pick == "rock":
        userPoint += 1
        print("Sen kazandın!\n")
    elif userInput == "scissors" and computer_pick == "paper":
        userPoint += 1
        print("Sen kazandın!\n")
    else:
        print("Kazanamadın!\n")

# Döngüden q ile çıkıldığında toplam puanı yazdırır
print(f"You win {userPoint} times")