#####################################################################################
#
#  Copyright (c) Microsoft Corporation. All rights reserved.
#
# This source code is subject to terms and conditions of the Apache License, Version 2.0. A
# copy of the license can be found in the License.html file at the root of this distribution. If
# you cannot locate the  Apache License, Version 2.0, please send an email to
# ironpy@microsoft.com. By using this source code in any fashion, you are agreeing to be bound
# by the terms of the Apache License, Version 2.0.
#
# You must not remove this notice, or any other, from this software.
#
#
#####################################################################################

#
# test Microsoft.Scripting.Math
#

import unittest

from iptest import IronPythonTestCase, is_cli, is_netstandard

@unittest.skipUnless(is_cli, 'IronPython specific test case')
class IronMathTest(IronPythonTestCase):
    def setUp(self):
        super(IronMathTest, self).setUp()

        import clr
        from System import IFormatProvider
        class myFormatProvider(IFormatProvider):
            def ToString():pass
    
        self.p = myFormatProvider()
        
        clr.AddReference((1L).GetType().Assembly)
        self.load_iron_python_test()

    def test_bigint(self):
        from System import Char, IConvertible
        from System.Numerics import BigInteger, Complex
        self.assertEqual(BigInteger.Add(1L,99999999999999999999999999999999999999999999999999999999999L) ,BigInteger.Subtract(100000000000000000000000000000000000000000000000000000000001L,1L))
        self.assertEqual(BigInteger.Multiply(400L,500L) , BigInteger.Divide(1000000L,5L))
        self.assertEqual(BigInteger.Multiply(400L,8L) , BigInteger.LeftShift(400L,3L))
        self.assertEqual(BigInteger.Divide(400L,8L) , BigInteger.RightShift(400L,3L))
        self.assertEqual(BigInteger.RightShift(BigInteger.LeftShift(400L,100L),100L) , 400L)
        self.assertEqual(BigInteger.RightShift(BigInteger.LeftShift(-12345678987654321L,100L),100L) , -12345678987654321L)
        self.assertRaises(ValueError, BigInteger.RightShift, 400L, -100L)
        self.assertRaises(ValueError, BigInteger.LeftShift, 400L, -100L)
        self.assertRaises(ValueError, BigInteger.RightShift, -12345678987654321L, -100L)
        self.assertRaises(ValueError, BigInteger.LeftShift, -12345678987654321L, -100L)
        self.assertEqual(BigInteger(-123456781234567812345678123456781234567812345678123456781234567812345678L).OnesComplement().OnesComplement() , -123456781234567812345678123456781234567812345678123456781234567812345678L)
        self.assertEqual(BigInteger(-1234567812345678123456781234567812345678123456781234567812345678123456781234567812345678L).OnesComplement() , -(-1234567812345678123456781234567812345678123456781234567812345678123456781234567812345678L + 1L ))
        self.assertTrue(BigInteger.Xor(-1234567812345678123456781234567812345678123456781234567812345678123456781234567812345678L,BigInteger(-1234567812345678123456781234567812345678123456781234567812345678123456781234567812345678L).OnesComplement()) , -1L)
        self.assertEqual(BigInteger.BitwiseAnd(0xff00ff00,BigInteger.BitwiseOr(0x00ff00ff,0xaabbaabb)) , BigInteger(0xaa00aa00))
        self.assertEqual(BigInteger.Mod(BigInteger(-9999999999999999999999999999999999999999),1000000000000000000) , -BigInteger.Mod(9999999999999999999999999999999999999999,BigInteger(-1000000000000000000)))
        
        self.assertEqual(BigInteger.ToInt64(0x7fffffffffffffff) , 9223372036854775807L)
        self.assertRaises(OverflowError, BigInteger.ToInt64, 0x8000000000000000)
        
        self.assertEqual(BigInteger(-0).ToBoolean(self.p) , False )
        self.assertEqual(BigInteger(-1212321.3213).ToBoolean(self.p) , True )
        self.assertEqual(BigInteger(1212321384892342394723947L).ToBoolean(self.p) , True )
        
        self.assertEqual(BigInteger(0L).ToChar(self.p) , Char.MinValue)
        self.assertEqual(BigInteger(65L).ToChar(self.p) , IConvertible.ToChar('A', self.p))
        self.assertEqual(BigInteger(0xffff).ToChar(self.p) , Char.MaxValue)
        self.assertRaises(OverflowError, BigInteger(-1).ToChar, self.p)
        
        self.assertEqual(BigInteger(100).ToDouble(self.p) , 100.0)
        self.assertEqual(BigInteger(BigInteger(100).ToDouble(self.p)).ToSingle(self.p) , BigInteger(100.1213123).ToFloat())
        
        self.assertTrue(BigInteger(100) != 100.32)
        self.assertEqual(BigInteger(100) , 100.0)
        
        self.assertTrue( 100.32 != BigInteger(100))
        self.assertEqual(100.0 , BigInteger(100) )

    def test_big_1(self):
        from System import SByte, Byte, Int16, UInt16, Int32, UInt32, Int64, UInt64
        from System.Numerics import BigInteger
        for (a, m, t,x) in [
                            (7, "ToSByte",  SByte,2),
                            (8, "ToByte",   Byte, 0),
                            (15, "ToInt16", Int16,2),
                            (16, "ToUInt16", UInt16,0),
                            (31, "ToInt32", Int32,2),
                            (32, "ToUInt32", UInt32,0),
                            (63, "ToInt64", Int64,2),
                            (64, "ToUInt64", UInt64,0)
                        ]:
        
            b = BigInteger(-x ** a )
            left = getattr(b, m)(self.p)
            right = t.MinValue
            self.assertEqual(left, right)
            
            b = BigInteger(2 ** a -1)
            left = getattr(b, m)(self.p)
            right = t.MaxValue
            self.assertEqual(left, right)
        
            b = BigInteger(0L)
            left = getattr(b, m)(self.p)
            right = t.MaxValue - t.MaxValue
            self.assertEqual(left, 0)

            self.assertRaises(OverflowError,getattr(BigInteger(2 ** a ), m),self.p)
            self.assertRaises(OverflowError,getattr(BigInteger(-1 - x ** a ), m),self.p)


    def test_big_2(self):
        from System import Int32, UInt32, Int64, UInt64
        from System.Numerics import BigInteger
        for (a, m, t,x) in [
                            (31, "ToInt32",Int32,2),
                            (32, "ToUInt32",UInt32,0),
                            (63, "ToInt64",Int64,2),
                            (64, "ToUInt64",UInt64,0)
                        ]:
        
            b = BigInteger(-x ** a )
            left = getattr(b, m)()
            right = t.MinValue
            self.assertEqual(left, right)

            b = BigInteger(2 ** a -1)
            left = getattr(b, m)()
            right = t.MaxValue
            self.assertEqual(left, right)
        
            b = BigInteger(0L)
            left = getattr(b, m)()
            right = t.MaxValue - t.MaxValue
            self.assertEqual(left, right)

            self.assertRaises(OverflowError,getattr(BigInteger(2 ** a ), m))
            self.assertRaises(OverflowError,getattr(BigInteger(-1 - x ** a ), m))


    def test_complex(self):
        from System.Numerics import BigInteger, Complex
        self.assertEqual(
            Complex.Add(
                Complex(BigInteger(9999L), -1234),
                Complex.Conjugate(Complex(9999, -1234)) ),
            Complex.Multiply(BigInteger(9999L), 2) )
        self.assertEqual(
            Complex.Add(
                Complex(99999.99e-200, 12345.88e+100),
                Complex.Negate(Complex(99999.99e-200, 12345.88e+100)) ),
            Complex.Subtract(
                Complex(99999.99e-200, 12345.88e+100),
                Complex(99999.99e-200, 12345.88e+100) ))
        self.assertEqual(
            Complex.Divide(4+2j,2),
            (2 + 1j) )
        self.assertTrue(not hasattr(Complex, "Mod"))  #IP 1.x had limited support for modulo which has been removed

    def test_bool_misc(self):
        from System.Numerics import BigInteger
        def is_zero(bigint):
            return bigint.IsZero
        
        self.assertEqual(BigInteger(-1234).Sign, -1)
        self.assertEqual(is_zero(BigInteger(-1234)), False)
        self.assertEqual(BigInteger(-1234).IsNegative(), True)
        self.assertEqual(BigInteger(-1234).IsPositive(), False)
        
        self.assertEqual(BigInteger(0).Sign, 0)
        self.assertEqual(is_zero(BigInteger(0)), True)
        self.assertEqual(BigInteger(0).IsNegative(), False)
        self.assertEqual(BigInteger(0).IsPositive(), False)

        self.assertEqual(BigInteger(1234).Sign, 1)
        self.assertEqual(is_zero(BigInteger(1234)), False)
        self.assertEqual(BigInteger(1234).IsNegative(), False)
        self.assertEqual(BigInteger(1234).IsPositive(), True)


    def test_byte_conversions(self):
        from System import Array, Byte
        from System.Numerics import BigInteger

        def CheckByteConversions(bigint, bytes):
            self.assertSequenceEqual(bigint.ToByteArray(), bytes)
            self.assertEqual(BigInteger.Create(Array[Byte](bytes)), bigint)

        CheckByteConversions(BigInteger(0x00), [0x00])

        CheckByteConversions(BigInteger(-0x01), [0xff])
        CheckByteConversions(BigInteger(-0x81), [0x7f, 0xff])
        CheckByteConversions(BigInteger(-0x100), [0x00, 0xff])
        CheckByteConversions(BigInteger(-0x1000), [0x00, 0xf0])
        CheckByteConversions(BigInteger(-0x10000), [0x00, 0x00, 0xff])
        CheckByteConversions(BigInteger(-0x100000), [0x00, 0x00, 0xf0])
        CheckByteConversions(BigInteger(-0x10000000), [0x00, 0x00, 0x00, 0xf0])
        CheckByteConversions(BigInteger(-0x100000000), [0x00, 0x00, 0x00, 0x00, 0xff])

        CheckByteConversions(BigInteger(0x7f), [0x7f])
        CheckByteConversions(BigInteger(0xff), [0xff, 0x00])
        CheckByteConversions(BigInteger(0x0201), [0x01, 0x02])
        CheckByteConversions(BigInteger(0xf2f1), [0xf1, 0xf2, 0x00])
        CheckByteConversions(BigInteger(0x03020100), [0x00, 0x01, 0x02, 0x03])
        CheckByteConversions(BigInteger(0x0403020100), [0x00, 0x01, 0x02, 0x03, 0x04])
        CheckByteConversions(BigInteger(0x0706050403020100), [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
        CheckByteConversions(BigInteger(0x080706050403020100), [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

    def test_dword_conversions(self):
        from System import Array, UInt32
        from System.Numerics import BigInteger
        from IronPythonTest import System_Scripting_Math
        def CheckDwordConversions(bigint, dwords):
            self.assertSequenceEqual(bigint.GetWords(), dwords)
            if bigint == BigInteger.Zero:
                self.assertEqual(
                    System_Scripting_Math.CreateBigInteger(
                        0,
                        Array[UInt32](dwords),),
                    bigint)
            else:
                self.assertEqual(
                    System_Scripting_Math.CreateBigInteger(
                        1,
                        Array[UInt32](dwords)),
                    bigint)
                self.assertEqual(
                    System_Scripting_Math.CreateBigInteger(
                        -1,
                        Array[UInt32](dwords)),
                    BigInteger.Negate(bigint))
        
        CheckDwordConversions(BigInteger(0), [0x00000000])
        CheckDwordConversions(BigInteger(1), [0x00000001])
        CheckDwordConversions(BigInteger((1<<31)), [0x80000000])
        CheckDwordConversions(BigInteger(((1<<31) + 9)), [0x80000009])
        CheckDwordConversions(BigInteger((1<<32)), [0x00000000, 0x00000001])

    def test_misc(self):
        from System import ArgumentException, ArgumentNullException
        from System.Numerics import BigInteger
        from IronPythonTest import System_Scripting_Math
        self.assertRaises(ArgumentException, System_Scripting_Math.CreateBigInteger, 0, (1, 2, 3))
        self.assertRaises(ArgumentNullException, System_Scripting_Math.CreateBigInteger, 0, None)

        if not is_netstandard: # TODO: figure out why this doesn't work
            self.assertEqual(BigInteger(1).CompareTo(None), 1)
        self.assertEqual(BigInteger(1).CompareTo(True), 0)

if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(__name__)
