import random
import string
import argparse
import zxcvbn



class PasswordGenerator:
    def __init__(self, length=12, complexity="strong"):
        if not isinstance(length, int) or length <= 3:
            raise ValueError("Password length must be a positive integer and greater than 3.")
        if complexity not in ["weak", "moderate", "strong"]:
            raise ValueError(
                "Password complexity must be 'weak', 'moderate', or 'strong'.")
        self.length = length
        self.complexity = complexity

    def generate_password(self):
        # Define character sets for password generation
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        symbols = string.punctuation

        # Initialize password string
        password = ""

        # Generate password based on length
        for i in range(self.length):
            # Randomly select a character from the available sets
            rand_set = random.choice(
                [lowercase_letters, uppercase_letters, digits, symbols])
            rand_char = random.choice(rand_set)

            # Add the character to the password string
            password += rand_char

        return password


class PasswordChecker:
    def __init__(self, password):
        self.password = password

    def check_strength(self):
        strength = zxcvbn.password_strength(self.password)['score']
        return strength


if __name__ == "__main__":
    # Set up argparse to get user input for password length and complexity
    parser = argparse.ArgumentParser(description="Generate a strong password.")
    parser.add_argument("-l", "--length", type=int,
                        help="Password length ")
    parser.add_argument("-c", "--complexity", type=str, 
                        choices=["weak", "moderate", "strong"], help="Password complexity (default: strong)")
    args = parser.parse_args()

    # Prompt user to enter input if missing
    while not args.length:
        try:
            args.length = int(input('Enter password length: '))
            if args.length <= 3:
                print('Password length must be a positive integer. and greater than 3')
                args.length = None
        except ValueError:
            print('Invalid input. Password length must be a positive integer.')
            args.length = None

    while not args.complexity:
        args.complexity = input('Enter password complexity (weak/moderate/strong): ')
        if args.complexity not in ["weak", "moderate", "strong"]:
            print('Invalid input. Password complexity must be "weak", "moderate", or "strong".')
            args.complexity = None

 # Check password length based on complexity level
    if args.complexity == "weak" and args.length < 5:
        print("Password length must be at least 5 for weak passwords.")
        exit()
    elif args.complexity == "moderate" and args.length < 6:
        print("Password length must be at least 6 for moderate passwords.")
        exit()
    elif args.complexity == "strong" and args.length < 7:
        print("Password length must be at least 7 for strong passwords.")
        exit()

    # Generate a password and check its strength
    generator = PasswordGenerator(args.length, args.complexity)
    password = generator.generate_password()

    checker = PasswordChecker(password)
    while checker.check_strength() < {"weak": 2, "moderate": 3, "strong": 4}[args.complexity]:
        password = generator.generate_password()
        checker = PasswordChecker(password)



# Output a message to the user
print(f"Generated password: {password}")
