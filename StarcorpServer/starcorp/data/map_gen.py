import random


from data import TileType


def generate(types, rows=20, cols=20):
    tiles = []

    for tile_type, count in types.items():
        for _ in range(count):
            tiles.append(tile_type)

    data = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(random.choice(tiles))

        data.append(row)

    return data


def display(data):

    string = []
    cols = len(data[0])
    string.append("#" * (cols + 2))
    for row in data:
        string.append(f"#{''.join(row)}#")
    string.append("#" * (cols + 2))

    return "\n".join(string)


def load(file_name):
    with open(file_name, "r") as map_file:
        string = map_file.read()

    string = string.replace("#", "")
    lines = string.split("\n")

    lines = lines[1:-1]  # Strip first and last

    data = []
    for line in lines:
        row = []
        for char in line:
            row.append(TileType(char))
        data.append(row)

    return data


RATIOS = {
    TileType.LUSH: 10,
    TileType.AQUATIC: 20,
    TileType.ARID: 50,
    TileType.SPACE: 3000,
    TileType.SOLAR: 1,
}


def main():
    data = generate(RATIOS)
    string = display(data)
    print(string)


if __name__ == "__main__":
    main()