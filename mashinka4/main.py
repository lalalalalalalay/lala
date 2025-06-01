import random
import copy
import openrouteservice
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Параметры генетического алгоритма
POP_SIZE = 50
GENERATIONS = 100
MUT_RATE = 0.1
CR_RATE = 0.8
TOURN_SIZE = 3
ELITE_COUNT = 2

# Глобальные данные
locations = []         # Список координат точек
priority_map = {}      # Приоритеты точек по индексу
dur_matrix = []        # Матрица времен
TIME_LIMIT = 20 * 60   # Лимит времени в секундах

# Профили маршрутов OpenRouteService
map_types = [
    "driving-car", "driving-hgv", "foot-walking",
    "foot-hiking", "cycling-regular", "cycling-road",
    "cycling-safe", "cycling-mountain", "cycling-tour", "cycling-electric"
]
map_type = map_types[0]


def eval_route(route):
    """
    Рассчитывает приоритет и длительность для маршрута.
    """
    if not route:
        return 0, 0
    total_prio = sum(priority_map.get(i, 0) for i in route)
    total_time = 0
    if len(route) > 1:
        for a, b in zip(route, route[1:]):
            total_time += dur_matrix[a][b]
    if total_time > TIME_LIMIT:
        return 0, total_time
    return total_prio, total_time


def make_route():
    """
    Создает случайный маршрут.
    """
    n = len(locations)
    if n == 0:
        return []
    k = random.randint(1, n)
    return random.sample(range(n), k)


def init_pop(size=POP_SIZE):
    return [make_route() for _ in range(size)]


def tournament_select(pop_fit):
    parents = []
    for _ in range(len(pop_fit)):
        tour = random.sample(pop_fit, TOURN_SIZE)
        winner = max(tour, key=lambda x: x[1][0])
        parents.append(winner[0])
    return parents


def do_crossover(p1, p2):
    if random.random() > CR_RATE:
        return p1.copy(), p2.copy()
    # Одноточечный срез
    if len(p1) > 1:
        i, j = sorted(random.sample(range(len(p1)), 2))
        seg = p1[i:j+1]
    else:
        seg = p1[:]
    child1 = seg + [x for x in p2 if x not in seg]
    child2 = seg + [x for x in p1 if x not in seg]
    return child1, child2


def apply_mutation(route):
    if random.random() > MUT_RATE or not route:
        return route
    r = route.copy()
    op = random.choice(['swap', 'insert', 'remove', 'add'])
    n = len(locations)
    if op == 'swap' and len(r) > 1:
        i, j = random.sample(range(len(r)), 2)
        r[i], r[j] = r[j], r[i]
    elif op == 'insert' and len(r) > 1:
        idx = random.randrange(len(r))
        val = r.pop(idx)
        r.insert(random.randrange(len(r)+1), val)
    elif op == 'remove' and r:
        r.pop(random.randrange(len(r)))
    elif op == 'add' and len(r) < n:
        choices = [i for i in range(n) if i not in r]
        r.insert(random.randrange(len(r)+1), random.choice(choices))
    return r


def run_ga():
    pop = init_pop()
    best_route, best_prio, best_time = [], -1, float('inf')
    for gen in range(GENERATIONS):
        scored = [(ind, eval_route(ind)) for ind in pop]
        scored.sort(key=lambda x: x[1][0], reverse=True)
        top, (tp, tt) = scored[0]
        if tp > best_prio:
            best_route, best_prio, best_time = top.copy(), tp, tt
            print(f"Поколение {gen}: новый рекорд приоритета {best_prio}, время {best_time:.1f}s")
        # Элитизм
        next_pop = [ind for ind, _ in scored[:ELITE_COUNT]]
        parents = tournament_select(scored)
        while len(next_pop) < POP_SIZE:
            p1, p2 = random.sample(parents, 2)
            c1, c2 = do_crossover(p1, p2)
            next_pop.append(apply_mutation(c1))
            if len(next_pop) < POP_SIZE:
                next_pop.append(apply_mutation(c2))
        pop = next_pop
    return best_route, best_prio, best_time


def main():
    global locations, priority_map, dur_matrix
    # Начальные данные — мои координаты в Нью-Йорке
    raw = [
        {'coords': (40.7580, -73.9855), 'priority': 10},  # Times Square
        {'coords': (40.7061, -74.0087), 'priority': 8},   # Wall Street
        {'coords': (40.7295, -73.9965), 'priority': 15},  # Washington Square Park
        {'coords': (40.7527, -73.9772), 'priority': 20},  # Grand Central
        {'coords': (40.7069, -74.0113), 'priority': 5},   # One World Trade Center
        {'coords': (40.7484, -73.9857), 'priority': 25},  # Empire State Building
        {'coords': (40.7812, -73.9665), 'priority': 12}   # Central Park
    ]
    # Привести к (lon, lat)
    locations = [(p['coords'][1], p['coords'][0]) for p in raw]
    priority_map = {i: p['priority'] for i, p in enumerate(raw)}

    client = openrouteservice.Client(key='5b3ce3597851110001cf624849b43a0299834c198e8502bd4df10db6')
    matrix_response = client.distance_matrix(
        locations=locations,
        profile=map_type,
        metrics=['duration']
    )
    dur_matrix = matrix_response['durations']

    route, prio, dur = run_ga()
    print(f"Лучший маршрут: {route}")
    print(f"Суммарный приоритет: {prio}")
    print(f"Общее время: {dur/60:.2f} мин")

    if route:
        coords = [locations[i] for i in route]
        geo = client.directions(
            coordinates=coords,
            profile=map_type,
            format='geojson'
        )
        gdf = gpd.GeoDataFrame.from_features(geo['features'], crs='EPSG:4326').to_crs(epsg=3857)
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, linewidth=4)
        all_pts = gpd.GeoDataFrame(
            geometry=gpd.points_from_xy(
                [c[0] for c in locations], [c[1] for c in locations]
            ), crs='EPSG:4326'
        ).to_crs(epsg=3857)
        all_pts.plot(ax=ax, markersize=50, alpha=0.4)
        sel_pts = gpd.GeoDataFrame(
            geometry=gpd.points_from_xy(
                [coords[i][0] for i in range(len(coords))],
                [coords[i][1] for i in range(len(coords))]
            ), crs='EPSG:4326'
        ).to_crs(epsg=3857)
        sel_pts.plot(ax=ax, markersize=100)
        for idx, pt in enumerate(sel_pts.geometry):
            ax.text(pt.x, pt.y, str(idx+1), fontsize=9, bbox=dict(facecolor='yellow', alpha=0.5))
        ctx.add_basemap(ax)
        ax.set_axis_off()
        plt.title(f"Опт. маршрут: приоритет {prio}, время {dur/60:.1f} мин")
        plt.show()

if __name__ == '__main__':
    main()
