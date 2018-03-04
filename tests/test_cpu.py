import unittest
from random import randint as random

from cpu import CPU
from cpu import CPUNotARegistry

class TestCPU(unittest.TestCase):

    def setUp(self):
        self.sut = CPU()

    def test_initialized_with_defaults(self):
        values = self.sut._registers.copy()
        values.update(self.sut._flags)
        for key, value in values.iteritems():
            self.assertEqual(value, 0)

    def test_set_registers(self):
        for key in self.sut._registers:
            value = random(0x00, 0xff)
            self.sut[key] = value
            self.assertEqual(self.sut[key], value)

    def test_not_a_registry(self):
        for key in self.sut._flags:
            value = random(0x00, 0xff)
            self.assertRaises(CPUNotARegistry, self.sut.__setitem__, key, value)

    def test_set_carry(self):
        self.sut.set_carry()
        self.assertEqual(self.sut['c'], 1)
        self.sut.clear_carry()
        self.assertEqual(self.sut['c'], 0)

    def test_carry_if_when_eval_true(self):
        self.sut.carry_if(True)
        self.assertEqual(self.sut['c'], 1)

    def test_carry_if_when_eval_false(self):
        self.sut.carry_if(False)
        self.assertEqual(self.sut['c'], 0)

    def test_value_out_of_bounds(self):
        self.assertEqual(self.sut.result(0xffdd), 0xdd)

    def test_z_flag(self):
        self.sut.result(0x00)
        self.assertEqual(self.sut['z'], 1)
        self.sut.result(0xff)
        self.assertEqual(self.sut['z'], 0)

    def test_n_flag(self):
        self.sut.result(0x7f)
        self.assertEqual(self.sut['n'], 0)
        self.sut.result(0x81)
        self.assertEqual(self.sut['n'], 1)

    def test_implicit_flag_processing_when_setting_registers(self):
        self.sut['a'] = 0xff00
        self.assertEqual(self.sut['a'], 0x00)
        self.assertEqual(self.sut['z'], 1)
        self.assertEqual(self.sut['n'], 0)

        self.sut['x'] = 0xff81
        self.assertEqual(self.sut['x'], 0x81)
        self.assertEqual(self.sut['z'], 0)
        self.assertEqual(self.sut['n'], 1)

