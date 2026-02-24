def parse_indexes(raw: str, max_len: int) -> list[int]:
    result: set[int] = set()

    for part in raw.split(","):
        part = part.strip()

        if "-" in part:
            start, end = part.split("-", 1)
            if start.isdigit() and end.isdigit():
                for i in range(int(start), int(end) + 1):
                    if 0 <= i < max_len:
                        result.add(i)

        elif part.isdigit():
            i = int(part)
            if 0 <= i < max_len:
                result.add(i)

    return sorted(result)
