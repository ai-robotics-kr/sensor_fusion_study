
# ScanContext - Python Example 

---

## Folder Structure

```
.
├── data
│   └── 000095.bin
├── Distance_SC.py
├── make_sc_example.py
├── README.md
├── requirements.txt
└── result
    ├── ptcloud_filtered.png
    └── sc_multires.png
```

### First, It contains two python example codes

1. `make_sc_example` : Shows how ScanContext is build (Sometimes it's referred as **SC**)
2. `Distance_SC` : Calculate difference btw two **SCs** 

And it provides sample pointCloud data. which located in `data` folder.
During codes, There's an option to show rough shape of it. Here's an image for that.

<p align="center">
    <img src="./result/ptcloud_filtered.png" width="500">
</p>

`result` folder also contains **SC** images with various resolutions.

<p align="center">
    <img src="./result/sc_multires.png" width="300">
</p>


# How to use

1. Prepare python virtual environment

We recommend to use `Anaconda`, since we tested all those things on that. You can create your environments only for this example like this.


* Anaconda Setup
  
```bash
$ conda activate <your-conda-env>
$ cd Examples/ScanContext
$ pip install -r requirements.txt

# Finally Run Codes
$ python3 make_sc_example.py
# or 
$ python3 Distance_SC.py
```