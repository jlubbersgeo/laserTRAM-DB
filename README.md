**THIS REPOSITORY IS NOW ARCHIVED. CURRENT DEVELOPMENT ON LASERTRAM-DB 2.X.X IS NOW BEING DONE AT https://code.usgs.gov/vsc/petro/tools/lasertramdb**
**PLEASE GO THERE FOR UP TO DATE CODE AND DATA PROCESSING AS THIS IS NO LONGER SUPPORTED**

# `LaserTRAM-DB`: A dashboard for the complete laser ablation icp-ms data reduction pipeline.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8329594.svg)](https://doi.org/10.5281/zenodo.8329594)

**_Note_** `LaserTRAM-DB` is (seemingly) always in development and new features are being added (we are happy to take suggestions!). While this is the case, the underlying math and data produced by the software are still accurate. Functionalities being added are those that fall into the following areas:

- signal despiking
- region omission within selected area

_Happy processing!_ <br> -`Jordan`

## Summary

LaserTRAM-DB is a dashboard for the complete processing pipeline of Laser Ablation Inductively Coupled Plasma Mass Spectrometry (LA-ICP-MS) data in complex materials such as geologic samples. As LA-ICP-MS data in geologic samples frequently have multiple phases, inclusions, and other compositional complexities within them that do not represent the material of interest, user interaction is required to filter unwanted signals out of the overall ablation signal. LaserTRAM-DB allows the user to filter which portion of the ablation peak is utilized in calculating concentrations, subsequently allowing for more accurate data to be obtained. It allows easy inspection of any sort of calculation done to the data and just about everything is exportable from tables displayed within the dashboard.

It is comprised of 3 parts:

1. **LaserTRAM:** Choosing an interval of interest from raw cps data in individual spot analyses and normalizing it to an internal standard.

![LaserTRAM GUI](images/LaserTRAM_tab.png)

2. **LaserTRAM profiler** Choosing numerous intervals of interest from raw cps data in a series of rapidly gathered line of spots and normalizing them to an internal standard.

![LaserTRAM-profiler GUI](images/LaserTRAM-profiler_tab.png)

3. **LaserCalc:** Takes the output from either LaserTRAM or LaserTRAM profiler and converts the normalized data into concentrations using the equations outlined below.

![LaserCalc GUI](images/LaserCalc_concentrations_tab.png)

## Installation and Use

LaserTRAM-DB can be installed locally and run by creating a virtual environment using the provided `yml` file. If you are new to python, we recommend doing this through [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

```
git clone https://github.com/jlubbersgeo/laserTRAM-DB
cd /path/to/laserTRAM-DB
conda env create -f environment.yml
conda activate lasertram-db
python lasertram-db.py
```

Alternatively, you may run the `lasertram-db.py` script through any Python IDE: VSCode, JupyterLab, etc. After running the script, the dashboard will open in the browser. Because it is browser hosted, all data uploaded into the dashboard are stored there. _This means hitting the refresh button will completely clear and delete all data...you've been warned_.

### Caveats

If you are on a computer where you do not have admin permissions, `git` may not be installed when you create a new virtual environment. A workaround for this is simply downloading the repository as a zip file and unpacking. This will accomplish the same task as:

```
git clone https://github.com/jlubbersgeo/laserTRAM-DB
```

## Data input format

Initially, LaserTRAM and LaserTRAM-profiler require a single spreadsheet upload that looks like:
| timestamp | SampleLabel | Time | analyte 1 | ... | analyte n |
|:-------------------:|:-----------:|:-----:|:---------:|:---:|:---------:|
| 2022-10-10 22:44:00 | GSE-1G_1 | 13.24 | 100000 | ... | 100 |

All standard reference materials should be appropriately named. More specifically, their GEOREM name should be somewhere in the actual string:

For example if our standard is GSE-1G:

- okay: GSE-1G-10, GSE-1G-iheartlasers
- not okay: GSE1G, literally anything that doesn't have GSE-1G in it

If they are not appropriately named they will be treated as unknowns and not available as calibration standards.

If you are using either a Thermo iCAP series or Agilent 8900 QQQ quadrupole mass spectrometer there is a small app called `multifiler` that can do this for you [here](https://drive.google.com/drive/folders/1vECM690szcXf54rm-DI3Hz1OH5BAJYjq?usp=sharing) or you can get it at the GitHub repo [here](https://github.com/jlubbersgeo/multifiler).

## Calculations

All calculations are done under the hood using the package [`lasertram`](https://jlubbersgeo.github.io/lasertram/). In many ways you can think about `LaserTRAM-DB` as a wrapper to `lasertram` that is designed to offer better interactivity with no scripting.


The math, logic, and structure of `lasertram` is now published in _Applied Computing and Geosciences_: [`lasertram`: A Python library for time resolved analysis of laser ablation inductively coupled plasma mass spectrometry data](https://doi.org/10.1016/j.acags.2025.100225)

Here's a bib entry for you:

```tex
@article{lubbers2025lasertram,
  title={lasertram: A Python library for time resolved analysis of laser ablation inductively coupled plasma mass spectrometry data},
  author={Lubbers, Jordan and Kent, Adam JR and Russo, Chris},
  journal={Applied Computing and Geosciences},
  pages={100225},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.acags.2025.100225}
}
```


## Quickstart

With LaserTRAM-DB up and running, to get started, sample data may be found in the "tests" folder:

- LaserTRAM test data: `spot_test_timestamp_raw_data.xlsx`
- LaserCalc test data: `spot_test_timestamp_lasertram_complete.xlsx`,`profile_test_lasertram_profiler_complete.xlsx`
- LaserCalc standards data: `laicpms_stds_tidy.xlsx`

## Tutorials
### Video

A three-part video series on the basics of LaserTRAM-DB can be found [here](https://www.youtube.com/playlist?list=PLxZuo_RAAq_c4pd23NQzQ03hZgHjJ6AAN)

### Documentation

_Coming Soon_

A series of YouTube tutorials on how to use the dashboard can be found here: [https://youtu.be/dOm4dW4qy0s?si=1efj4G1tqqH8SJDG](https://youtu.be/dOm4dW4qy0s?si=1efj4G1tqqH8SJDG)

## Contributing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

One of the main goals of this project is to bring increased transparency to the fields that utilize LA-ICP-MS data. As such, we welcome feedback and suggestions to help improve the software! If you wish to be a part of further development, or have ideas for new features please open an [issue](https://github.com/jlubbersgeo/laserTRAM-DB/issues) here on GitHub or reach out to Jordan Lubbers (jlubbers _at_ usgs.gov).
