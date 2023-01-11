def get_idx_laser_fov_for_each_well(index, laser, file_path, fov=None):
    """
        Get index, laser and optional FOV for each well (used to name PDF save)
    """
    for l in laser:
        for i in index:
            if fov !=None:
                for f in fov:
                    if (i in file_path) and (l in file_path) and (f in file_path):
                        return[i, l, f]
            elif (i in file_path) and (l in file_path):
                return[i, l]