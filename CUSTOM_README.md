## PyICP-SLAM Execution

### Reference

* [gisbi-kim/PyICP-SLAM](https://github.com/gisbi-kim/PyICP-SLAM/tree/master)
* [Scan Context: Egocentric Spatial Descriptor
for Place Recognition within 3D Point Cloud Map](https://irap.kaist.ac.kr/publications/gkim-2018-iros.pdf)
* [Youtube tutorial from SLAM KR - Korean](https://www.youtube.com/watch?v=xuMZVC53SGU)

### 1. sophus install

* **sophus** is a c++ implementation of Lie groups

```bash
$ git clone https://github.com/strasdat/Sophus.git
$ cd Sophus
$ mkdir build && cd build
$ cmake ..

# For Faster build, 8 cores will used.
$ make -j8
$ sudo make install

$ sudo apt-get install apt-file
$ sudo apt-get update
$ apt-file search horst.so
```

### 2. minisam install for python

* **miniSAM** is an open-source `C++/Python` framework for solving factor graph based least squares problems.

```bash
$ git clone --recurse-submodules https://github.com/dongjing3309/minisam.git
$ cd minisam
$ mkdir build
$ cd build

# enter your virtual env path
$ cmake .. -DPYTHON_EXECUTABLE=<your_python_env_path> -DMINISAM_BUILD_PYTHON_PACKAGE=ON -DMINISAM_BUILD_SHARED_LIB=ON

# for example
$ cmake .. -DPYTHON_EXECUTABLE=/home/swimming/anaconda3/envs/ai_robo_kr_env/bin/python -DMINISAM_BUILD_PYTHON_PACKAGE=ON -DMINISAM_BUILD_SHARED_LIB=ON

$ make python_package -j8
$ sudo make install -j8

# install check
$ pip list | grep minisam
>> minsam 0.0.0
```

### ROS users can encounter such an errors 

![](https://user-images.githubusercontent.com/12381733/106414198-6440c780-648f-11eb-8a23-77cdbe335cd5.png)

![](https://user-images.githubusercontent.com/12381733/106414199-64d95e00-648f-11eb-90c1-ff7e0a4a0712.png)

### This is a problem caused by `ros-sophus` is looking at past versions. - original issue from [stonier/sophus](https://github.com/stonier/sophus)

![](https://user-images.githubusercontent.com/12381733/106414200-6571f480-648f-11eb-8e40-53212641ed77.png)


* referenced from : [https://github.com/stonier/sophus]()

- It is standard to modify `cmake` to look at the newly built sophus, but the ROS package was removed because it did not know how to do it.

```bash
$ sudo apt-get purge ros-melodic-sophus
# Let's install it again later. :)
```


---

## Build Again!!

- Or it can be built without sophus, which can lead to the following error.

![](https://user-images.githubusercontent.com/12381733/106414201-660a8b00-648f-11eb-8f2e-5322df6dd6fb.png)


`setup_no_sophus.py.in` Syntax errors can occur in this file.

- Additional installation required Packages

```bash
# libcholmod 에러 발생 시
$ sudo apt-get install libsuitesparse-dev
```

### Specify file location

```cpp
parser.add_argument('--data_base_dir', type=str, 
                    default='../KITTI_Dataset/2011_09_26/2011_09_26_drive_0027_sync/velodyne_points/data')
parser.add_argument('--sequence_idx', type=str, default='')

parser.add_argument('--save_gap', type=int, default=300)

args = parser.parse_args()

# dataset 
sequence_dir = os.path.join(args.data_base_dir, args.sequence_idx, '')
sequence_manager = Ptutils.KittiScanDirManager(sequence_dir)
scan_paths = sequence_manager.scan_fullpaths
num_frames = len(scan_paths)
```

### Additional Package install

* The following packages must be installed in your **Python environment**:

```bash
$ pip install numpy tqdm scipy matplotlib sklearn easydict
```

* Let's install `ffmpeg` when the following error occurs during `sklearn` installation.

```bash
File "/home/kimsooyoung/anaconda3/envs/ai_robo_kr/lib/python3.8/subprocess.py", line 854, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/home/kimsooyoung/anaconda3/envs/ai_robo_kr/lib/python3.8/subprocess.py", line 1702, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

```bash
$ sudo apt-get install ffmpeg
```

## Run!!!


```bash
$ python3 main_icp_slam.py
```

- When executed, the `matplotlib` screen appears with the status bar as follows:

<p align="center">
    <img src="https://user-images.githubusercontent.com/12381733/106414204-660a8b00-648f-11eb-9d98-e976c0836577.png" width="450">
</p>

When all tasks are completed, `mp4` files and `result` folders are created, and the `result` folder has a `pose graph image`.

* `PyICP` and `ScanContext` are included as **Submodules** and can be cloned to a local PC as follows:

```bash
$ git submodule update --init --recursive

# make it to follows brand new commit
$ git submodule update --remote --merge
```