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
                
                if len(lines) < 1:
                    raise ValueError("File is empty")
                
                explicit_dimensions = False
                try:
                    if '=' in lines[0]: 
                        numRows = int(lines[0].strip().split('=')[1])
                        numCols = int(lines[1].strip().split('=')[1])
                        data_start_line = 2
                        explicit_dimensions = True
                    else:  
                        dims = lines[0].strip().split()
                        if len(dims) >= 2 and all(d.isdigit() for d in dims[:2]):
                            numRows = int(dims[0])
                            numCols = int(dims[1])
                            data_start_line = 1
                            explicit_dimensions = True
                        else:
                           
                            data_start_line = 0
                            numRows = 0
                            numCols = 0
                except Exception:
                   
                    data_start_line = 0
                    numRows = 0
                    numCols = 0
                
              
                matrix = SparseMatrix(numRows, numCols)
                max_row = 0
                max_col = 0
                
               
                for i, line in enumerate(lines[data_start_line:], data_start_line + 1):
                    line = line.strip()
                    if not line: 
                        continue
                    
                    try:
                       
                        if line.startswith('(') and line.endswith(')'):
                           
                            parts = line[1:-1].split(',')
                            row, col, val = map(int, parts)
                        else:
                           
                            parts = line.split()
                            if len(parts) != 3:
                                raise ValueError(f"Expected 3 values for row col val, got {len(parts)}")
                            row, col, val = map(int, parts)
                        
                      
                        max_row = max(max_row, row)
                        max_col = max(max_col, col)
                        
                      
                        if val != 0:  
                            matrix.matrix[(row, col)] = val
                    except Exception as e:
                        raise ValueError(f"Error parsing line {i}: '{line}' - {str(e)}")
                
                
                if not explicit_dimensions or (max_row >= matrix.numRows or max_col >= matrix.numCols):
                    matrix.numRows = max(matrix.numRows, max_row + 1)
                    matrix.numCols = max(matrix.numCols, max_col + 1)
                
                return matrix
                
        except Exception as e:
            raise ValueError(f"Input file has wrong format: {str(e)}") from e
    
    def getElement(self, row, col):

        return self.matrix.get((row, col), 0)
    
    def setElement(self, row, col, value):
      
        if row >= self.numRows:
            self.numRows = row + 1
        if col >= self.numCols:
            self.numCols = col + 1
        
        if value != 0:
            self.matrix[(row, col)] = value
        elif (row, col) in self.matrix:
            del self.matrix[(row, col)]
            
    def __getitem__(self, tuple):
        return self.getElement(tuple[0], tuple[1])
    
    def __setitem__(self, tuple, value):
        self.setElement(tuple[0], tuple[1], value)
    
    def transpose(self):
        """Return a new matrix that is the transpose of this matrix"""
        result = SparseMatrix(self.numCols, self.numRows)
        for (row, col), value in self.matrix.items():
            result[(col, row)] = value
        return result
        
    def __add__(self, other):
        if not isinstance(other, SparseMatrix):
            raise ValueError("Matrices can only be added to matrices")
        
       
        if self.numRows == other.numRows and self.numCols == other.numCols:
         
            result = SparseMatrix(self.numRows, self.numCols)
            
           
            for (row, col), value in self.matrix.items():
                result[(row, col)] = value
            
            for (row, col), value in other.matrix.items():
                result[(row, col)] = result[(row, col)] + value
        
        elif self.numRows == other.numCols and self.numCols == other.numRows:
          
            print("Transposing second matrix for addition...")
            other_transposed = other.transpose()
            
            result = SparseMatrix(self.numRows, self.numCols)
            
  
            for (row, col), value in self.matrix.items():
                result[(row, col)] = value
            
            for (row, col), value in other_transposed.matrix.items():
                result[(row, col)] = result[(row, col)] + value
        else:
            raise ValueError(f"Matrix dimensions must match for addition: ({self.numRows}, {self.numCols}) and ({other.numRows}, {other.numCols})")
            
        return result
    
    def __sub__(self, other):
        if not isinstance(other, SparseMatrix):
            raise ValueError("Matrices can only be subtracted from matrices")
        
       
        if self.numRows == other.numRows and self.numCols == other.numCols:
         
            result = SparseMatrix(self.numRows, self.numCols)
            
     
            for (row, col), value in self.matrix.items():
                result[(row, col)] = value
            
           
            for (row, col), value in other.matrix.items():
                result[(row, col)] = result[(row, col)] - value
                
        elif self.numRows == other.numCols and self.numCols == other.numRows:
       
            print("Transposing second matrix for subtraction...")
            other_transposed = other.transpose()
            
            result = SparseMatrix(self.numRows, self.numCols)
            
            
            for (row, col), value in self.matrix.items():
                result[(row, col)] = value
            
           
            for (row, col), value in other_transposed.matrix.items():
                result[(row, col)] = result[(row, col)] - value
        else:
            raise ValueError(f"Matrix dimensions must match for subtraction: ({self.numRows}, {self.numCols}) and ({other.numRows}, {other.numCols})")
            
        return result
    
    def __mul__(self, other):
        if not isinstance(other, SparseMatrix):
            raise ValueError("Matrices can only be multiplied by matrices")
        
        
        if self.numCols == other.numRows:
          
            result = SparseMatrix(self.numRows, other.numCols)
            
           
            for (i, k), val1 in self.matrix.items():
                for (k2, j), val2 in other.matrix.items():
                    if k == k2: 
                        current = result.matrix.get((i, j), 0)
                        new_val = current + val1 * val2
                        if new_val != 0:
                            result.matrix[(i, j)] = new_val
                        elif (i, j) in result.matrix:
                            del result.matrix[(i, j)]
            
    
        elif self.numCols == other.numCols and self.numRows != other.numRows:
            print("Transposing second matrix for multiplication...")
            other_transposed = other.transpose()
            
            
            result = SparseMatrix(self.numRows, other_transposed.numCols)
            
           
            for (i, k), val1 in self.matrix.items():
                for (k2, j), val2 in other_transposed.matrix.items():
                    if k == k2: 
                        current = result.matrix.get((i, j), 0)
                        new_val = current + val1 * val2
                        if new_val != 0:
                            result.matrix[(i, j)] = new_val
                        elif (i, j) in result.matrix:
                            del result.matrix[(i, j)]
        else:
            raise ValueError(f"Matrix dimensions not compatible for multiplication: ({self.numRows}, {self.numCols}) * ({other.numRows}, {other.numCols})")
                    
        return result
        
    def __str__(self):
        result = f"rows={self.numRows}\ncols={self.numCols}\n"
        for (row, col), value in sorted(self.matrix.items()):
            result += f"({row},{col},{value})\n"
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

    try:
        matrix1 = SparseMatrix.load(matrix1_path)
        matrix2 = SparseMatrix.load(matrix2_path)

        print("Choose an operation to perform:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        
        print(f"Matrix 1: ({matrix1.numRows}, {matrix1.numCols})")
        print(f"Matrix 2: ({matrix2.numRows}, {matrix2.numCols})")

        operation = input("Enter the number of the operation (1/2/3): ")

        if operation == '1':
            try:
                result = matrix1 + matrix2
                result.to_file("results.txt")
                print("The result has been written to results.txt")
            except ValueError as e:
                print(f"Error: {e}")
                print("Hint: If the matrices have transposed dimensions, try transposing one of them first.")
        elif operation == '2':
            try:
                result = matrix1 - matrix2
                result.to_file("results.txt")
                print("The result has been written to results.txt")
            except ValueError as e:
                print(f"Error: {e}")
                print("Hint: If the matrices have transposed dimensions, try transposing one of them first.")
        elif operation == '3':
            try:
                result = matrix1 * matrix2
                result.to_file("results.txt")
                print("The result has been written to results.txt")
            except ValueError as e:
                print(f"Error: {e}")
                if matrix1.numRows == matrix2.numRows and matrix1.numCols == matrix2.numCols:
                    print("Note: For matrix multiplication, typically matrix1's columns should equal matrix2's rows.")
        else:
            print("Unknown operation. Please enter 1, 2, or 3.")
            return
        
    except Exception as e:
        print(f"Error: {str(e)}")
  
if __name__ == "__main__":
    main()