import numpy as np
import os

"""
Generate scratch-off cards with different prizes based on what the company wants

    Attributes:
        cost (float): The cost of a single scratch card that the user can change in the command line
        num_cards (int): The number of scratch cards to generate
        prize_stats (dict): Tracks the count of each prize that won
        prize_values (dict): Count of prize money depending on the type that won
        probabilities (list of floats): probability of the prize winning
        matrices (list): Stores generated matrices that are scratch cards
"""
class ScratchOffGenerator:
    #initializer
    def __init__(self, cost, num_cards):
        self.cost = cost
        self.num_cards = num_cards

        #dictionary to track how many of each prize has been won
        self.prize_stats = {'No Prize': 0, 'Baby Prize': 0, 'Prize': 0, 'Small Prize': 0, 'Medium Prize': 0, 'Big Prize': 0, 'JACKPOT': 0, 'total_won': 0}

        #prize winnings depending on cost
        self.prize_values = {
            'No Prize': 0,
            'Baby Prize': int(0.5 * cost), 
            'Prize': cost,                  
            'Small Prize': int(1.5 * cost),
            'Medium Prize': int(3 * cost),
            'Big Prize': int(20 * cost),
            'JACKPOT': int(2000 * cost)
        }

        #probabilities of winning each prize, can change values depending on what the company wants the odds to be
        self.probabilities = [
            ('No Prize', 0.51),
            ('Baby Prize', 0.20),
            ('Prize', 0.15019),
            ('Small Prize', 0.08),
            ('Medium Prize', 0.05),
            ('Big Prize', 0.0098),
            ('JACKPOT', 0.00001)
        ]
        #list to store generated scratch offs
        self.matrices = []

    """
    Generates a scratch off matrix with a random prize(or no prize :OOOO)

    Returns:
        matrix: A 2D array representing the scratch off ticket  
"""
    def generate_prize_matrix(self):
        rows = 3
        col = 4

        #fills matrix with zeroes
        matrix = np.zeros((rows, col), dtype=int)

        #randomly selects row and col to put prize in
        random_row = np.random.randint(rows)
        random_col = np.random.randint(col)

        #unpacks prize types based on the probabilities given earlier
        zipped_probabilities = zip(*self.probabilities)
        prizes, probabilities = list(zipped_probabilities)

        #Chooses prize 
        prize_level = np.random.choice(prizes, p=probabilities)

        #puts prize in the random row and col
        matrix[random_row, random_col] = self.prize_values[prize_level]

        #for statistics adds one for the prize won
        self.prize_stats['total_won'] += self.prize_values[prize_level]
        self.prize_stats[prize_level] += 1
        return matrix
    
    #Generates number of matrices depending on how many user wants
    def generate_matrices(self):
        for _ in range(self.num_cards):
            self.matrices.append(self.generate_prize_matrix())

    #Saves matrices to scrathoffs.txt
    def save_matrices(self, file_name):
        with open(file_name, 'w') as file:
            for matrix in self.matrices:
                matrix_str = np.array2string(matrix, separator=', ')
                file.write(matrix_str + "\n\n")

    """Prompts user for input making sure that it meets the right conditions

    Args:
        prompt (str): Displays prompt
        cast_type (float): type of input the user can put in
        condition (function): A function to validate the input

    Returns:
        user input
    """
def get_user_input(prompt, cast_type=float, condition=None):
    while True:
        try:
            value = cast_type(input(prompt))
            if condition and not condition(value):
                raise ValueError
            return value
        except ValueError:
            print("Invalid input, please try again.")

"""
    Main function to start the process of generating scratch cards and prints the results
    """
def main():
    #Gets number of scratch cards to generate and the cost of each card
    num_cards = get_user_input("Enter the number of scratch cards to generate (1-100000): ", int, lambda x: 1 <= x <= 100000)
    cost = get_user_input("Enter the cost of each scratch card: ", float, lambda x: x > 0)

    #initializes the scratch card with user input
    scratch_off = ScratchOffGenerator(cost, num_cards)
    scratch_off.generate_matrices()
    
    #seperate file that is generated
    output_file_name = 'scratchoffs.txt'
    scratch_off.save_matrices(output_file_name)
    
    #prints results for user to see
    print(f'{num_cards} random scratch-off matrices have been generated and saved successfully in "{output_file_name}".')
    print(f'Total Spent: ${num_cards * cost:.2f}')
    print(f'Total Won: ${scratch_off.prize_stats["total_won"]:.2f}')
    print('Prizes breakdown:')

    for prize_name in ['No Prize', 'Baby Prize', 'Prize', 'Small Prize', 'Medium Prize', 'Big Prize', 'JACKPOT']:
        #calculates percentage of each prize won
        if scratch_off.prize_stats[prize_name] > 0:
            percentage = (scratch_off.prize_stats[prize_name] / num_cards) * 100
        else:
            percentage = 0
        prize_money = scratch_off.prize_stats[prize_name] * scratch_off.prize_values[prize_name]
        print(f'  {prize_name}: {scratch_off.prize_stats[prize_name]} times (${prize_money}) ({percentage:.2f}%)')

if __name__ == "__main__":
    main()
