class MemoryAddressOutOfBoundsException(Exception):
    pass

class MemoryStackOverflow(Exception):
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

    def _split_bytes(self, addr): # split 16-bit address values
        self._validate_address(addr)
        high = (addr >> 8) & 0xff
        low = addr & 0xff
        return (high, low)

    def _create_16_bit_addr(self, high, low):
        high &= 0xff # values can only be 1 byte
        low &= 0xff
        high = (high << 8)
        return high + low

    def push(self, value):
        if self.sp - 1 < 0:
            raise MemoryStackOverflow
        value &= 0xff # values can only be 1 byte
        self._store[self.STACK_OFFSET + self.sp] = value
        self.sp -= 1

    def pull(self):
        if self.sp + 1 > self.STACK_ORIGIN:
            raise MemoryStackOverflow
        self.sp += 1
        return self._store[self.STACK_OFFSET + self.sp]

    def jsr(self, addr):
        high, low = self._split_bytes(self.pc)
        self.push(low)
        self.push(high)

        self.jump(addr)

    def rts(self):
        high = self.pull()
        low = self.pull()
        addr = self._create_16_bit_addr(high, low)

        self.jump(addr)
