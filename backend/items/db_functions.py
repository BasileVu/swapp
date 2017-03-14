def distance_points(distance):
    if distance < 1:
        return 50
    if distance < 5:
        return 30
    if distance < 10:
        return 20
    if distance < 20:
        return 15
    if distance < 30:
        return 10
    if distance < 40:
        return 5
    if distance < 50:
        return 3
    return 0
