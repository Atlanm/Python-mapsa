import os
from abc import ABC, abstractmethod
import hashlib
import pickle
open('password.txt', 'a+')


class Account(ABC):  # abstract class to define concepts of an account
    @abstractmethod
    def signup(self):
        pass

    @abstractmethod
    def login(self):
        pass


class UserInterface(ABC):  # abstract class to define concepts of UI in Semi-Redis
    @abstractmethod
    def set(self, key_value):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def remove(self, key):
        pass

    @abstractmethod
    def level_1(self):
        pass

    @abstractmethod
    def level_2(self):
        pass

    @abstractmethod
    def exit(self):
        pass


class Data:                                                           # data class for generate key-value data structure
    def __init__(self, key, value):
        self.key = key
        self.value = value


class User(Account):                                                    # class of account operation to create or use
    def __init__(self):                                                 # define user-name, password, user-lists & etc.
        self.user_name = None
        self.password = None
        self.data_base = open('password.txt', 'rb')
        self.past_user_names = list()
        try:
            self.usr = pickle.load(self.data_base)
        except:
            self.usr = dict()

    def signup(self):                                                   # define signing up operation
        self.data_base = open('password.txt', 'rb')
        # print(pickle.load(self.data_base))
        try:
            self.past_user_names = pickle.load(self.data_base).keys()   # read signed user names
        except:
            self.past_user_names = []

        self.user_name = input('Please Enter your user name: ')         # Enter user-name
        if self.user_name in self.past_user_names:                      # compare of user name to be unique
            print('This user name is be selected; Please try again')
            self.signup()
        self.data_base.close()
        self.password = input('Please Enter your password (at least 8 characters): ')  # Enter password
        if len(self.password) >= 8:
            self.password_repeat = input('Please Repeat your password: ')              # Re-Enter password
            if self.password_repeat == self.password:                                  # Verification of password
                md5 = hashlib.md5()
                md5.update(self.password.encode('utf-8'))
                self.password = md5.hexdigest()                                        # Hashing
                self.usr[self.user_name] = self.password                         # Assigning username to chosen password
                self.data_base = open('password.txt', 'wb')
                pickle.dump(self.usr, self.data_base)                            # Update account data-base
                self.data_base.close()
                open(f'{self.user_name}.txt', 'a')                               # Create new file in name of username
                return
        else:
            print('\"\"Your password must be more than 8 characters\"\"')
            self.signup()

    def login(self):                                                        # define Login operation
        self.user_name = input('Please Enter your user name: ')             # Take username
        self.password = input('Please Enter your password: ')               # Take password
        md5 = hashlib.md5()
        md5.update(self.password.encode('utf-8'))
        self.password = md5.hexdigest()                                     # Hashing taken password
        self.data_base = open('password.txt', 'rb')
        self.accounts = pickle.load(self.data_base)
        if self.user_name in self.accounts.keys() and self.password == self.accounts[self.user_name]:   # compare with data-base
            return True, self.data_base.close()  # self.accounts_file
        print('Username or Password is Wrong!!!')
        User.login(self)


class Menu(User, UserInterface):                                    # Menu class to prepare an Interface to use pro.
    def __init__(self):
        super(Menu, self).__init__()
        Menu.level_1(self)

    def level_1(self):                                              # First-Level Selection
        print('''Please select Your entering type:
                [+]-1 login
                [+]-2 signup
                [+]-3 Exit
                    ''')
        self.entering = input()                                     # Switching to use class methods
        if self.entering == '1':
            User.login(self)
            Menu.level_2(self)
        elif self.entering == '2':
            User.signup(self)
            Menu.level_1(self)
        elif self.entering == '3':
            Menu.exit(self)
        else:
            print('That\'s wrong, Please try again')
            Menu.level_1(self)

    def level_2(self):                                              # Second-Level Selection
        print('''*** Welcome ***
        Let\'s select something:
        [+]-1 Help
        [+]-2 SET key value
        [+]-3 Get key
        [+]-4 Remove key
        [+]-5 Exit
            ''')
        self.choice = input()                                       # Switching to use class methods
        if self.choice == '1':
            Menu.help(self)
        elif self.choice == '2':
            self.key_value = input('SET ')
            Menu.set(self, self.key_value)
        elif self.choice == '3':
            self._key_ = input('GET ')
            Menu.get(self, self._key_)
        elif self.choice == '4':
            self.remove_item = input('Remove ')
            Menu.remove(self, self.remove_item)
        elif self.choice == '5':
            Menu.exit(self)
        else:
            print('select error: Please try again!!!')
            Menu.level_2(self)
        if input("Previous [y/n]? ") == 'y':
            Menu.level_2(self)

    def help(self):                                                         # HELP method to have some Description
        print(f'''*** Hello {self.user_name} ***
        SET Method: 
        This method is using for set key-value data\'s; 
        (before first blank-space given key and after first blank-space given value
        key-value can be int,str,list,dict,...)
        
        Get Method: 
        This method is using for represent value of given key data;
        (every data type you enter, given key and if there are exist this item represented data value)
        
        REMOVE Method: 
        This method is using for remove a key-value data from your file;
        (entering a key is enough to remove)
        
        EXIT Method:
        This method generated to end of operation;
        (after select this method operation i\'ll stoped)
                ''')

    def set(self, set_data):                                    # define SET method to set new key-value data in account
        account_data = open(f'{self.user_name}.txt', 'ab')
        set_data = set_data.split()                             # separate by blank-space
        new_data = Data(set_data[0], set_data[1:])
        return pickle.dump(new_data, account_data), account_data.close()

    def get(self, key):                                         # define GET method to call value of specified key
        self.user_file = open(f'{self.user_name}.txt', 'rb')
        while True:
            try:
                self.item = pickle.load(self.user_file)
                if self.item.key == key:                        # compare to find specified key
                    print(f'{self.item.key}: {self.item.value}')
                    return self.item, self.user_file.close()
            except EOFError:
                break
        self.user_file.close()
        return print('This item is not founded')

    def remove(self, key):                                      # define REMOVE method to remove a specified item
        self.new_file_objects = []
        self.user_file = open(f'{self.user_name}.txt', 'rb')
        while True:
            try:
                self.item = pickle.load(self.user_file)
                if self.item.key != key:                        # Add all objects to a list except a specified data
                    self.new_file_objects.append(self.item)
            except EOFError:
                if not self.new_file_objects:
                    self.user_file.close()
                    return
                self.user_file.close()
                os.remove(f'{self.user_name}.txt')                      # Remove file
                self.user_file = open(f'{self.user_name}.txt', 'wb')    # Create new file in same name
                for obj in self.new_file_objects:
                    pickle.dump(obj, self.user_file)                    # Save objects except removed data
                self.user_file.close()
                return

    def exit(self):                                             # define EXIT method
        exit()


a = Menu()
