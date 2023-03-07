def get_idx_laser_fov_for_each_well(index, laser, file_path):
    """
        Get index, laser and optional FOV for each well (used to name PDF save)
    """
    for l in laser:
        for i in index:
            if (l in file_path) and (i in file_path):
                return[i, l]