from PIL import Image, ImageDraw


class Depiction:
    BLACK = "black"
    WHITE = "white"
    GREEN = "green"
    RED = "red"

    FORMAT = "RGB"

    def __init__(
            self,
            columns,
            rows,
            thickness=4,
            background_color=WHITE,
            line_color=BLACK
    ):
        self.columns = columns
        self.rows = rows
        self.background_color = background_color
        self.line_color = line_color

        self.thickness = thickness
        self.width = self.columns * self.thickness * 2 + self.thickness
        self.height = self.rows * self.thickness * 2 + self.thickness

        self.grid = self._make_grid()

    def _make_grid(self):
        grid = Image.new("RGB", (self.width, self.height), self.background_color)

        for x in range(0, self.columns + 1):
            x0, y0, x1, y1 = x * self.thickness * 2, 0, x * self.thickness * 2 + self.thickness - 1, self.height
            column = (x0, y0), (x1, y1)
            ImageDraw.Draw(grid).rectangle(column, self.line_color, width=0)

        for y in range(0, self.rows + 1):
            x0, y0, x1, y1 = 0, y * self.thickness * 2, self.width, y * self.thickness * 2 + self.thickness - 1
            row = (x0, y0), (x1, y1)
            ImageDraw.Draw(grid).rectangle(row, self.line_color)

        return grid

    def generate_image(self, cells):
        cell1, cell2 = cells
        cell1_coordinates = cell1.coordinates()
        cell2_coordinates = cell2.coordinates()

        if cell1_coordinates[0] == cell2_coordinates[0]:
            column = min(cell1_coordinates[1], cell2_coordinates[1])
            row = cell1_coordinates[0]
            x0 = (column + 1) * self.thickness * 2
            y0 = row * self.thickness * 2 + self.thickness
            x1 = x0 + self.thickness - 1
            y1 = y0 + self.thickness - 1
            wall = (x0, y0), (x1, y1)
            ImageDraw.Draw(self.grid).rectangle(wall, self.background_color, width=0)

        # Remove horizontal walls
        if cell1_coordinates[1] == cell2_coordinates[1]:
            column = cell1_coordinates[1]
            row = min(cell1_coordinates[0], cell2_coordinates[0])
            x0 = column * self.thickness * 2 + self.thickness
            y0 = (row + 1) * self.thickness * 2
            x1 = x0 + self.thickness - 1
            y1 = y0 + self.thickness - 1
            wall = (x0, y0), (x1, y1)
            ImageDraw.Draw(self.grid).rectangle(wall, self.background_color)

        return self.grid

    def put_dots(self):
        ImageDraw.Draw(self.grid).rectangle(
            (self.thickness, self.thickness, self.thickness * 2 - 1, self.thickness * 2 - 1),
            fill=self.RED)
        ImageDraw.Draw(self.grid).rectangle(
            (self.width - self.thickness * 2, self.height - self.thickness * 2, self.width - self.thickness - 1, self.height - self.thickness - 1),
            fill=self.GREEN)
        return self.grid