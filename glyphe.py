#!/usr/bin/env python2
import itertools
import shlex, subprocess

# List all glyphe which contain strictly 3 empty cells
# Each value is the index of an empty cell

# A Glyphe is a WidthxHeight empty/filled cells
class Glyphe:
    def __init__(self, width, height, value):
        self.width_ = width
        self.height_ = height
        self.cells_ = list(itertools.repeat(value, width*height))
        self.index = len(self.cells_)

    def __iter__(self):
        return self

    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.cells_[self.index]

    def add(self, i, j):
        if (i+j*self.width_ < len(self.cells_)):
            self.cells_[i+j*self.width_] = 1;
        return self

    def add(self, idx):
        if (idx < len(self.cells_)):
            self.cells_[idx] = 1;
        return self

    def remove(self, i, j):
        if (i+j*self.width_ < len(self.cells_)):
            self.cells_[i+j*self.width_] = 0;
        return self

    def remove(self, idx):
        if (idx < len(self.cells_)):
            self.cells_[idx] = 0;
        return self

    def draw(self, filename, size):
        cmd = "convert -size {0}x{0}".format(size)
        cmd+= " xc:white -fill black -stroke black"

        for j in range(self.height_):
            for i in range(self.width_):
                if (self.cells_[j*self.width_+i] == 1):
                    cmd += " -draw \"rectangle {0},{1} {2},{3}\"".format(
                        i*size/self.width_,
                        j*size/self.height_,
                        (i+1)*size/self.width_,
                        (j+1)*size/self.height_)
        cmd += " " + filename
        return cmd

    def draw_ascii(self):
        cmd = ""
        for j in range(self.height_):
            if (i != 0):
                cmd += "\n"
            for i in range(self.width_):
                if (self.cells_[j*self.width_+i]):
                    cmd += "#"
                else:
                    cmd += " "
        return cmd

# A Glyphe should contain strictly 3 or 4 empty cell
def rule_0(glyphe):
    count =0
    for i in range(len(glyphe.cells_)):
        if (glyphe.cells_[i] == 0):
            count += 1
    if (count == 3 or count == 4):
        return True
    else:
        return False

# a Glyphe can't contain the pattern:
# -----    -----
# |B|W|    |W|B|
# ----- or -----
# |W|B|    |B|W|
# -----    -----
def rule_1(glyphe):
    for j in range(glyphe.height_ - 1):
        for i in range(glyphe.width_ - 1):
            if (glyphe.cells_[i+j*glyphe.width_] == glyphe.cells_[i+1+(j+1)*glyphe.width_] and
                    glyphe.cells_[i+1+j*glyphe.width_] ==  glyphe.cells_[i+(j+1)*glyphe.width_] and
                    glyphe.cells_[i+j*glyphe.width_] != glyphe.cells_[i+1+j*glyphe.width_]):
                return False
    return True

def genGlypheEmpty_3(width, height):
    for i in range(width*height):
        for j in range(i+1,width*height):
            for k in range(j+1,width*height):
                g = Glyphe(width, height, 1)
                g.remove(i).remove(j).remove(k)
                yield [g, i, j, k]

def genGlypheEmpty_4(width, height):
    for i in range(width*height):
        for j in range(i+1,width*height):
            for k in range(j+1,width*height):
                for l in range(k+1,width*height):
                    g = Glyphe(width, height, 1)
                    g.remove(i).remove(j).remove(k).remove(l)
                    yield [g, i, j, k, l]

def test():
    name = "plop_"
    #for it in genGlypheEmpty_3(3,3):
    #    if (rule_0(it[0]) and rule_1(it[0])):
    #            filename = name+`it[1]`+"_"+`it[2]`+"_"+`it[3]`+".png"
    #            #print it[0].draw(filename, 256)
    #            args = shlex.split(it[0].draw(filename, 256))
    #            subprocess.Popen(args)
    for it in genGlypheEmpty_4(3,3):
        if (rule_0(it[0]) and rule_1(it[0])):
                filename = name+`it[1]`+"_"+`it[2]`+"_"+`it[3]`+"_"+`it[4]`+".png"
                #print it[0].draw(filename, 256)
                args = shlex.split(it[0].draw(filename, 256))
                subprocess.Popen(args)

if __name__ == '__main__':
    test()

