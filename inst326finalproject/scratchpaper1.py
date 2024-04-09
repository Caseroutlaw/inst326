import numpy as np
from PIL import Image
import os

# Function to generate a matrix for scratch-off rewards
def generate_ordered_prizes(prize_quantities):
    matrix_list = []
    rows, cols = 3, 4
    total_positions = rows * cols
    
    for prize, quantity in prize_quantities.items():
        for _ in range(quantity):
            position = len(matrix_list) % total_positions
            matrix = np.zeros((rows, cols), dtype=int)
            matrix[position // cols, position % cols] = prize
            matrix_list.append(matrix)
    return matrix_list

# Quantities for each prize
prize_quantities = {1: 20, 2: 30, 3: 150, 4: 200}

# Generate prize matrices
ordered_matrices = generate_ordered_prizes(prize_quantities)

# Save matrices to a text file
with open('ScratchOff1.txt', 'w') as file:
    for matrix in ordered_matrices:
        matrix_str = np.array2string(matrix, separator=', ')
        file.write(matrix_str + "\n\n")

# Load the template image
template_path = 'E:\\Company\\Program\\ScratchOffTemplate1.png'
template_image = Image.open(template_path)

# Load saved matrices from the file
matrices = []
with open('ScratchOff1.txt', 'r') as file:
    content = file.read()
    matrices = [np.array(eval(matrix)) for matrix in content.strip().split('\n\n')]

# Define coordinates for the positions of the prizes
positions = [
    (230, 800), (430, 800), (630, 800), (830, 800),      # First row
    (230, 990), (430, 990), (630, 990), (830, 990),      # Second row
    (230, 1180), (430, 1180), (630, 1180), (830, 1180)   # Third row
]

# Output folder
output_folder = 'E:\\Company\\Program\\ScratchOffResults' # Change the path as needed
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Paths for prize images
prizes_path = 'E:\\Company\\Program\\'
prize_images = {
    0: Image.open(os.path.join(prizes_path, '0.png')),  # Non-winning prize image
    1: Image.open(os.path.join(prizes_path, '1.png')),  # First prize image
    2: Image.open(os.path.join(prizes_path, '2.png')),  # Second prize image
    3: Image.open(os.path.join(prizes_path, '3.png')),  # Third prize image
    4: Image.open(os.path.join(prizes_path, '4.png')),  # Fourth prize image
    # Add other prize images as needed by copying and modifying the above lines
}

# Generate and save images
for index, matrix in enumerate(matrices):
    edited_image = template_image.copy()
    for i, row in enumerate(matrix):
        for j, prize in enumerate(row):
            if prize >= 0:  # Assuming 0 is also a valid prize
                prize_image = prize_images[prize]
                x, y = positions[i * len(row) + j]
                # Ensure the prize image fits the template position, may need to adjust the size
                prize_image = prize_image.resize((130, 115))  # Assuming size is 80x80
                edited_image.paste(prize_image, (x, y), prize_image)

    output_path = os.path.join(output_folder, f'ScratchOff_{index+1}.png')
    edited_image.save(output_path)

print('All scratch-off images have been generated successfully.')
