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

##
## Test array support by IronPython (System.Array)
##

import unittest

from iptest import IronPythonTestCase, is_netstandard, is_cli, is_posix

if is_cli:
    import System

class ArrayTest(IronPythonTestCase):

    @unittest.skipUnless(is_cli, 'IronPython specific test')
    def test_sanity(self):
        # 1-dimension array
        array1 = System.Array.CreateInstance(int, 2)
        for i in range(2): array1[i] = i * 10
        
        self.assertRaises(IndexError, lambda: array1[2])
            
        array2 = System.Array.CreateInstance(int, 4)
        for i in range(2, 6): array2[i - 2] = i * 10

        array3 = System.Array.CreateInstance(float, 3)
        array3[0] = 2.1
        array3[1] = 3.14
        array3[2] = 0.11

        ## __setitem__/__getitem__
        System.Array.__setitem__(array3, 2, 0.14)
        self.assertEqual(System.Array.__getitem__(array3, 1), 3.14)
        self.assertEqual([x for x in System.Array.__getitem__(array3, slice(2))], [2.1, 3.14])

        ## __repr__

        # 2-dimension array
        array4 = System.Array.CreateInstance(int, 2, 2)
        array4[0, 1] = 1
        self.assertTrue(repr(array4).startswith("<2 dimensional Array[int] at"), "bad repr for 2-dimensional array")

        # 3-dimension array
        array5 = System.Array.CreateInstance(object, 2, 2, 2)
        array5[0, 1, 1] = int
        self.assertTrue(repr(array5).startswith("<3 dimensional Array[object] at "), "bad repr for 3-dimensional array")

        ## index access
        self.assertRaises(TypeError, lambda : array5['s'])
        def f1(): array5[0, 1] = 0
        self.assertRaises(ValueError, f1)
        def f2(): array5['s'] = 0
        self.assertRaises(TypeError, f2)

        ## __add__/__mul__
        for f in (
            lambda a, b : System.Array.__add__(a, b),
            lambda a, b : a + b
            ) :
            
            temp = System.Array.__add__(array1, array2)
            result = f(array1, array2)
            
            for i in range(6): self.assertEqual(i * 10, result[i])
            self.assertEqual(repr(result), "Array[int]((0, 10, 20, 30, 40, 50))")
            
            result = f(array1, array3)
            self.assertEqual(len(result), 2 + 3)
            self.assertEqual([x for x in result], [0, 10, 2.1, 3.14, 0.14])
            
            self.assertRaises(NotImplementedError, f, array1, array4)
            
        for f in [
            lambda a, x: System.Array.__mul__(a, x),
            lambda a, x: array1 * x
            ]:

            self.assertEqual([x for x in f(array1, 4)], [0, 10, 0, 10, 0, 10, 0, 10])
            self.assertEqual([x for x in f(array1, 5)], [0, 10, 0, 10, 0, 10, 0, 10, 0, 10])
            self.assertEqual([x for x in f(array1, 0)], [])
            self.assertEqual([x for x in f(array1, -10)], [])

    @unittest.skipUnless(is_cli, 'IronPython specific test')
    def test_slice(self):
        array1 = System.Array.CreateInstance(int, 20)
        for i in range(20): array1[i] = i * i
        
        # positive
        array1[::2] = [x * 2 for x in range(10)]

        for i in range(0, 20, 2):
            self.assertEqual(array1[i], i)
        for i in range(1, 20, 2):
            self.assertEqual(array1[i], i * i)

        # negative: not-same-length
        def f(): array1[::2] = [x * 2 for x in range(11)]
        self.assertRaises(ValueError, f)

    @unittest.skipUnless(is_cli, 'IronPython specific test')
    def test_creation(self):
        t = System.Array
        ti = type(System.Array.CreateInstance(int, 1))

        self.assertRaises(TypeError, t, [1, 2])
        for x in (ti([1,2]), t[int]([1, 2]), ti([1.5, 2.3])):
            self.assertEqual([i for i in x], [1, 2])
            t.Reverse(x)
            self.assertEqual([i for i in x], [2, 1])

    @unittest.skipUnless(is_cli, 'IronPython specific test')
    def test_nonzero_lowerbound(self):
        a = System.Array.CreateInstance(int, (5,), (5,))
        for i in xrange(5): a[i] = i
        
        self.assertArrayEqual(a[:2], System.Array[int]((0,1)))
        self.assertArrayEqual(a[2:], System.Array[int]((2,3,4)))
        self.assertArrayEqual(a[2:4], System.Array[int]((2,3)))
        self.assertEqual(a[-1], 4)

        self.assertEqual(repr(a), 'Array[int]((0, 1, 2, 3, 4))')

        a = System.Array.CreateInstance(int, (5,), (15,))
        b = System.Array.CreateInstance(int, (5,), (20,))
        self.assertArrayEqual(a,b)

        ## 5-dimension
        a = System.Array.CreateInstance(int, (2,2,2,2,2), (1,2,3,4,5))
        self.assertEqual(a[0,0,0,0,0], 0)

        for i in range(5):
            index = [0,0,0,0,0]
            index[i] = 1
            
            a[index[0], index[1], index[2], index[3], index[4]] = i
            self.assertEqual(a[index[0], index[1], index[2], index[3], index[4]], i)
            
        for i in range(5):
            index = [0,0,0,0,0]
            index[i] = 0
            
            a[index[0], index[1], index[2], index[3], index[4]] = i
            self.assertEqual(a[index[0], index[1], index[2], index[3], index[4]], i)

        def sliceArray(arr, index):
            arr[:index]

        def sliceArrayAssign(arr, index, val):
            arr[:index] = val

        self.assertRaises(NotImplementedError, sliceArray, a, 1)
        self.assertRaises(NotImplementedError, sliceArray, a, 200)
        self.assertRaises(NotImplementedError, sliceArray, a, -200)
        self.assertRaises(NotImplementedError, sliceArrayAssign, a, -200, 1)
        self.assertRaises(NotImplementedError, sliceArrayAssign, a, 1, 1)

    @unittest.skipUnless(is_cli, 'IronPython specific test')
    def test_array_type(self):
        
        def type_helper(array_type, instance):
            #create the array type
            AT = System.Array[array_type]
            
            a0 = AT([])
            a1 = AT([instance])
            a2 = AT([instance, instance])
                    
            a_normal = System.Array.CreateInstance(array_type, 3)
            self.assertTrue(str(AT)==str(type(a_normal)))
            for i in xrange(3):
                a_normal[i] = instance
                self.assertTrue(str(AT)==str(type(a_normal)))
    
            a_multi  = System.Array.CreateInstance(array_type, 2, 3)
            self.assertTrue(str(AT)==str(type(a_multi)))
            for i in xrange(2):
                for j in xrange(3):
                    self.assertTrue(str(AT)==str(type(a_multi)))
                    a_multi[i, j]=instance
                    
            self.assertTrue(str(AT)==str(type(a0)))
            self.assertTrue(str(AT)==str(type(a0[0:])))
            self.assertTrue(str(AT)==str(type(a0[:0])))
            self.assertTrue(str(AT)==str(type(a1)))
            self.assertTrue(str(AT)==str(type(a1[1:])))
            self.assertTrue(str(AT)==str(type(a1[:0])))
            self.assertTrue(str(AT)==str(type(a_normal)))
            self.assertTrue(str(AT)==str(type(a_normal[:0])))
            self.assertTrue(str(AT)==str(type(a_normal[3:])))
            self.assertTrue(str(AT)==str(type(a_normal[4:])))
            self.assertTrue(str(AT)==str(type(a_normal[1:])))
            self.assertTrue(str(AT)==str(type(a_normal[1:1:50])))
            self.assertTrue(str(AT)==str(type(a_multi)))
            def silly(): a_multi[0:][1:0]
            self.assertRaises(NotImplementedError, silly)
            self.assertTrue(str(AT)==str(type((a0+a1)[:0])))
                
        type_helper(int, 0)
        type_helper(int, 1)
        type_helper(int, 100)
        type_helper(bool, False)
        type_helper(bool, True)
        #type_helper(bool, 1)
        type_helper(long, 0L)
        type_helper(long, 1L)
        type_helper(long, 100L)
        type_helper(float, 0.0)
        type_helper(float, 1.0)
        type_helper(float, 3.14)
        type_helper(str, "")
        type_helper(str, " ")
        type_helper(str, "abc")

    @unittest.skipUnless(is_cli, 'IronPython specific test')
    def test_tuple_indexer(self):
        array1 = System.Array.CreateInstance(int, 20, 20)
        array1[0,0] = 5
        self.assertEqual(array1[0,0], array1[(0,0)])

if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(__name__)
