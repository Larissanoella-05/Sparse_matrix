#! /usr/bin/python3
import os

from compressed_matrix import CompressedMatrix

def main():
    # Input paths
    input_base_path = 'dsa/compressed_matrix/sample_inputs/'
    matrix1_file_path = os.path.join(input_base_path, 'matrix1.txt')
    matrix2_file_path = os.path.join(input_base_path, 'matrix2.txt')

    # Load the matrices
    matrix1 = CompressedMatrix(file_path=matrix1_file_path)
    matrix2 = CompressedMatrix(file_path=matrix2_file_path)

    # Operations
    result_add = matrix1.add(matrix2)
    result_sub = matrix1.subtract(matrix2)
    result_mult = matrix1.multiply(matrix2)

    # Output paths
    output_base_path = 'dsa/compressed_matrix/sample_outputs/'
    output_add_path = os.path.join(output_base_path, 'addition_result.txt')
    output_sub_path = os.path.join(output_base_path, 'subtraction_result.txt')
    output_mult_path = os.path.join(output_base_path, 'multiplication_result.txt')

    # Save the result
    result_add.save_to_file(output_add_path)
    result_sub.save_to_file(output_sub_path)
    result_mult.save_to_file(output_mult_path)

    # Print the result
    print()
    print(f"Addition\n{result_add}")
    print()
    print(f"Subtraction\n{result_sub}")
    print()
    print(f"Multiplication\n{result_mult}")

main()
