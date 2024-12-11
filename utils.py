def map_to_int8t(x: float, min_val: float, max_val: float) -> int:
    norm = (x - min_val) / (max_val - min_val)
    return int(norm * 255) - 128


def int_to_uint8t(x: int) -> int:
    return x & 0xFF


if __name__ == "__main__":
    print(map_to_int8t(0, 0, 1))
    print(int_to_uint8t(0))
