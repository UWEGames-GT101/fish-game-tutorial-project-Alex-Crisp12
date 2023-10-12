class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return tuple((self.x, self.y))

    def set(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        print(self.x, self.y)

    def display_coord(self):
        print("(" + str(self.x) + ", " + str(self.y) + ")")

    def display_complex(self):
        match self.x, self.y:
            case 0, 0:
                print("0")
            case 0, 1:
                print("i")
            case 0, -1:
                print("-i")
            case 0, b:
                print(str(b) + "i")
            case a, 0:
                print(a)
            case a, 1:
                print(str(a) + "+i")
            case a, -1:
                print(str(a) + "-i")
            case a, b:
                if b < 0:
                    print(str(a) + str(b) + "i")
                else:
                    print(str(a) + "+" + str(b) + "i")

    def add(self, target):
        t = target.get_tuple()
        return Coord(
            self.x + t[0],
            self.y + t[1]
        )

    def sub(self, target):
        return self.add(target.prod(-1))

    def prod(self, coefficient):
        return Coord(
            self.x * coefficient,
            self.y * coefficient
        )

    def div(self, denominator):
        return Coord(
            self.x / denominator,
            self.y / denominator
        )

    def round(self, decimals=0):
        return Coord(
            round(self.x, decimals),
            round(self.y, decimals)
        )

    def magnitude(self):
        return self.x ** 2 + self.y ** 2

    def conjugate(self):
        return Coord(self.x, -self.y)

    def reciprocal(self):
        return self.conjugate().div(self.magnitude())

    def i(self, operation, target):
        match operation:
            case "+":
                return self.add(target)
            case "-":
                return self.sub(target)
            case "*" | "x":
                t = target.get_tuple()
                return Coord(
                    self.x * t[0] - self.y * t[1],
                    self.x * t[1] + self.y * t[0]
                )
            case "/":
                return self.i("*", target.reciprocal())

    def exp(self, power):
        if power == 1:
            return self
        elif power == 0:
            return Coord(1, 0)
        else:
            return self.i("*", self.exp(power - 1))
