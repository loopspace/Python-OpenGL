# OpenGL is column-major:
#
# 0 4  8 12
# 1 5  9 13
# 2 6 10 14
# 3 7 11 15
#
class Matrix:

    def __init__(self,*args):
        if len(args) == 1:
            self.matrix = args[0]
        elif len(args) == 16:
            self.matrix = args
        else:
            self.matrix = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

    def __mul(self,m):
        if isinstance(m,Matrix):
            mm = self.matrix
            m = m.matrix
            return Matrix([
                mm[0] * m[0] + mm[4] * m[1] + mm[8] * m[2] + mm[12] * m[3],
                mm[1] * m[0] + mm[5] * m[1] + mm[9] * m[2] + mm[13] * m[3],
                mm[2] * m[0] + mm[6] * m[1] + mm[10] * m[2] + mm[14] * m[3],
                mm[3] * m[0] + mm[7] * m[1] + mm[11] * m[2] + mm[15] * m[3],
                mm[0] * m[4] + mm[4] * m[5] + mm[8] * m[6] + mm[12] * m[7],
                mm[1] * m[4] + mm[5] * m[5] + mm[9] * m[6] + mm[13] * m[7],
                mm[2] * m[4] + mm[6] * m[5] + mm[10] * m[6] + mm[14] * m[7],
                mm[3] * m[4] + mm[7] * m[5] + mm[11] * m[6] + mm[15] * m[7],
                mm[0] * m[8] + mm[4] * m[9] + mm[8] * m[10] + mm[12] * m[11],
                mm[1] * m[8] + mm[5] * m[9] + mm[9] * m[10] + mm[13] * m[11],
                mm[2] * m[8] + mm[6] * m[9] + mm[10] * m[10] + mm[14] * m[11],
                mm[3] * m[8] + mm[7] * m[9] + mm[11] * m[10] + mm[15] * m[11],
                mm[0] * m[12] + mm[4] * m[13] + mm[8] * m[14] + mm[12] * m[15],
                mm[1] * m[12] + mm[5] * m[13] + mm[9] * m[14] + mm[13] * m[15],
                mm[2] * m[12] + mm[6] * m[13] + mm[10] * m[14] + mm[14] * m[15],
                mm[3] * m[12] + mm[7] * m[13] + mm[11] * m[14] + mm[15] * m[15]
            ])
        else:
            return Matrix(map (lambda x: x * m, self.matrix))


    def __rmul(self,m):
        if isinstance(m,Matrix):
            mm = m.matrix
            m = self.matrix
            return Matrix([
                mm[0] * m[0] + mm[4] * m[1] + mm[8] * m[2] + mm[12] * m[3],
                mm[1] * m[0] + mm[5] * m[1] + mm[9] * m[2] + mm[13] * m[3],
                mm[2] * m[0] + mm[6] * m[1] + mm[10] * m[2] + mm[14] * m[3],
                mm[3] * m[0] + mm[7] * m[1] + mm[11] * m[2] + mm[15] * m[3],
                mm[0] * m[4] + mm[4] * m[5] + mm[8] * m[6] + mm[12] * m[7],
                mm[1] * m[4] + mm[5] * m[5] + mm[9] * m[6] + mm[13] * m[7],
                mm[2] * m[4] + mm[6] * m[5] + mm[10] * m[6] + mm[14] * m[7],
                mm[3] * m[4] + mm[7] * m[5] + mm[11] * m[6] + mm[15] * m[7],
                mm[0] * m[8] + mm[4] * m[9] + mm[8] * m[10] + mm[12] * m[11],
                mm[1] * m[8] + mm[5] * m[9] + mm[9] * m[10] + mm[13] * m[11],
                mm[2] * m[8] + mm[6] * m[9] + mm[10] * m[10] + mm[14] * m[11],
                mm[3] * m[8] + mm[7] * m[9] + mm[11] * m[10] + mm[15] * m[11],
                mm[0] * m[12] + mm[4] * m[13] + mm[8] * m[14] + mm[12] * m[15],
                mm[1] * m[12] + mm[5] * m[13] + mm[9] * m[14] + mm[13] * m[15],
                mm[2] * m[12] + mm[6] * m[13] + mm[10] * m[14] + mm[14] * m[15],
                mm[3] * m[12] + mm[7] * m[13] + mm[11] * m[14] + mm[15] * m[15]
            ])
        else:
            return Matrix(map (lambda x: x * m, self.matrix))

    def __truediv(self,m):
        return Matrix(map (lambda x: x / m, self.matrix))

    def __add(self,m):
        return Matrix(map (lambda x,y: x + y, self.matrix, m.matrix))

    def __sub(self,m):
        return Matrix(map (lambda x,y: x - y, self.matrix, m.matrix))
    
