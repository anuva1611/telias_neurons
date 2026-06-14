# Neuron Morphology Analysis: Standard Operating Procedure
Prepared by: Anuva Nabiha
Date: 6/12/2026

# Purpose
This SOP describes detailed steps for processing and analysing longitudinal in vivo fluorescence images of 2 individual neurons at 2 times using Fiji/ImageJ software. It covers preprocessing, stitching, neurite tracing, temporal comparison, and false positive/false negative assessment. (Optionally 3D reconstruction)

# Final output 
Please use this google drive link to find the original output folder:
Screenshots of steps is added in the repository under `imagej_output_screenshots' for quick navigation. 

# Assignment Methodology

Detailed steps of each phase is written in here, with output files in the `outputs` folder. An example walkthrough of steps with screenshots will be added in the output folders' markdown file. 

## Raw data set 
Dataset     |  # Tiles   |  Tile size  | dtype 
CELL1_TIME1 |     15     |  480×624 px | uint8
CELL1_TIME2 |     16     |  480×624 px | uint8
CELL2_TIME1 |     23     |  480×624 px | uint8
CELL2_TIME2 | 36 + 2 AVI |  480×624 px | uint8


## Step 1: Image Prepocessing & Optimization 
The goal of this step is to remove any uneven background, boost contrast, reduce nouse, and isolate the target cells from any neighboring cells.

1. Confirm Imagetype: Open each tile at a time to confirm they are grayscale images 624x480 px and 8-bit type; If this is not default image type can be found: `image` ->  `Type` 
2. Background Subtraction: This will remove uneven glow that is visible. Follow these steps:
    * `Process` -> `Subtarct Background`
    * Set `Rolling Ball Radius` = 50.0 pixels
    * Uncheck `Light background` 
    * Check `Sliding paraboloid`
    * Click `OK`

    _Notes/rationale: We are using 50px as the tiles are 480×624px and neurites are thin (~3-5 px wide). Therefore a radius of 50px can capture the background without affecting the actual signal. Light background is uncheked as the images are grayscale fluorescence. Finally, sliding paraboloid will give more accurate correction on curved background._
3. Contrast Enhancement (CLAHE): Instead of uisng the standard 'Enhance Contrast`, CLAHE adjusts to local regions which is better for neurons with soma and distal neurites. 
    * `Process` -> `Enhance Local Contrast (CLAHE)`
    * Set `Blocksize` = 63
    * Set `Histogram bins` = 256
    * Set `Maximum slope` = 1.5
    * Leave Mask as `*None*`, leave `Fast` checked
    * Click `OK`

    _Notes/rationale: A blocksize of 63 px is set as 63px is the size CLAHE uses to compute its local histogram. our tiles are 624×480px and individual neurites are ~3–5 px wide. A blocksize of 63px is ~10% of the tile width, large enough to capture meaningful local contrast around a dendritic branch while small enough to adapt between the bright soma and distal tips. Histogram bins of 256 is left (default) as it matches the full uint8 range of images, fewer bins would lose intensity resolution. Maximum slope is the contrast amplification limit per tile block. As the images are already dim, a slope of 1.5 enhances signal without over-amplifying background noise._
4. Denoise:
    * `Process` -> `Filters` -> `Gaussian Blur...`
        - `Sigma` = 1.0
        - Click OK

        _Notes/rationale: Gaussian blur reduces continuous shot noise. Sigma controls the blur radius. At 1.0 px, the blur kernel is narrow enough that it only averages over ~3 px, which smooths out single-pixel shot noise without visibly blurring neurite edges._
    * `Process` -> `Filters` -> `Median...`
        - `Radius` = 1
        - Click OK

        _Notes/rationale: Median filter replaces each pixel with the median of its neighbors in a 3×3 window (radius 1 = 1 px out from centre). This specifically targets isolated hot pixels and salt-and-pepper noise that Gaussian blur softens but does not fully remove. Radius 1 is the minimum effective setting as a radius of 2 was stating to erode the dentritic tips._
5. Separate Neighboring Cells: 
    * Duplicate the image first: `Image` -> `Duplicate` -> name it **separate_neighbor** -> OK
    * On this duplicate image, run: `Image` -> `Adjust` -> `Threshold...` In the threshold GUI:
        - Method dropdown: select `Otsu` (instead of `Default`)
        - Select `B&W` in the color dropdown
        - Check `Dark background`
        - Uncheck `Dont Reset Range`
        - Click Apply. The image should become black and white

    _Notes/rationale: Otsu's method automatically finds the threshold by minimizing the variance within the two classes_
    * `Process` -> `Binary` -> `Watershed` — this separates touching blobs
    _Notes: This is optional depending on the image we are processing_
6. Analyze: `Analyze` -> `Analyze Particles...`
    * `Size`: 500-Infinity (in pixels²) 
    * `Circularity`: 0.00 - 1.00 
    * Show: `Bare Outlines`?
    * Check `Add to Manager`
    * Check `Include holes`
    * Click OK

    _Notes/rationale: 500-Infinity pixels² sets the minimum area a connected region must have to be counted as a real object. 500 px² corresponds to a circle of roughly 25 px diameter, which is larger than any noise speck or single hot pixel but smaller than the soma. Setting circularity ranges from 0 (infinitely elongated) to 1 (perfect circle) means we accept all shapes: the soma is roughly circular (~0.7–1.0) but dendritic branches are very elongated (~0.0–0.2)._
7. ROI Manager: The ROI Manager opens with numbered regions. Looking at the original image, we can now identify which ROI is the target cell. The largest continuous region is our cell. 
    * In the ROI Manager: click on any ROI that is a neighbor cell
    * On the original image (not the duplicate): go to `Edit` -> `Clear`; this fills that region with black (zero)
    * Close the **separate_neighbor** duplicate 
8. Save the original file under `outputs` > `step1_processed`





# References
* https://sbalzarini-lab.org/?q=downloads/imageJ 
* https://imagej.net/plugins/clahe 
* https://imagej.net/ij/docs/guide/146-29.html
* https://imagej.net/ij/docs/menus/process.html
* https://imagej.net/imaging/particle-analysis
* https://imagej.net/scripting/batch 

