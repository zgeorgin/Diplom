import numpy as np


class Particle:
    def __init__(self, position, charge):
        self.position = np.array(position)  # Координаты частицы (x, y)
        self.charge = charge                # Заряд частицы
        self.potential = 0                  # Потенциал в данной точке

class Cluster:
    def __init__(self, particles, level, bounds):
        self.particles = particles          # Частицы в кластере
        self.level = level                  # Уровень иерархии
        self.bounds = bounds                # Границы кластера [xmin, xmax, ymin, ymax]
        self.children = []                  # Дочерние кластеры
        self.center = np.mean(bounds.reshape(2, 2), axis=1)  # Центр кластера
        self.multipole_moment = 0           # Мультипольный момент
        self.local_expansion = 0            # Локальное разложение
        
def build_tree(particles, max_particles, level, bounds):
    cluster = Cluster(particles, level, bounds)
    if len(particles) > max_particles:
        xmin, xmax, ymin, ymax = bounds
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        bounds_children = [
            [xmin, xmid, ymin, ymid],  # Нижний левый
            [xmid, xmax, ymin, ymid],  # Нижний правый
            [xmin, xmid, ymid, ymax],  # Верхний левый
            [xmid, xmax, ymid, ymax],  # Верхний правый
        ]

        particles_children = [[] for _ in range(4)]

        for p in particles:
            x, y = p.position
            index = 0
            if x > xmid:
                index += 1
            if y > ymid:
                index += 2
            particles_children[index].append(p)

        for i in range(4):
            if particles_children[i]:
                child = build_tree(particles_children[i], max_particles, level+1, np.array(bounds_children[i]))
                cluster.children.append(child)
    return cluster

def well_separated(cluster_a, cluster_b):
    distance = np.linalg.norm(cluster_a.center - cluster_b.center)
    size_a = max(cluster_a.bounds[1] - cluster_a.bounds[0], cluster_a.bounds[3] - cluster_a.bounds[2])
    size_b = max(cluster_b.bounds[1] - cluster_b.bounds[0], cluster_b.bounds[3] - cluster_b.bounds[2])
    return distance > 2 * (size_a + size_b)

def compute_multipole(cluster):
    if not cluster.children:
        for p in cluster.particles:
            #r = p.position - cluster.center
            cluster.multipole_moment += p.charge  
    else:
        for child in cluster.children:
            compute_multipole(child)
            cluster.multipole_moment += child.multipole_moment
            
def multipole_to_local(cluster, clusters):
    for target in clusters:
        if well_separated(cluster, target):
            r = target.center - cluster.center
            target.local_expansion += cluster.multipole_moment / np.linalg.norm(r)
        else:
            if cluster.children:
                for child in cluster.children:
                    multipole_to_local(child, [target] if not target.children else target.children)
                    
def local_to_local(cluster):
    if cluster.children:
        for child in cluster.children:
            child.local_expansion += cluster.local_expansion
            local_to_local(child)
    
def evaluate_potential(cluster):
    if not cluster.children:
        for p in cluster.particles:
            #r = p.position - cluster.center
            p.potential += cluster.local_expansion
    else:
        for child in cluster.children:
            evaluate_potential(child)

def collect_clusters(cluster, clusters):
    clusters.append(cluster)
    for child in cluster.children:
        collect_clusters(child, clusters)
        
def compute_MLFMA(particles, max_particles, bounds):
    root_cluster = build_tree(particles, max_particles, level=0, bounds=bounds)

    compute_multipole(root_cluster)


    clusters = []
    collect_clusters(root_cluster, clusters)

    for cluster in clusters:
        if cluster.children:
            multipole_to_local(cluster, clusters)

    local_to_local(root_cluster)

    evaluate_potential(root_cluster)    
