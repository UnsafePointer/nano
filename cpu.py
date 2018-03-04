class CPUNotARegistry(Exception):
    pass

class CPU(object):
    def __init__(self):
        self._registers = { 'a': 0, 'x': 0, 'y': 0 }
        self._flags = { 'z': 0, 'c': 0, 'n': 0 }

    def result(self, value):
        value &= 0xff # values can only be 1 byte

        self._flags['z'] = 1 if value == 0 else 0
        self._flags['n'] = 1 if value >= 0x80 else 0

        return value

    def __getitem__(self, key):
        if key in self._registers:
            return self._registers[key]
        return self._flags[key]

    def __setitem__(self, key, value):
        if not key in self._registers:
            raise CPUNotARegistry("{} is not a registry".format(key))
        self._registers[key] = self.result(value)

    def set_carry(self):
        self._flags['c'] = 1

    def clear_carry(self):
        self._flags['c'] = 0

    def carry_if(self, verify):
        if verify:
            self.set_carry()
        else:
            self.clear_carry()
