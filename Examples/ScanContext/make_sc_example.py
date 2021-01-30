import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from open3d import *


class kitti_vlp_database:
    def __init__(self, bin_dir):
        self.bin_dir = bin_dir
        self.bin_files = os.listdir(bin_dir)
        self.bin_files.sort()

        self.num_bins = len(self.bin_files)


class ScanContext:

    # static variables
    multiple_resolution = 1

    downcell_size = 0.5

    kitti_lidar_height = 2.0

    max_length = 80

    def __init__(self, bin_dir, bin_file_name, viz=0, multiple_resolution=0):

        self.viz = viz
        self.set_resolution(multiple_resolution)

        self.bin_dir = bin_dir
        self.bin_file_name = bin_file_name
        self.bin_path = bin_dir + bin_file_name

        self.scancontexts = self.genSCs()

    def set_resolution(self, multiple_resolution):
        if multiple_resolution:
            self.sector_res = np.array([45, 90, 180, 360, 720])
            self.ring_res = np.array([10, 20, 40, 80, 160])
        else:
            self.sector_res = np.array([60])
            self.ring_res = np.array([20])

        ScanContext.multiple_resolution = multiple_resolution

    def load_velo_scan(self):
        scan = np.fromfile(self.bin_path, dtype=np.float32)
        scan = scan.reshape((-1, 4))
        ptcloud_xyz = scan[:, :-1]

        return ptcloud_xyz

    def xy2theta(self, x, y):
        if x >= 0 and y >= 0:
            theta = 180 / np.pi * np.arctan(y / x)
        if x < 0 and y >= 0:
            theta = 180 - ((180 / np.pi) * np.arctan(y / (-x)))
        if x < 0 and y < 0:
            theta = 180 + ((180 / np.pi) * np.arctan(y / x))
        if x >= 0 and y < 0:
            theta = 360 - ((180 / np.pi) * np.arctan((-y) / x))

        return theta

    # returns location of input point in SC Coordinates
    def pt2rs(self, point, gap_ring, gap_sector, num_ring, num_sector):
        x = point[0]
        y = point[1]
        z = point[2]

        if x == 0.0:
            x = 0.001
        if y == 0.0:
            y = 0.001

        theta = self.xy2theta(x, y)
        faraway = np.sqrt(x * x + y * y)

        """ np.divmod, referenced from https://numpy.org/doc/stable/reference/generated/numpy.divmod.html
        >>> np.divmod(np.arange(5), 3)
        (array([0, 0, 0, 1, 1]), array([0, 1, 2, 0, 1]))
        """

        idx_ring = np.divmod(faraway, gap_ring)[0]
        idx_sector = np.divmod(theta, gap_sector)[0]

        if idx_ring >= num_ring:
            idx_ring = num_ring - 1  # python starts with 0 and ends with N-1

        return int(idx_ring), int(idx_sector)

    # Main Function
    def ptcloud2sc(self, ptcloud, num_sector, num_ring, max_length):

        num_points = ptcloud.shape[0]

        gap_ring = max_length / num_ring
        gap_sector = 360 / num_sector

        enough_large = 1000
        sc_storage = np.zeros([enough_large, num_ring, num_sector])
        sc_counter = np.zeros([num_ring, num_sector])

        for pt_idx in range(num_points):

            point = ptcloud[pt_idx, :]
            point_height = point[2] + ScanContext.kitti_lidar_height

            idx_ring, idx_sector = self.pt2rs(
                point, gap_ring, gap_sector, num_ring, num_sector
            )

            if sc_counter[idx_ring, idx_sector] >= enough_large:
                continue
            sc_storage[
                int(sc_counter[idx_ring, idx_sector]), idx_ring, idx_sector
            ] = point_height
            sc_counter[idx_ring, idx_sector] = sc_counter[idx_ring, idx_sector] + 1

        sc = np.amax(sc_storage, axis=0)

        return sc

    def genSCs(self):
        ptcloud_xyz = self.load_velo_scan()
        print("The number of original points: " + str(ptcloud_xyz.shape))
        pcd = open3d.geometry.PointCloud()
        pcd.points = open3d.utility.Vector3dVector(ptcloud_xyz)

        # Half-Scale DownSampling
        downpcd = pcd.voxel_down_sample(voxel_size=ScanContext.downcell_size)
        ptcloud_xyz_downed = np.asarray(downpcd.points)
        print("The number of downsampled points: " + str(ptcloud_xyz_downed.shape))

        if self.viz:
            open3d.visualization.draw_geometries([downpcd])

        self.SCs = []
        for res in range(len(self.sector_res)):
            num_sector = self.sector_res[res]
            num_ring = self.ring_res[res]

            sc = self.ptcloud2sc(
                ptcloud_xyz_downed, num_sector, num_ring, ScanContext.max_length
            )
            self.SCs.append(sc)

    def plot_multiple_sc(self, fig_idx=1):

        num_res = len(self.sector_res)

        if ScanContext.multiple_resolution:
            fig, axes = plt.subplots(nrows=num_res, figsize=(8, 16))

            axes[0].set_title("Scan Contexts with multiple resolutions", fontsize=20)
            for ax, res in zip(axes, range(num_res)):
                ax.imshow(self.SCs[res])
        else:
            fig, axes = plt.subplots(figsize=(16, 8))
            axes.imshow(self.SCs[0])

        plt.show()


if __name__ == "__main__":

    bin_dir = "./data/"
    bin_db = kitti_vlp_database(bin_dir)

    for bin_idx in range(bin_db.num_bins):

        bin_file_name = bin_db.bin_files[bin_idx]
        bin_path = bin_db.bin_dir + bin_file_name

        sc = ScanContext(bin_dir, bin_file_name, multiple_resolution=1)

        fig_idx = 1
        sc.plot_multiple_sc(fig_idx)

        print(len(sc.SCs))
        print(sc.SCs[0].shape)
