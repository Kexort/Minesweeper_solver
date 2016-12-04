from ctypes import *
from ctypes.wintypes import *
import sys

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle


#https://msdn.microsoft.com/en-us/library/windows/desktop/ms684880(v=vs.85).aspx
PROCESS_ALL_ACCESS = 0x1F0FFF 

pid = int(sys.argv[1])   #We get the process id from the first argument
base_address = 0x1000000  #Base address of the executable

#offsets from Cheat Engine
width_offset = 0x5334 
height_offset = 0x5338
field_offset = 0x5361

width = c_int(0)
height = c_int(0)

mine_field = (c_ubyte * (30 * 30))()
cast(mine_field, POINTER(c_ubyte))

bytesRead = c_ulong(0)


processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

ReadProcessMemory(processHandle, base_address + width_offset, byref(width), sizeof(width), byref(bytesRead))
ReadProcessMemory(processHandle, base_address + height_offset, byref(height), sizeof(height), byref(bytesRead))

ReadProcessMemory(processHandle, base_address + field_offset, mine_field, 30 * 30, byref(bytesRead))

for x in xrange(0,width.value+1):
    print "{:>3}".format(x),
print ""

for y in xrange(0,height.value):
    print "{:>3} ".format(y+1),
    for x in xrange(0,width.value):
        if mine_field[y*32+x] == 0x8F:
            print " * ",
        else:
            print "   ",
    print ""

CloseHandle(processHandle)