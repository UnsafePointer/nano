class MemoryAddressOutOfBoundsException(Exception):
    pass

class Memory(object):
    PROGRAM_OFFSET = 0x0600
    STACK_OFFSET = 0x100
    STACK_ORIGIN = 0xff

    def __init__(self):
        self._store = {}
        self.pc = self.PROGRAM_OFFSET
        self.sp = self.STACK_ORIGIN

    def load(self, bytes):
        start = self.PROGRAM_OFFSET
        for idx, byte in enumerate(bytes):
            self._store[start + idx] = byte

    def _validate_address(self, addr):
        if addr >= 0xffff: # 16-bit memory address space
            raise MemoryAddressOutOfBoundsException

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._validate_address(key)
        self._store[key] = (value & 0xff) # values can only be 1 byte

    def next(self):
        value = self._store[self.pc]
        self.pc += 1
        return value

    def jump(self, addr):
        self._validate_address(addr)
        self.pc = addr

    def branch(self, verify, addr):
        self._validate_address(addr)
        if not verify:
            return
        self.pc = addr
