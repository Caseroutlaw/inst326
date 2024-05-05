import unittest
from scratchpaper1 import ScratchOffGenerator

class TestScratchOffGenerator(unittest.TestCase):

    def test_initialization(self):
        """Test whether the initialization is correct."""
        gen = ScratchOffGenerator(2.00, 100)
        self.assertEqual(gen.cost, 2.00)
        self.assertEqual(gen.num_cards, 100)

    def test_generate_prize_matrix(self):
        """Test whether the generated matrix is valid 
        and check that the award statistics are updated correctly."""
        gen = ScratchOffGenerator(2.00, 1)
        matrix = gen.generate_prize_matrix()
        self.assertIn(matrix.max(), gen.prize_values.values())
        self.assertEqual(sum(gen.prize_stats.values()), 1)

    def test_generate_matrices(self):
        """Test whether the correct number of matrices is generated."""
        gen = ScratchOffGenerator(2.00, 10)
        gen.generate_matrices()
        self.assertEqual(len(gen.matrices), 10)

    def test_save_matrices(self):
        """Test the file saving function"""
        gen = ScratchOffGenerator(2.00, 10)
        gen.generate_matrices()
        output_file_name = 'test_output.txt'
        gen.save_matrices(output_file_name)
        # Confirm file creation
        with open(output_file_name, 'r') as file:
            content = file.read()
        self.assertIn('0', content)  

if __name__ == '__main__':
    unittest.main()
