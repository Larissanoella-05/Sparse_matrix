#! /usr/bin/python3


class CompressedMatrix:
    def __init__(self, file_path=None, rows=None, cols=None):
        self.rows = rows
        self.cols = cols
        self.data = {}
        if file_path:
            self.load_from_file(file_path)

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = CompressedMatrix(rows=self.rows, cols=self.cols)
        result.data = self.data.copy()

        for (r, c), val in other.data.items():
            new_val = result.get_value(r, c) + val
            result.set_value(r, c, new_val)

        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = CompressedMatrix(rows=self.rows, cols=self.cols)
        result.data = self.data.copy()

        for (r, c), val in other.data.items():
            new_val = result.get_value(r, c) - val
            result.set_value(r, c, new_val)
        
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions must match for multiplication")

        result = CompressedMatrix(rows=self.rows, cols=other.cols)

        for (r1, c1), val1 in self.data.items():
            for (r2, c2), val2 in other.data.items():
                if c1 == r2:
                    result.set_value(r1, c2, result.get_value(r1, c2) + val1 * val2)
        
        return result

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                self.rows = int(lines[0].split('=')[1].strip())
                self.cols = int(lines[1].split('=')[1].strip())

                for line in lines[2:]:
                    line = line.strip()
                    if line:
                        r, c, val = map(int, line.strip('()').split(','))
                        self.data[(r, c)] = val
                return self.data
        except ValueError as e:
            raise ValueError("File format is incorrect") from e

    def save_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (r, c), val in self.data.items():
                file.write(f"({r}, {c}, {val})\n")

    def get_value(self, r, c):
        return self.data.get((r, c), 0)

    def set_value(self, r, c, val):
        if val != 0:
            self.data[(r, c)] = val
        elif (r, c) in self.data:
            del self.data[(r, c)]

    def __str__(self):
        return f"rows={self.rows}\ncols={self.cols}\n(data={self.data})"
