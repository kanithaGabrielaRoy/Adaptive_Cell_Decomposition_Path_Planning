def smooth_path(path):
    if len(path) < 3:
        return path

    smooth = [path[0]]
    for i in range(1, len(path)-1):
        smooth.append(path[i])
    smooth.append(path[-1])
    return smooth

