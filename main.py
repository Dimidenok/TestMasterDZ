from faker import Faker


fake = Faker('ru_Ru')
name = fake.name()
name = name.split()
print(name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
