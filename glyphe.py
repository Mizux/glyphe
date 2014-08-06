#!/usr/bin/env python2
import itertools
import shlex, subprocess

# List all glyphe which contain strictly 3 empty cells
# Each value is the index of an empty cell

# A Glyphe is a 3x3 empty/filled cells
class Glyphe:
    def __init__(self, filename, size, value):
        self.filename_ = filename
        self.size_ = size
        self.cells_ = list(itertools.repeat(value, 9))

    def add(self, idx):
        if (idx < len(self.cells_)-1):
            self.cells_[idx] = 1;
        return self

    def remove(self, idx):
        if (idx < len(self.cells_)):
            self.cells_[idx] = 0;
        return self

    def draw(self):
        cmd = "convert -size {0}x{0}".format(self.size_)
        cmd+= " -fill black -stroke black xc:white"

        for j in range(3):
            for i in range(3):
                if (self.cells_[i*3+j]):
                    cmd += " -draw \"rectangle {0},{1} {2},{3}\"".format(
                        j*self.size_/3,
                        i*self.size_/3,
                        (j+1)*self.size_/3,
                        (i+1)*self.size_/3)
        cmd += " " + self.filename_
        return cmd

    def draw_ascii(self):
        cmd = ""
        for i in range(3):
            if (i != 0):
                cmd += "\n"
            for j in range(3):
                if (self.cells_[i*3+j]):
                    cmd += "#"
                else:
                    cmd += " "
        return cmd

def test():
    for i in range(9):
        for j in range(i+1,9):
            for k in range(j+1,9):
                name="plop_"+`i`+"_"+`j`+"_"+`k`+".png"
                a=Glyphe(name, 256, 1)
                a.remove(i).remove(j).remove(k)
                args = shlex.split(a.draw())
                #print args
                subprocess.Popen(args)

if __name__ == '__main__':
    test()

