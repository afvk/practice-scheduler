def update_easiness(q, EF):
    """
    Adapted from https://en.wikipedia.org/wiki/SuperMemo. Removed n and I because only the easiness factor is used. 
    """

    EF += 0.1 - (5 - q) * 0.08 + (5 - q) * 0.02
    EF = max(EF, 1.3)
    return EF
