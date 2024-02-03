from djitellopy import Tello

tello = Tello()
tello.connect()
tello.speed = 0
print(tello.get_battery())

# input() Function
# input() function is used to take input from the user.
# input() function always returns a string
# name = input("Enter your name: ")
# age = input("Enter your age: ")
# favorite_food = input("Enter your favorite food: ")

# print(name)

print("Enter your name: ")
name = input()
print("Enter your age: ")
age = input()
print("Enter your favorite food: ")
favorite_food = input()
print('Your Name is: ' + name)
print('Your Age is : ' + age)
print('Your Favorite Food is : ' + favorite_food)
