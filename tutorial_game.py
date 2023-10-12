import random
import pyasge
from coordinate import Coord
from gamedata import GameData


def isInside(sprite, mouse_x, mouse_y) -> bool:
    bounds = sprite.getWorldBounds()

    if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v2.y:
        return True

    return False


def f(x):
    while x > 180:
        x -= 360
    while x < -180:
        x += 360
    x = (x / 180) * 3.1414794921875
    k = x
    c = 2
    for i in range(1, 3):
        c = c * (2 * i + 1)
        k += ((-1) ** i) * (x ** (2 * i + 1)) / c
        c = c * (2 * (i + 1))
    return k


def sin(x):
    x = (x - 180) % 360 - 180
    if -180 <= x < -90:
        return -f(x + 180)
    elif -90 <= x < 0:
        return -f(-x)
    elif 0 <= x < 90:
        return f(x)
    else:
        return f(180 - x)


def cos(x):
    return sin(90 - x)


class Fish(pyasge.Sprite):
    def __init__(self):
        pyasge.Sprite.__init__(self)
        self.velocity = Coord(0, 0)

    #  Remove this Class
    def updatePosition(self) -> None:
        self.x += self.velocity.x
        self.y += self.velocity.y


class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BURLYWOOD)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        # This is a comment
        self.data.background = pyasge.Sprite()
        self.initBackground()

        #
        self.menu_text = None
        self.initMenu()

        #
        self.scoreboard = None
        self.initScoreboard()

        # This is a comment
        self.fish = []
        self.timePassed = 0
        self.fishSpawnCounter = 60
        self.fishNet = (self.data.game_res[0] - 128, self.data.game_res[1] - 128)

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):
            self.data.background.z_order = -100
            return True
        return False

    def initFish(self, fish_index) -> bool:
        if self.fish[fish_index].loadTexture("/data/images/kenney_fishpack/fishTile_073.png"):
            self.fish[fish_index].z_order = 1
            self.fish[fish_index].scale = 1
            self.spawn(fish_index)

            return True

        return False

    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.x = 1300
        self.scoreboard.y = 75
        self.scoreboard.string = str(self.data.score).zfill(6)

    def initMenu(self) -> bool:
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "The Fish Game"
        self.menu_text.position = [100, 100]
        self.menu_text.colour = pyasge.COLOURS.HOTPINK

        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = "START<"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.HOTPINK

        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "EXIT "
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        return True

    def clickHandler(self, event: pyasge.ClickEvent) -> bool:
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and \
                event.button == pyasge.MOUSE.MOUSE_BTN1:

            for i in range(len(self.fish)):
                if isInside(self.fish[i], event.x, event.y):
                    self.fish.pop(i)

                    if not self.fish:
                        self.menu = True

                    return True

            self.timePassed += 10

        return False

    def keyHandler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:

            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 0:
                    self.play_option.string = "START<"
                    self.play_option.colour = pyasge.COLOURS.HOTPINK
                    self.exit_option.string = "EXIT "
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                else:
                    self.play_option.string = "START "
                    self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.exit_option.string = "EXIT<"
                    self.exit_option.colour = pyasge.COLOURS.HOTPINK

            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.menu_option == 0:
                    self.startGame()
                    self.menu = False
                else:
                    self.signalExit()

            if event.key == pyasge.KEYS.KEY_ESCAPE:
                if self.menu:
                    self.signalExit()
                else:
                    self.menu = True
                    self.data.score = 0

            if event.key == pyasge.KEYS.KEY_S:
                self.spawn(random.randint(0, len(self.fish) - 1))

    def spawn(self, fish_index) -> None:
        self.fish[fish_index].x = random.randint(0, self.data.game_res[0] - self.fish[fish_index].width)
        self.fish[fish_index].y = random.randint(0, self.data.game_res[1] - self.fish[fish_index].height)
        magnitude = random.randint(0, 50) / 10
        direction = random.randint(0, 359)

        self.fish[fish_index].velocity.set(
            magnitude * cos(direction),
            magnitude * sin(direction)
        )

    def trackTimePassage(self) -> None:
        self.timePassed += 1
        self.fishSpawnCounter -= 1
        if self.timePassed % 60 == 0:
            self.data.score += 1
            self.scoreboard.string = str(self.data.score).zfill(6)

        if self.fishSpawnCounter == 0:
            self.fish.append(Fish())
            self.initFish(-1)
            self.fishSpawnCounter = (20 * len(self.fish)) - self.data.score

    def updateFishCollisions(self) -> None:
        for a in self.fish:
            #  collisions with each other
            for b in self.fish:
                if a == b:
                    continue

                vector = Coord(
                    b.x - a.x,
                    b.y - a.y
                )

                if abs(vector.x) <= a.width and abs(vector.y) <= a.height:
                    Ua = a.velocity.i("/", vector)
                    Ub = b.velocity.i("/", vector)
                    Va = Coord((Ub.x + 9 * Ua.x) / 10, Ua.y)
                    Vb = Coord((Ub.x * 9 + Ua.x) / 10, Ub.y)

                    a.velocity = Va.i("*", vector)
                    b.velocity = Vb.i("*", vector)

                    a.updatePosition()
                    b.updatePosition()

                    while abs(vector.x) <= a.width and abs(vector.y) <= a.height:
                        a.updatePosition()
                        b.updatePosition()

                        vector.set(
                            b.x - a.x,
                            b.y - a.y
                        )

            #  collisions with walls
            if a.x < 0:
                a.x += self.fishNet[0]
            elif a.x > self.fishNet[0]:
                a.x -= self.fishNet[0]
            if a.y < 0:
                a.y += self.fishNet[1]
            elif a.y > self.fishNet[1]:
                a.y -= self.fishNet[1]

    def startGame(self) -> None:
        # This is a comment
        self.fish = [Fish() for _ in range(10)]
        for i in range(10):
            self.initFish(i)
        self.timePassed = 0
        self.scoreboard.string = "000000"
        self.data.score = 0
        self.fishSpawnCounter = 60

    def update(self, game_time: pyasge.GameTime) -> None:
        if self.menu:
            # update the menu here
            pass
        else:
            self.trackTimePassage()
            for fish in self.fish:
                fish.updatePosition()
            # update the game here

    """
        This is the variable time-step function. Use to update
        animations and to render the game-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """
    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.data.background)

        if self.menu:
            # render the menu here
            self.data.renderer.render(self.menu_text)

            self.data.renderer.render(self.play_option)
            self.data.renderer.render(self.exit_option)

            if self.data.score != 0:
                self.data.renderer.render(self.scoreboard)
        else:
            # render the game here
            self.data.renderer.render(self.scoreboard)
            for fish in self.fish:
                self.data.renderer.render(fish)


def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
