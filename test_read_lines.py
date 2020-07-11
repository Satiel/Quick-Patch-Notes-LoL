import os

#set THIS_FOLDER to current absolute path
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

#join together absolute path + file name
patch_version_file = os.path.join(THIS_FOLDER, 'patch_versions.txt')

#open up the file, print each line
f = open(patch_version_file, "r")
#print(f.readlines())

#add all versions into a list, removing the newline character
patch_versions = []
line = f.readline()
while line:
    line = line.strip()
    line = str(line)
    patch_versions.append(line)
    line = f.readline()
f.close()

print(patch_versions)

