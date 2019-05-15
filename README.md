# Flop 3D Layers

***WORK IN PROGRESS***

PrusaSlicer has some really nice supports and slicing for printing with the Prusa SL1 UV resin printer, but for printing on a Wanhao D7, these images are backwards, and result in “inside out” 3D prints. This script will flop all of the images and re-zip for easy upload to [NanoDLP](https://www.nanodlp.com/) and printing.

## Usage

```bash
$ flop_3d_layers.py /path/to/example.<sl1|zip> [-f|--force]
```

The script checks for an `.sl1` extension, which is the zipped format that the PrusaSlicer exports. a `.zip` extension is also acceptable. If, for some odd reason, your file ends in a different extension, just add `-f` or `--force` to the end to force processing.

***[WIP]***