# Asus Z10PE-D16 WS
BIOS modification scripts and such for Asus Z10PE D16 WS motherboards, created as a backup for files I posted to the overclock.net forums.

## PCIe Bifurcation
### Premise
By default, BIOS files from Asus don't support PCIe modes beyond x16, x8, or x4 for a given card slot.  
The Z10PE-D16 WS doesn't have onboard m2 slots for NVMe drives, so it's common to use m2 PCIe cards instead.  
However, using an m2 PCIe card with more than one m2 slot requires PCIe bifurcation. Typically, each m2 slot uses one x4 PCIe lane. This means that one x16 PCIe slot could support up to four x4 lanes, if the slot were bifurcated into x4/x4/x4/x4 lanes.  

### Solution
The last Asus-supported BIOS image for Z10PE-D16 WS motherboards can be found here (version 4101):  
https://dlcdnets.asus.com/pub/ASUS/mb/Socket2011-R3/Z10PE-D16_WS/BIOS/Z10PE-D16-WS-ASUS-4101.zip?model=z10pe-d16%20ws

The 4101 BIOS image is embedded inside a capsule file (.CAP), which is primarily just a 2048 byte signature header in addition to the raw BIOS image.  
I've outlined the structure of the capsule file here:  
https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/post-28761722
```
Picture that this is the whole CAP file:
[ ...... whole CAP file from ASUS ...... ]

And it can be split into these two parts:
[ CAP header ][ original BIOS image data ]

Which is laid out like this, as far as byte offsets:
[0 ..... 2047][2048 ......... end-of-file]

The CAP header exists from offset 0 to offset 2048 (it starts at the beginning of the file and is 2048 bytes long).
The original BIOS image data exists from offset 2049 to the end of the file.
```

I wrote some simple tooling in Python to extract a BIOS image from a CAP file (decapify.py) and reconstruct a CAP file from a BIOS image (capify.py).  
My tooling takes advantage of the fact that the Z10PE-D16 WS firmware doesn't seem to verify the CAP file header signature against the embedded BIOS image. The original CAP header can be used with a modified BIOS image. My capify.py tool just contains the bytes for the original CAP file header for BIOS version 4101, which it concatenates with any given BIOS file.  
Here's a link to my original post about these files in the overclock.net forums:  
https://www.overclock.net/threads/asus-z10pe-d16-ws-owners-thread.1579548/post-28762030
```
Instructions:

    Download BIOS image 4101 from ASUS.
    Use decapify.py to extract the BIOS image for AMIBCP
        Example: python3 decapify.py Z10PE-D16-WS-ASUS-4101.CAP bios.bin
    Use AMIBCP to edit bios.bin to add in support for bifurcation. Save to a filename like mod-bios.bin.
        Here's my description of how the PCIe slots are mapped.
    Use capify.py to construct a new CAP file. It uses the CAP header from the original 4101 CAP file, making it possible to use USB Flashback.
        Example: python3 capify.py mod-bios.bin Z1016WS.CAP
    Flash Z1016WS.CAP to your board.
```

Once extracted, the BIOS file can be edited using some kind of standard tool such as AMIBCP.  
