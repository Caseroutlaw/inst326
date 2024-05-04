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

# Ask user to enter prize quantities
prize_quantities = {}
for i in range(1, 5):
    while True:
        try:
            quantity = int(input(f"Enter quantity for prize {i}: "))
            if quantity < 0:
                raise ValueError("Quantity must be a positive integer.")
            prize_quantities[i] = quantity
            break
        except ValueError as e:
            print(e)

# Generate prize matrices
ordered_matrices = generate_ordered_prizes(prize_quantities)

# Save matrices to a text file
while True:
    try:
        file_name = input("Enter file name to save matrices (include extension): ")
        with open(file_name, 'w') as file:
            for matrix in ordered_matrices:
                matrix_str = np.array2string(matrix, separator=', ')
                file.write(matrix_str + "\n\n")
        break
    except FileNotFoundError:
        print("File not found. Please enter a valid file name.")

# Load the template image
while True:
    template_path = input("Enter path for template image (e.g., D:\\images\\template.png): ")
    if os.path.exists(template_path):
        break
    else:
        print("File not found. Please enter a valid path.")

template_image = Image.open(template_path)

# Load saved matrices from the file
matrices = []
while True:
    file_name = input("Enter file name to load matrices (include extension): ")
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            content = file.read()
            matrices = [np.array(eval(matrix)) for matrix in content.strip().split('\n\n')]
        break
    else:
        print("File not found. Please enter a valid file name.")

# Define coordinates for the positions of the prizes
positions = []
for i in range(3):
    for j in range(4):
        while True:
            try:
                coordinate = input(f"Enter coordinates for prize at row {i+1} and column {j+1} (format: x,y): ")
                x, y = map(int, coordinate.split(','))
                positions.append((x, y))
                break
            except ValueError:
                print("Invalid input format. Please enter coordinates in the format 'x,y'.")


# Output folder
while True:
    output_folder = input("Enter output folder path: ")
    if os.path.exists(output_folder):
        break
    else:
        print("Folder not found. Please enter a valid folder path.")

# Paths for prize images
prizes_path = input("Enter path for prize images: ")
while not os.path.exists(prizes_path):
    print("Folder not found. Please enter a valid folder path.")
    prizes_path = input("Enter path for prize images: ")

prize_images = {}
for i in range(5):
    image_path = input(f"Enter path for prize image {i}: ")
    while not os.path.exists(image_path):
        print("File not found. Please enter a valid file path.")
        image_path = input(f"Enter path for prize image {i}: ")
    prize_images[i] = Image.open(image_path)

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
