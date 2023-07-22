from api.v1.task.serializers import TaskSerializer
from task.maze.maze import Maze
from task.maze.maze_depiction import MazeDepiction
from task.maze.utils import convert_to_64


def generate_image_stream(rows, columns, scale, algorithm, step=20):
    maze = Maze(
        rows=rows,
        columns=columns
    )
    depiction = MazeDepiction(
        rows=maze.rows,
        columns=maze.columns,
        thickness=scale
    )

    for i, cells in enumerate(maze.generate_maze(algorithm)):
        image = depiction.generate_image(cells)
        if i % step == 0:
            yield convert_to_64(image)
    else:
        depiction.put_dots()
        yield convert_to_64(image)

def prepare_data(db_task, **kwargs):
    data = TaskSerializer(db_task).data
    data |= kwargs
    return data
