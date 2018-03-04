import unittest

from memory import Memory
from memory import MemoryAddressOutOfBoundsException
from memory import MemoryStackOverflow

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.sut = Memory()

    def test_initialized_with_defaults(self):
        self.assertEqual(self.sut.pc, 0x600)
        self.assertEqual(self.sut.sp, 0xff)

    def test_load_to_memory(self):
        bytes = [0xff, 0xee, 0xdd]
        self.sut.load(bytes)
        self.assertEqual(self.sut[Memory.PROGRAM_OFFSET], 0xff)
        self.assertEqual(self.sut[Memory.PROGRAM_OFFSET + 1], 0xee)
        self.assertEqual(self.sut[Memory.PROGRAM_OFFSET + 2], 0xdd)

    def test_set_get_item(self):
        self.sut[0xff] = 0xee
        self.assertEqual(self.sut[0xff], 0xee)

    def test_address_out_of_bounds(self):
        self.assertRaises(MemoryAddressOutOfBoundsException, self.sut.__setitem__, 0x10000, 0xff)
        self.assertRaises(MemoryAddressOutOfBoundsException, self.sut.jump, 0x10000)

    def test_value_out_of_bounds(self):
        self.sut[0xff] = 0x10e
        self.assertEqual(self.sut[0xff], 0xe)

    def test_next(self):
        bytes = [0xff, 0xee, 0xdd]
        self.sut.load(bytes)
        self.assertEqual(self.sut.next(), 0xff)
        self.assertEqual(self.sut.next(), 0xee)
        self.assertEqual(self.sut.next(), 0xdd)

    def test_jump(self):
        self.sut.jump(0xff)
        self.assertEqual(self.sut.pc, 0xff)

    def test_branch_when_eval_false(self):
        self.sut.branch(False, 0xff)
        self.assertNotEqual(self.sut.pc, 0xff)

    def test_branch_when_eval_true(self):
        self.sut.branch(True, 0xff)
        self.assertEqual(self.sut.pc, 0xff)

    def test_split_bytes(self):
        high, low = self.sut._split_bytes(0xeeff)
        self.assertEqual(high, 0xee)
        self.assertEqual(low, 0xff)

    def test_create_16_bit_addr(self):
        addr = self.sut._create_16_bit_addr(0xee, 0xff)
        self.assertEqual(addr, 0xeeff)

    def test_stack_overflow(self):
        self.assertRaises(MemoryStackOverflow, self.sut.pull)
        for i in xrange(255):
            self.sut.push(0xff)
        self.assertRaises(MemoryStackOverflow, self.sut.push, 0xff)

    def test_push_to_stack(self):
        self.sut.push(0xff)
        self.sut.push(0xee)
        self.sut.push(0xdd)
        self.assertEqual(self.sut.sp, Memory.STACK_ORIGIN - 3)
        self.assertEqual(self.sut.pull(), 0xdd)
        self.assertEqual(self.sut.pull(), 0xee)
        self.assertEqual(self.sut.pull(), 0xff)
        self.assertEqual(self.sut.sp, Memory.STACK_ORIGIN)

    def test_jsr_rts(self):
        self.sut.jsr(0xeeff)
        self.sut.jsr(0xddcc)
        self.assertEqual(self.sut.pc, 0xddcc)

        self.sut.rts()
        self.assertEqual(self.sut.pc, 0xeeff)

        self.sut.rts()
        self.assertEqual(self.sut.pc, Memory.PROGRAM_OFFSET)

