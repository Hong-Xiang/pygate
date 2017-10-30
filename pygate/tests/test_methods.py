# import unittest
# # from fs.memoryfs import MemoryFS as FS
# from fs.tempfs import TempFS as FS
# from pygate import methods


# class TestMethods(unittest.TestCase):
#     def setUp(self):
#         self.fs = FS()
#         for i in range(5):
#             self.fs.makedir('sub.{}'.format(i))
#         for i in range(3):
#             self.fs.touch('test{}.mac'.format(i))
#         for i in range(3):
#             self.fs.touch('result{}.txt'.format(i))
#         self.fs.makedir('testdir')
#         self.fs.touch('testdir/tmp.txt')

#     def tearDown(self):
#         self.fs.close()

#     def test_files(self):
#         expected = set()
#         for i in range(3):
#             expected.add('test{}.mac'.format(i))
#             expected.add('result{}.txt'.format(i))
#         result = set()
#         methods.files(self.fs).subscribe(result.add)
#         self.assertEqual(result, expected)

#     def test_files_exclude(self):
#         expected = {'test{}.mac'.format(i) for i in range(3)}
#         result = set()
#         methods.files(self.fs, exclude_files=['result*']).subscribe(result.add)
#         self.assertEqual(result, expected)

#     def test_subdirs(self):
#         expected = {'sub.{}'.format(i) for i in range(5)}
#         result = set()
#         methods.dirs(self.fs, filters=['sub*']).subscribe(result.add)
#         self.assertEqual(result, expected)

#     def test_mapper_subdirs(self):
#         m = methods.Mapper(self.fs)
#         result = set()
#         m.files('result.txt').subscribe(result.add)
#         expected = {'sub.{}/result.txt'.format(i) for i in range(5)}
#         self.assertEqual(result, expected)
