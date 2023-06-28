import sys

if len(sys.argv) != 3:
    print("Usage: python3 decapify.py cap_filename extracted_bios_filename")
    sys.exit(0)

print("Reading CAP file:", sys.argv[1])
with open(sys.argv[1], 'rb') as f:
    cap = f.read()

print("Extracting BIOS image from CAP file.")
bios = cap[2048:]

print("Writing extracted BIOS image file:", sys.argv[2])
with open(sys.argv[2], 'wb') as f:
    f.write(bios)

