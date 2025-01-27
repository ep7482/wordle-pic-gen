from PIL import Image, ImageFilter
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import itertools
from math import floor
import wordle_solver as bot
import time as time
import random



GREEN = (77, 149, 70)
YELLOW = (181, 159, 59)
DARK_GRAY = (58, 58, 60)

color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))

test_file = "images/test1.jpg"

def image_mat(file, lower_bound, middle_bound, save=False):
    img = Image.open(file)
    greyImg = Image.open(file).convert('L')
    
    width, height = img.size
    imgMatrix = []

    for x in range(width):
        temp = []
        for y in range(height):
            if greyImg.getpixel((x, y)) < int(255*lower_bound):
                greyImg.putpixel((x, y), 0)
                temp.append(0)
                img.putpixel((x, y), DARK_GRAY)
            elif greyImg.getpixel((x, y)) >= int(255*lower_bound) and greyImg.getpixel((x, y)) < int(255*middle_bound):
                greyImg.putpixel((x, y), 128)
                temp.append(1)
                img.putpixel((x, y), GREEN)
            else:
                greyImg.putpixel((x, y), 255)
                temp.append(2)
                img.putpixel((x, y), YELLOW)
        imgMatrix.append(temp)

    if save:
        img.save("images/newColorImage.jpg")
        greyImg.save("images/greyOuputImage.jpg")
    imgMatrix = np.array(imgMatrix)
    return imgMatrix

def coarseImage(matrix, coarseVal):
    width, height = len(matrix), len(matrix[0])
    newWidth, newHeight = width//coarseVal, height//coarseVal

    coarseMatrix = []
    coarseMatplot = np.zeros((newWidth, newHeight))
    for x in range(newWidth):
        tempArray = []
        for y in range(newHeight):
            matrixChunk = matrix[x*coarseVal:(x+1)*coarseVal, y*coarseVal:(y+1)*coarseVal]
            
            colorVal = mostCommonVal(matrixChunk)
            if colorVal == 0:
                tempArray.append(DARK_GRAY)
                coarseMatplot[x][y] = 0
            elif colorVal == 1:
                tempArray.append(GREEN)
                coarseMatplot[x][y] = 1
            else:
                tempArray.append(YELLOW)
                coarseMatplot[x][y] = 2
        coarseMatrix.append(tempArray)

    return coarseMatrix, coarseMatplot
    
def mostCommonVal(matrixChunk):
    flatChunk = matrixChunk.flatten()
    maxCountVal = -1
    for i in range(3):
        if maxCountVal < np.count_nonzero(flatChunk == i):
            maxCountVal = i
    return maxCountVal

def RGBtoColormap(color):
    return (color[0]/235, color[1]/235, color[2]/235)


cmap = matplotlib.colors.ListedColormap([RGBtoColormap(DARK_GRAY), RGBtoColormap(GREEN), RGBtoColormap(YELLOW)])
bounds=[-0.25,0.25,1.25,2]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

def viewImage(image_matrix):
    output_mat = np.flip(np.rot90(image_matrix, k=3), 1)
    plt.imshow(output_mat, cmap=cmap, norm=norm)
    plt.show()

def coarseFig(coarseN, rows, cols, image_matrix, save=False):
    fig, ax = plt.subplots(nrows=rows, ncols=cols)

    for i in range(2):
        for j in range(3):
            newCoarseMatplot = coarseImage(image_matrix, coarseN[i][j])[1]
            
            newCoarseMatplot = np.flip(np.rot90(newCoarseMatplot, k=3), 1)
            xNum, yNum = len(newCoarseMatplot)//2, len(newCoarseMatplot[0])//2

            ax[i,j].imshow(newCoarseMatplot, cmap= cmap, norm=norm)
    if save:
        plt.savefig(f'images/outputCoarseImage.png')
    plt.show()

def divideImg(image_matrix, coarseVal):
    newCoarseMatplot = coarseImage(image_matrix, coarseVal)[1]
    output_mat = np.flip(np.rot90(newCoarseMatplot, k=3), 1)

    imgRowNum = len(output_mat)
    imgColNum = len(output_mat[0])
    totRows = floor(imgRowNum/6)
    totCols = floor(imgColNum/5)
    print(totRows, totCols)
    newMat = output_mat[:int(totRows*6), :int(totCols*5)]

    pieces = []
    for x in range(totRows):
        inner_mat = []
        for y in range(totCols):
            inner_mat.append(newMat[int(6*x):int(6*(x+1)),int(5*y):int(5*(y+1))])
        pieces.append(inner_mat)
    return newMat, pieces

def divideImgPlot(image_matrix, pieces):
    ax = plt.axes()
    plt.imshow(image_matrix, cmap=cmap, norm=norm)
    ax.set_yticks([i*6 for i in range(len(pieces))])
    ax.set_xticks([i*5 for i in range(len(pieces[0]))])
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    plt.grid(color="white", linestyle=':')
    plt.show()

coarseN = [[1, 3, 9],
          [27, 64, 81]]

imgMatrix = image_mat(test_file, lower_bound=0.4, middle_bound=0.7)
# coarseFig(coarseN, 2, 3,imgMatrix , save=True)

# testMat, pieces = divideImg(imgMatrix, 3)

# divideImgPlot(testMat, pieces)

# 
# other_file = "images/lava-flow.jpg"
# mat = image_mat(other_file, 0.4, 0.6)
# newCoarseMatplot = coarseImage(mat, 3)[1]
# testMat, pieces = divideImg(newCoarseMatplot, 3)
# divideImgPlot(testMat, pieces)


# other_file = "images/wave.jpg"
# mat = image_mat(other_file, 0.4, 0.7)
# newCoarseMatplot = coarseImage(mat, 3)[1]
# testMat, pieces = divideImg(newCoarseMatplot, 3)
# divideImgPlot(testMat, pieces)


other_file = "images/Pug-dog.jpg"
mat = image_mat(other_file, 0.35, 0.5)
coarseImg = coarseImage(mat, 3)[1]
testMat, pieces = divideImg(mat, 3)
# divideImgPlot(testMat, pieces)

# for i in range(len(pieces)):
#     for j in range(len(pieces[0])):
#         print(pieces[i][j])

piece = pieces[0][0]
wordle_space = bot.wordle_words
guess_space = bot.guess_words
word_of_day = random.choice(wordle_space)
print(word_of_day)


print(piece)





# print(piece[0])

# ZERO =  np.array([0, 0, 0, 0, 0])
# ONES = np.array([1, 1, 1, 1, 1])
# TWOS = np.array([2, 2, 2, 2, 2])
# print((piece[0] == ONES).all())



# guess_words = []
# if (piece[0] == ZERO).all():
#     guess = "FUZZY"
#     if bot.comparison(guess, word_of_day) == (0, 0, 0, 0, 0):
#         guess_words.append(guess)


# coarseFig([[1, 2, 3],[4, 5, 6]], 2, 3, coarseImg)
# viewImage(coarseImg)

# combo_dict = {i : set() for i in range(10000)}
# for combo in combination_list:
#     tot = 0

#     for i, val in enumerate(combo):
        # tot += val * ((i * i) + 1)
        
#         tot += val * ((i ** 3) + i**2 + 1) 

#     combo_dict[tot].add(combo)

# for key in combo_dict.keys():
#     if len(combo_dict[key]) != 0:
#         print(combo_dict[key])

