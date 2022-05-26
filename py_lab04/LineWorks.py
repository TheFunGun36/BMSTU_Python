def isEqual(a: float, b: float) -> bool:
    return abs(a - b) < 1e-10;

class Point(object):
    x: float = 0.0
    y: float = 0.0

    isHighlighted: bool
    isHovered: bool
    isChosen: bool

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

        self.isHighlighted = False
        self.isHovered = False
        self.isChosen = False

    def __eq__(self, other):
        return isEqual(self.x, other.x) and isEqual(self.y, other.y)


class Line(object):
    coefA: float = 0.0
    coefB: float = 0.0
    coefC: float = 0.0

    isHighlighted: bool
    isHovered: bool
    isChosen: bool

    def __init__(self, pointA: Point = None, pointB: Point = None):
        if pointA == pointB:
            raise ValueError("Cant build a line through one point")

        self.coefA = pointA.y - pointB.y
        self.coefB = pointB.x - pointA.x
        self.coefC = -(self.coefA * pointA.x + self.coefB * pointA.y)

        if self.coefA < 0.0:
            self.coefA *= -1.0;
            self.coefB *= -1.0;
            self.coefC *= -1.0;

        self.isHighlighted = False
        self.isHovered = False
        self.isChosen = False

    def __eq__(self, other):
        if isEqual(self.coefA, 0.0):
            return isEqual(other.coefA, 0.0) and isEqual(self.coefC, other.coefC)
        elif isEqual(self.coefB, 0.0):
            return isEqual(other.coefB, 0.0) and isEqual(self.coefC, other.coefC)
        elif isEqual(other.coefA, 0.0):
            return isEqual(self.coefA, 0.0) and isEqual(self.coefC, other.coefC)
        elif isEqual(other.coefB, 0.0):
            return isEqual(self.coefB, 0.0) and isEqual(self.coefC, other.coefC)
        elif isEqual(self.coefC, 0.0) and isEqual(0.0, other.coefC):
            return isEqual(self.coefA / other.coefA, self.coefB / other.coefB)
        else:
            return isEqual(self.coefA / other.coefA, self.coefB / other.coefB) and isEqual(self.coefC, other.coefC)

    def _equation(self, x: float, y: float) -> float:
        return self.coefA * x + self.coefB * y + self.coefC

    def isParallelTo(self, other):
        if not isEqual(other.coefA, 0) and not isEqual(other.coefB, 0):
            return isEqual(self.coefA / other.coefA, self.coefB / other.coefB)
        elif not isEqual(self.coefA, 0) and not isEqual(self.coefB, 0):
            return isEqual(other.coefA / self.coefA, other.coefB / self.coefB)
        return isEqual(other.coefA, self.coefA) or isEqual(other.coefB, self.coefB)

    def isBetweenPoints(self, pointA: Point, pointB: Point) -> bool:
        valueA = self._equation(pointA.x, pointA.y)
        valueB = self._equation(pointB.x, pointB.y)

        if isEqual(valueA, 0.0) or isEqual(valueB, 0.0):
            return False

        return valueA > 0.0 and valueB < 0.0 or valueA < 0.0 and valueB > 0.0

    def intercept(self, other) -> Point:
        if isEqual(self.coefA, 0.0) and isEqual(other.coefB, 0.0):
            x = -other.coefC / other.coefA
            y = -self.coefC / self.coefB
            return Point(x, y)
        elif isEqual(self.coefB, 0.0) and isEqual(other.coefA, 0.0):
            x = -self.coefC / self.coefA
            y = -other.coefC / other.coefB
            return Point(x, y)
        elif isEqual(self.coefA, 0.0) and isEqual(other.coefA, 0.0):
            return None
        elif isEqual(self.coefB, 0.0) and isEqual(other.coefB, 0.0):
            return None
        elif not isEqual(self.coefA, 0.0) and not isEqual(other.coefA, 0.0):
            y = other.coefC * self.coefA - self.coefC * other.coefA
            y /= self.coefB * other.coefA - other.coefB * self.coefA
            x = -(self.coefB * y + self.coefC) / self.coefA
            return Point(x, y)
        elif not isEqual(self.coefB, 0.0) and not isEqual(other.coefB, 0.0):
            x = other.coefC * self.coefB - self.coefC * other.coefB
            x /= self.coefA * other.coefB - other.coefA * self.coefB
            y = -(self.coefA * x + self.coefC) / self.coefB
            return Point(x, y)
        else:
            return None

    def findRectInterceptions(self, x1: float, y1: float, x2: float, y2: float) -> list[Point]:
        interceptions = []

        lines = [
            Line(Point(x1, y1), Point(x2, y1)),
            Line(Point(x2, y1), Point(x2, y2)),
            Line(Point(x2, y2), Point(x1, y2)),
            Line(Point(x1, y2), Point(x1, y1))
        ]

        for line in lines:
            result = self.intercept(line)

            if result is not None and x1 - 1e-10 <= result.x <= x2 + 1e-10 and y1 - 1e-10 <= result.y <= y2 + 1e-10:
                interceptions.append(result)

        i = 0

        while i < len(interceptions):
            j = i + 1

            while j < len(interceptions):
                if interceptions[i] == interceptions[j]:
                    interceptions.pop(j)
                else:
                    j += 1
            i += 1

        return interceptions

    def getOrthogonal(self, point: Point = Point(0, 0)):
        newA = self.coefB
        newB = -self.coefA
        newC = -(newA * point.x + newB * point.y)

        newLine = Line(Point(0, 0), Point(1, 1))
        newLine.coefA = newA
        newLine.coefB = newB
        newLine.coefC = newC

        return newLine


def countParallelLines(linesArray: list[Line], line) -> int:
    counter = -1

    for otherLine in linesArray:
        if line.isParallelTo(otherLine):
            counter += 1

    return counter


def findParallelLines(linesArray: list[Line], line) -> list[Line]:
    result = []

    for otherLine in linesArray:
        if line.isParallelTo(otherLine):
            result.append(otherLine)

    return result


def findLinesBetweenPoints(a: Point, b: Point, linesArray: list[Line]) -> list[Line]:
    result = []

    for line in linesArray:
        if line.isBetweenPoints(a, b):
            result.append(line)

    return result

def findSameLine(lineArray: list[Line], line: Line) -> Line:
    for otherLine in lineArray:
        if line == otherLine:
            return otherLine

    return None

def findSamePoint(pointArray: list[Point], point: Point) -> Point:
    for otherPoint in pointArray:
        if point == otherPoint:
            return otherPoint

    return None    
