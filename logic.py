from itertools import combinations

import requests


def logic(lines: list[str]):
    points: list[tuple[float, float, int]] = []

    print('Получаем данные...')
    for line in lines:
        query = line.strip().replace('.', '').replace(',', '').replace('д', '').split()
        query = '+'.join(query)
        params = dict(q=query, format='json', extratags=1, limit=40)
        request = requests.get('https://nominatim.openstreetmap.org/search.php', params=params)
        request.raise_for_status()

        results: list = request.json()
        for result in results:
            extratags = result['extratags']
            if 'building:levels' not in extratags:
                continue
            level = int(extratags['building:levels'])
            lat = float(result['lat'])
            lon = float(result['lon'])
            point = (float(lat), float(lon), level)
            points.append(point)
            break

    length = 0
    for point in points:
        _, _, level = point
        print(f"Заложенная высота: {level} * 3 * 2 = {level * 3 * 2}")
        length += level * 3 * 2
    for first, second in combinations(points, 2):
        lat1, lon1, _ = first
        lat2, lon2, _ = second
        distance = (abs(lat1 - lat2) + abs(lon1 - lon2)) * 111.3 * 1000
        print(
            f"Первая точка: {lat1}, {lon1}\n"
            f"Вторая точка: {lat2}, {lon2}\n"
            f"Дистанция: {distance}\n"
        )
        length += distance
    print(f'Длина кабеля: {length} метров')

    return f'{length:.5f} метров', points
