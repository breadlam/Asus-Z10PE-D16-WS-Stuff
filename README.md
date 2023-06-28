# Modifying an Asus Z10PE-D16 WS BIOS image
Here are a couple scripts for extracting and re-encapsulating BIOS images for a Asus Z10PE D16 WS motherboard.  

I created this repo as a backup for my posts to an [overclock.net forum](https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/page-28)

## PCIe Bifurcation
### Premise
I wanted my Z10PE-D16 WS motherboard to support an Asus Hyper M.2 x16 V2 card. I had multiple NVMe drives and needed to free up more PCIe slots for other devices.  

By default, Z10PE-D16 WS BIOS images from Asus don't support PCIe bifurcation, for modes beyond a single x16, x8, or x4 lane per card slot.
The Z10PE-D16 WS also doesn't have onboard M.2 slots for NVMe drives, so it's common to use M.2 PCIe cards instead.  

Using an M.2 PCIe card with more than one M.2 slot requires PCIe bifurcation. Typically, each M.2 slot uses one x4 PCIe lane. This means that an x16 PCIe slot could support up to four M.2 devices, if the x16 slot were bifurcated into x4/x4/x4/x4 lanes.  

### Solution

The latest BIOS image from Asus (August 2019) can be modified to support PCIe bifurcation.

The last Asus-supported BIOS image for Z10PE-D16 WS motherboards can be found here (version 4101):  
https://dlcdnets.asus.com/pub/ASUS/mb/Socket2011-R3/Z10PE-D16_WS/BIOS/Z10PE-D16-WS-ASUS-4101.zip?model=z10pe-d16%20ws

The 4101 BIOS image is embedded inside a capsule file (.CAP), which is just a 2048 byte header prepended to a BIOS image.  
I originally outlined the structure of the capsule file here:  
https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/post-28761722
```
Picture that this is the whole CAP file:
[ ...... whole CAP file from ASUS ...... ]

And it can be split into these two parts:
[ CAP header ][ original BIOS image data ]

Which is laid out like this, as far as byte offsets:
[0 ..... 2047][2048 ......... end-of-file]
```

I wrote some simple scripts in Python to extract a BIOS image from a CAP file (`decapify.py`) and reconstruct a CAP file from a BIOS image (`capify.py`).  
The tools takes advantage of the fact that the Z10PE-D16 WS firmware **doesn't verify the CAP file header signature against the attached BIOS image**.  
As a result, the original CAP header can be used with a modified BIOS image.  

The `capify.py` tool contains the original CAP file header bytes for BIOS version 4101, which it prepends to any given BIOS file. The resulting capsule file passes the motherboard's file check, allowing a custom BIOS to be written to the board using USB Flashback (or from boot config menu).  

The extracted BIOS file can be edited manually, or by using some kind of standard tool such as AMIBCP.  

Here's a link to my original post about these scripts in the overclock.net forums:  
https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/post-28762030

#### Instructions:
* Download BIOS image 4101 from ASUS.
* Use `decapify.py` to extract the BIOS image for AMIBCP
    * Example: `python3 decapify.py Z10PE-D16-WS-ASUS-4101.CAP bios.bin`
* Use AMIBCP (or whatever) to edit `bios.bin` to add in support for bifurcation. Save to a filename such as `mod-bios.bin`.
    * [Here's my description of how the PCIe slots are mapped.](https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/post-28516664)
    * ```
      Slot #1: IIO 1 / IOU2
      Slot #2: IIO 0 / IOU0
      Slot #3: IIO 0 / IOU2
      Slot #4: IIO 0 / IOU1
      Slot #5: IIO 1 / IOU0
      Slot #6: IIO 1 / IOU1
      ```
* Use `capify.py` to construct a new CAP file. It uses the CAP header from the original 4101 CAP file, making it possible to use USB Flashback.
    * Example: `python3 capify.py mod-bios.bin Z1016WS.CAP`
* Flash Z1016WS.CAP to your board.

### Additional Info
* Instructions for enabling/disabling bifurcation support **via BIOS boot menu**, using AMIBCP: https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/post-29202198
    * I haven't incorporated this into my own BIOS image yet, but it's a huge improvement over what I did (which was just to put slot 5 into x4/x4/x4/x4 mode permanently)
