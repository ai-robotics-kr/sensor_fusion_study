import os
import sys
import csv
import copy
import time
import random
import argparse

import numpy as np
np.set_printoptions(precision=4)
from matplotlib.animation import FFMpegWriter

from tqdm import tqdm

from minisam import *
from utils.ScanContextManager import *
from utils.PoseGraphManager import *
from utils.UtilsMisc import *
import utils.UtilsPointcloud as Ptutils
import utils.ICP as ICP

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

# params
parser = argparse.ArgumentParser(description='PyICP SLAM arguments')

parser.add_argument('--num_icp_points', type=int, default=5000) # 5000 is enough for real time

parser.add_argument('--num_rings', type=int, default=20) # same as the original paper
parser.add_argument('--num_sectors', type=int, default=60) # same as the original paper
parser.add_argument('--num_candidates', type=int, default=10) # must be int
parser.add_argument('--try_gap_loop_detection', type=int, default=10) # same as the original paper

parser.add_argument('--loop_threshold', type=float, default=0.11) # 0.11 is usually safe (for avoiding false loop closure)

parser.add_argument('--data_base_dir', type=str, 
                    default='/media/swimming/Seagate SDD/Data/KITTI/dataset/sequences')
parser.add_argument('--sequence_idx', type=str, default='01')

parser.add_argument('--save_gap', type=int, default=300)

args = parser.parse_args()

from easydict import EasyDict as edict

ed_args = edict(
    {
        "num_icp_points": 5000,
        "num_rings": 20,
        "num_sectors": 60,
        "num_candidates": 10,
        "try_gap_loop_detection": 10,
        "loop_threshold": 0.11,
    }
)

ed_args.data_base_dir = "/media/swimming/Seagate SDD/Data/KITTI/dataset/sequences"
ed_args.sequence_idx = "00"
ed_args.save_gap = 300


# dataset 
sequence_dir = os.path.join(ed_args.data_base_dir, ed_args.sequence_idx, 'velodyne')
sequence_manager = Ptutils.KittiScanDirManager(sequence_dir)
scan_paths = sequence_manager.scan_fullpaths
num_frames = len(scan_paths)

# Pose Graph Manager (for back-end optimization) initialization
PGM = PoseGraphManager()
PGM.addPriorFactor()

# Result saver
save_dir = "result/" + ed_args.sequence_idx
if not os.path.exists(save_dir): os.makedirs(save_dir)
ResultSaver = PoseGraphResultSaver(init_pose=PGM.curr_se3, 
                             save_gap=ed_args.save_gap,
                             num_frames=num_frames,
                             seq_idx=ed_args.sequence_idx,
                             save_dir=save_dir)

# Scan Context Manager (for loop detection) initialization
SCM = ScanContextManager(shape=[ed_args.num_rings, ed_args.num_sectors], 
                                        num_candidates=ed_args.num_candidates, 
                                        threshold=ed_args.loop_threshold)

# for save the results as a video
fig_idx = 1
fig = plt.figure(fig_idx)
writer = FFMpegWriter(fps=15)
video_name = ed_args.sequence_idx + "_" + str(ed_args.num_icp_points) + ".mp4"
num_frames_to_skip_to_show = 5
num_frames_to_save = np.floor(num_frames/num_frames_to_skip_to_show)

def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'basic2.png'

    with PyCallGraph(output=graphviz):
    # with writer.saving(fig, video_name, num_frames_to_save): # this video saving part is optional
        # @@@ MAIN @@@: data stream
        for for_idx, scan_path in tqdm(enumerate(scan_paths), total=num_frames, mininterval=5.0):

            # get current information     
            curr_scan_pts = Ptutils.readScan(scan_path) 
            curr_scan_down_pts = Ptutils.random_sampling(curr_scan_pts, num_points=ed_args.num_icp_points)

            # save current node
            PGM.curr_node_idx = for_idx # make start with 0
            SCM.addNode(node_idx=PGM.curr_node_idx, ptcloud=curr_scan_down_pts)
            if(PGM.curr_node_idx == 0):
                PGM.prev_node_idx = PGM.curr_node_idx
                prev_scan_pts = copy.deepcopy(curr_scan_pts)
                icp_initial = np.eye(4)
                continue

            # calc odometry
            prev_scan_down_pts = Ptutils.random_sampling(prev_scan_pts, num_points=ed_args.num_icp_points)
            odom_transform, _, _ = ICP.icp(curr_scan_down_pts, prev_scan_down_pts, init_pose=icp_initial, max_iterations=20)

            # update the current (moved) pose 
            PGM.curr_se3 = np.matmul(PGM.curr_se3, odom_transform)
            icp_initial = odom_transform # assumption: constant velocity model (for better next ICP converges)

            # add the odometry factor to the graph 
            PGM.addOdometryFactor(odom_transform)

            # renewal the prev information 
            PGM.prev_node_idx = PGM.curr_node_idx
            prev_scan_pts = copy.deepcopy(curr_scan_pts)

            # loop detection and optimize the graph 
            if(PGM.curr_node_idx > 1 and PGM.curr_node_idx % ed_args.try_gap_loop_detection == 0): 
                # 1/ loop detection 
                loop_idx, loop_dist, yaw_diff_deg = SCM.detectLoop()
                if(loop_idx == None): # NOT FOUND
                    pass
                else:
                    print("Loop event detected: ", PGM.curr_node_idx, loop_idx, loop_dist)
                    # 2-1/ add the loop factor 
                    loop_scan_down_pts = SCM.getPtcloud(loop_idx)
                    loop_transform, _, _ = ICP.icp(curr_scan_down_pts, loop_scan_down_pts, init_pose=yawdeg2se3(yaw_diff_deg), max_iterations=20)
                    PGM.addLoopFactor(loop_transform, loop_idx)

                    # 2-2/ graph optimization 
                    PGM.optimizePoseGraph()

                    # 2-2/ save optimized poses
                    ResultSaver.saveOptimizedPoseGraphResult(PGM.curr_node_idx, PGM.graph_optimized)

            # save the ICP odometry pose result (no loop closure)
            ResultSaver.saveUnoptimizedPoseGraphResult(PGM.curr_se3, PGM.curr_node_idx) 
            # if(for_idx % num_frames_to_skip_to_show == 0): 
            #     ResultSaver.vizCurrentTrajectory(fig_idx=fig_idx)
            #     writer.grab_frame()

if __name__ == '__main__':
    main()