# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

def write_asm(filename, asm):
  filename = filename.split("/")[-1]
  filename = filename.split(".")[0]
  filename += ".ami"
  with open(filename, "w") as f:
    f.write(asm)
    f.close()
  return