class Vertex:
    def __init__(self, name: int, color=None):
        self.name = name
        self.color = color


class Edge:
    def __init__(self, name: str, start: Vertex, end: Vertex, weight: int):
        self.name = name
        self.start = start
        self.end = end
        self.weight = weight


class Graph:
    colors = {
        1: 'red',
        2: 'green',
        3: 'blue',
        4: 'orange',
        5: 'black'
    }

    def __init__(self, matrix: list):
        self.matrix = matrix
        self.edges = []
        self.vertexes = {}

        self._set_vertexes()
        self._set_edges()

    def _set_vertexes(self):
        """
        Create vertexes
        """
        for i in range(len(self.matrix)):
            self.vertexes[i + 1] = Vertex(i + 1)

    def get_edges_count(self):
        """
        return: total edges count of graph
        """
        edges_count = len(self.edges)

        return edges_count

    def get_vertexes_count(self):
        """
        return: total vertexes count of graph
        """
        vertexes_count = len(self.edges)

        return vertexes_count

    def paint_vertexes(self):
        """
        Paint vertexes
        """
        self.vertexes[1].color = 1
        for n in self.get_neighborus():
            neighbour_colors = set()
            for neighbour in self.get_neighborus()[n]:
                neighbour_colors.add(self.vertexes[neighbour].color if self.vertexes[neighbour].color else 0)
            self.vertexes[n].color = 1
            while self.vertexes[n].color in neighbour_colors:
                self.vertexes[n].color += 1

    def get_neighborus(self):
        """
        :return: dict with keys vertexes and list of it neighbours as value
        """
        neighborus_map = {}
        for vertex in self.vertexes:
            neighborus_map[vertex] = set()
            for edge in self.edges:
                if edge.start.name == vertex:
                    neighborus_map[vertex].add(edge.end.name)
                if edge.end.name == vertex:
                    neighborus_map[vertex].add(edge.start.name)

        return neighborus_map

    def _set_edges(self):
        """
        Add new edges into graph
        """
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                if int(self.matrix[row][col]) > 0 and not self._is_edge_exist(row + 1, col + 1):
                    edge = Edge(
                        start=self.vertexes[row + 1],
                        end=self.vertexes[col + 1],
                        name=f'{row + 1}-{col + 1}',
                        weight=int(self.matrix[row][col])
                    )
                    self.edges.append(edge)

    def _is_edge_exist(self, start: int, end: int) -> bool:
        """
        Checks exits this edge or not
        """
        for edge in self.edges:
            if edge.start.name == start and edge.end.name == end:
                return True
            if edge.start.name == end and edge.end.name == start:
                return True

        return False

    def get_edge_weight(self, start_vertex: int, end_vertex: int) -> int:
        """
        Return weight of edge
        """
        for edge in self.edges:
            if edge.start.name == start_vertex and edge.end.name == end_vertex or \
                    edge.end.name == start_vertex and edge.start.name == end_vertex:
                return edge.weight

        return 0

    def get_default_dict(self, len):
        """
        Build empty dict for road map
        """
        return {x+1: 0 for x in range(len)}

    def calculate_road(self):
        """
        Calculate the shortest way from each vertex for each other
        """
        result = {}
        for vertex in self.vertexes.values():
            result[vertex.name] = self.get_default_dict(len(self.vertexes))
            # primary filling
            for neighbour in self.vertexes.values():
                result[vertex.name][neighbour.name] = self.get_edge_weight(vertex.name, neighbour.name)

            # Clarify distance
            for neighbour_ex in self.vertexes.values():
                if neighbour_ex.name != vertex.name:
                    inithial_distance = result[vertex.name][neighbour_ex.name]
                    for neighbour_2 in self.vertexes.values():
                        if neighbour_2.name != vertex.name and neighbour_2.name != neighbour_ex.name:
                            current_distance = result[vertex.name][neighbour_2.name]
                            if self.get_edge_weight(neighbour_ex.name, neighbour_2.name):
                                new_distance = inithial_distance + self.get_edge_weight(neighbour_ex.name, neighbour_2.name)
                            else:
                                new_distance = self.get_edge_weight(neighbour_ex.name, neighbour_2.name)
                            if new_distance:
                                if current_distance:
                                    if new_distance < current_distance:
                                        result[vertex.name][neighbour_2.name] = new_distance
                                else:
                                    result[vertex.name][neighbour_2.name] = new_distance

        return result


def validate_item(el: str) -> None:
    """
    validate input data (elements)
    """
    if not el.strip().isdigit():
        raise TypeError('Elements has wrong type')
    if not el.strip().isdecimal():
        raise ValueError('Items may be int')
    if int(el) < 0:
        raise ValueError('Items may be positive int')


def check_row_size(row: list, length) -> None:
    """
    Validate input row length
    """
    if len(row) != length:
        raise ValueError(f'Row not equal with matrix_size = ({length})')


def transform_row(line: str, matrix_size: int) -> list:
    """
    Transform input line in list
    """
    line_row = line.split(',')
    if len(line_row) != matrix_size:
        raise ValueError(f'Row not equal with matrix_size = ({matrix_size})')
    formatted_row = []
    for el in line_row:
        validate_item(el)
        formatted_row.append(el)

    return formatted_row


if __name__ == '__main__':
    matrix_size = int(input("Please set matrix size: "))
    print('Input example: 1,0,1,0,1')
    matrix = []
    counter = 1
    while counter <= matrix_size:
        line = input(f'Set values for line {counter}: ')
        line_arr = transform_row(line, matrix_size)
        matrix.append(line_arr)
        counter += 1

    graph = Graph(matrix=matrix)

    # General data about graph
    for x in graph.edges:
        print(f'name - {x.name}, start - {x.start.name}, end - {x.end.name}, weight - {x.weight}')

    # Colored graph
    print(graph.get_neighborus())
    graph.paint_vertexes()
    for x in range(1, len(graph.vertexes) + 1):
        print(f'{graph.vertexes[x].name} - {Graph.colors[graph.vertexes[x].color]}')

    # Shortest ways
    ways = graph.calculate_road()
    for x in ways:
        print(f'vertex {x}. Roads map: {ways[x]}')

