#!/usr/bin/env python3

class SparseMatrix:
  def __init__(self, numRows=0, numCols=0):
    self.matrix = {}
    self.numRows = numRows
    self.numCols = numCols
    
  @staticmethod
  def load(matrixFilePath=None):
    if not matrixFilePath:
      return None
    
    try:
      with open(matrixFilePath, 'r') as file:
        lines = file.readlines()
        numRows = int(lines[0].strip().split('=')[1])
        numCols = int(lines[1].strip().split('=')[1])
        matrix = SparseMatrix(numRows, numCols)
        for line in lines[2:]:
          if line.strip():
            row, col, val = map(int, line.strip()[1:-1].split(','))
            matrix[(row, col)] = val
            
        return matrix
    except Exception as e:
      raise ValueError("Input file has wrong format") from e
    
  def getElement(self, row, col):
    return self.matrix.get((row, col), 0)
  
  def setElement(self, row, col, value):
    if value != 0:
      self.matrix[(row, col)] = value
    elif (row, col) in self.matrix:
      del self.matrix[(row, col)]
      
  def __getitem__(self, tuple):
    return self.getElement(tuple[0], tuple[1])
  
  def __setitem__(self, tuple, value):
    self.setElement(tuple[0], tuple[1], value)
    
  def __add__(self, other):
    if type(other) != SparseMatrix:
      raise ValueError("Matrices can only be added to matrices")
    if self.numRows != other.numRows or self.numCols != other.numCols:
      raise ValueError("Matrix dimensions must match for addition")
    result = SparseMatrix(self.numRows, self.numCols)
    for row in range(self.numRows):
      for col in range(self.numCols):
        sum_value = self[(row, col)] + other[(row, col)]
        result[(row, col)] = sum_value
    return result
  
  def __sub__(self, other):
    if type(other) != SparseMatrix:
      raise ValueError("Matrices can only be subtracted from matrices")
    if self.numRows != other.numRows or self.numCols != other.numCols:
      raise ValueError("Matrix dimensions must match for subtraction")
    result = SparseMatrix(self.numRows, self.numCols)
    for row in range(self.numRows):
      for col in range(self.numCols):
        sub_value = self[(row, col)] - other[(row, col)]
        result[(row, col)] = sub_value
    return result
  
  def __mul__(self, other):
    if type(other) != SparseMatrix:
      raise ValueError("Matrices can only be multiplied to matrices")
    if self.numRows != other.numCols:
      raise ValueError("Matrix dimensions must match for multiplication")
    result = SparseMatrix(self.numRows, other.numCols)
    for row in range(self.numRows):
      for col in range(other.numCols):
        product_value = 0
        for k in range(self.numCols):
          product_value += self[(row, k)] * self[(k, col)]
        result[(row, col)] = product_value
    return result
    
  def __str__(self):
    result = f"rows={self.numRows}\ncols={self.numCols}\n"
    for (row, col), value in sorted(self.matrix.items()):
      result += f"({row}, {col}, {value})\n"
    return result
  
  def to_file(self, file_path):
    with open(file_path, 'w') as file:
        file.write(str(self))


def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python main.py <matrix1_path> <matrix2_path>")
        return

    matrix1_path = sys.argv[1]
    matrix2_path = sys.argv[2]

    matrix1 = SparseMatrix.load(matrix1_path)
    matrix2 = SparseMatrix.load(matrix2_path)

    print("Choose an operation to perform:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    
    print(f"({matrix1.numRows}, {matrix1.numCols}) ({matrix2.numRows}, {matrix2.numCols})")

    operation = input("Enter the number of the operation (1/2/3): ")

    if operation == '1':
        result = matrix1 + matrix2
    elif operation == '2':
        result = matrix1 - matrix2
    elif operation == '3':
        result = matrix1 * matrix2
    else:
        print("Unknown operation. Please enter 1, 2, or 3.")
        return

    result.to_file("results.txt")
    print("The result has been written to results.txt")
  
if __name__ == "__main__":
  main()
