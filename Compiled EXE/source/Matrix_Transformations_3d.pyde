transformation = []
with open('matrix.txt') as f:
    for row in f:
        transformation.append(list(map(lambda x: float(x), row.split(' '))))

def matmult(m1, m2):
    if len(m1[0]) != len(m2):
        return None
    newm = []
    for x in range(len(m1)):
        row = []
        for y in range(len(m2[0])):
            cell = 0
            for i in range(len(m1[0])):
                cell += (m1[x][i] * m2[i][y])
            row.append(cell)
        newm.append(row)
    return newm


def reset():
    global cube, gridxy_ending, gridxy_starting, gridxz_starting, gridxz_ending, gridyz_starting,  gridyz_ending

    cube = [[-1000, -1000, -1000, -1000, -1000, -1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, -1000, -1000, -1000, 1000, 1000, -1000, -1000, 1000, 1000, -1000],
            [-1000, 1000, 1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, -1000, -1000, 1000, 1000, -1000, -1000],
            [-1000, -1000, 1000, 1000, 1000, -1000, -1000, 1000, 1000, -1000, -1000, 1000, 1000, -1000, -1000, 1000, -1000, -1000, -1000, -1000, 1000, 1000, 1000, 1000]]

    gridxy_starting = [list(r) for r in zip(*list(zip(21*[-1000] + list(range(-1000, 1001, 100)),
                                                      list(range(-1000, 1001, 100)) + 21*[1000], 42*[0]))[::-1])]

    gridxz_starting = [list(r) for r in zip(*list(zip(21*[-1000] + list(range(-1000, 1001, 100)),
                                                      42*[0], list(range(-1000, 1001, 100)) + 21*[1000]))[::-1])]

    gridyz_starting = [list(r) for r in zip(*list(zip(42*[0], 21*[-1000] + list(range(-1000, 1001, 100)),
                                                      list(range(-1000, 1001, 100)) + 21*[1000]))[::-1])]

    gridxy_ending = [list(r) for r in zip(*list(zip(21*[1000] + list(range(-1000, 1001, 100)),
                                                list(range(-1000, 1001, 100)) + 21*[-1000], 42*[0]))[::-1])]

    gridxz_ending = [list(r) for r in zip(*list(zip(21*[1000] + list(range(-1000, 1001, 100)),
                                                42*[0], list(range(-1000, 1001, 100)) + 21*[-1000]))[::-1])]

    gridyz_ending = [list(r) for r in zip(*list(zip(42*[0], 21*[1000] + list(range(-1000, 1001, 100)),
                                                list(range(-1000, 1001, 100)) + 21*[-1000]))[::-1])]


def startagain(transformation):
    global after_cube, dist_cube

    after_cube = matmult(transformation, cube)

    dist_cube = [(x[1] - x[0], y[1] - y[0], z[1] - z[0]) for x, y, z in
                     zip(zip(cube[0], after_cube[0]), zip(cube[1], after_cube[1]), zip(cube[2], after_cube[2]))]


def move(before, after, dist_):
    for i in range(len(before[0])):
        x1, y1, z1, x2, y2, z2 = before[0][i], before[1][i], before[2][i], after[0][i], after[1][i], after[2][i]
        X, Y, Z = dist_[i]
        if dist(x1, y1, z1, x2, y2, z2) < dist(0, 0, 0, X, Y, Z) / 100:
            before[0][i] = x2
            before[1][i] = y2
            before[2][i] = z2
            continue
        if x1 == x2 and y1 == y2 and z1 == z2: continue

        before[0][i] += X / 100

        before[1][i] += Y / 100

        before[2][i] += Z / 100


reset()

startagain(transformation)

scaleFactor = 0.2

def setup():
    global canvas
    size(1000, 1000, P3D)


def draw():
    background(0)
    translate(width/2, height/2)
    scale(scaleFactor, -scaleFactor, scaleFactor)
    rotateX(mouseY * TWO_PI / 1000)
    rotateZ(-mouseX * TWO_PI / 1000)
    strokeWeight(3)

    move(cube, after_cube, dist_cube)

    stroke(0,255,255)
    for a, b, c in zip(zip(gridxy_starting[0], gridxy_ending[0]), zip(gridxy_starting[1], gridxy_ending[1]), zip(gridxy_starting[2], gridxy_ending[2])):
        line(a[0], b[0], c[0], a[1], b[1], c[1])
    stroke(255,255,0)
    for a, b, c in zip(zip(gridxz_starting[0], gridxz_ending[0]), zip(gridxz_starting[1], gridxz_ending[1]), zip(gridxz_starting[2], gridxz_ending[2])):
        line(a[0], b[0], c[0], a[1], b[1], c[1])
    stroke(255,0,0)
    for a, b, c in zip(zip(gridyz_starting[0], gridyz_ending[0]), zip(gridyz_starting[1], gridyz_ending[1]), zip(gridyz_starting[2], gridyz_ending[2])):
        line(a[0], b[0], c[0], a[1], b[1], c[1])

    stroke(0,255,0)
    line(-1000, 0, 0, 1000, 0, 0)
    line(0, 1000, 0, 0, -1000, 0)
    line(0, 0, -1000, 0, 0, 1000)
    stroke(255)
    beginShape(QUADS)
    lights()
    fill(255, 255, 255, 127)
    for x, y, z in zip(cube[0], cube[1], cube[2]):
        vertex(x, y, z)
    endShape()


def mousePressed():
    if mouseButton == LEFT:
        startagain(transformation)
    elif mouseButton == RIGHT:
        reset()
        startagain(transformation)
        
def mouseWheel(event):
    global scaleFactor
    scaleFactor += -0.01 * event.getCount()
