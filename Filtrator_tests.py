import unittest
from filtrator import check_correctness, parse_file_name, parse_min_length,\
    parse_keep_filtered, parse_gc_bounds, parse_output_base_name


class TestParsing(unittest.TestCase):
    def setUp(self):
        self.arguments_1 = ['python', 'Fastq_filtrator.py',  # correct record
                            '--min_length', '10',
                            '--gc_bounds', '40', '60',
                            '--keep_filtered',
                            '--output_base_name', 'out',
                            'file.fastq']
        self.arguments_2 = ['python', 'Fastq_filtrator.py',  # less arguments
                            '--help']
        self.arguments_3 = ['python', 'Fastq_filtrator.py',  # mistake in arguments
                            '--min_len', '10',
                            '--keep_filtered',
                            'file.fast']
        self.arguments_4 = ['value', 'file.fastq']  # for check if no arg
        self.arguments_5 = ['--min_length', '10.5']  # incorrect/not defined value min_length
        self.arguments_6 = ['--gc_bounds', '40.5']  # incorrect/not defined value gc_bounds
        self.arguments_7 = ['--gc_bounds', '60', '40']  # incorrect order gc_bounds
        self.arguments_8 = ['--gc_bounds', '40', 'value']  # one value gc_bounds
        self.arguments_9 = ['--output_base_name',  # # output_base_name is not specified
                            'file.fastq']

    def test_check_correctness(self):
        self.assertEqual(check_correctness(self.arguments_1), True)
        with self.assertRaises(ValueError):
            check_correctness(self.arguments_2)
        with self.assertRaises(ValueError):
            check_correctness(self.arguments_3)

    def test_parse_file_name(self):
        self.assertEqual(parse_file_name(self.arguments_1), 'file.fastq')
        with self.assertRaises(ValueError):
            parse_file_name(self.arguments_3)

    def test_parse_min_length(self):
        self.assertEqual((parse_min_length(self.arguments_1),
                          parse_min_length(self.arguments_4)), (10, 0))
        with self.assertRaises(ValueError):
            parse_min_length(self.arguments_5)

    def test_parse_keep_filtered(self):
        self.assertEqual((parse_keep_filtered(self.arguments_1),
                          parse_keep_filtered(self.arguments_4)), (1, 0))

    def test_parse_gc_bounds(self):
        self.assertEqual((parse_gc_bounds(self.arguments_1),
                          parse_gc_bounds(self.arguments_4),
                          parse_gc_bounds(self.arguments_8)),
                         ((40, 60), (None, 101), (40, 101)))
        with self.assertRaises(ValueError):
            parse_gc_bounds(self.arguments_6)
        with self.assertRaises(ValueError):
            parse_gc_bounds(self.arguments_7)

    def test_parse_output_base_name(self):
        self.assertEqual((parse_output_base_name(self.arguments_1),
                          parse_output_base_name(self.arguments_4)), ('out', 'file'))
        with self.assertRaises(ValueError):
            parse_output_base_name(self.arguments_9)


if __name__ == "__main__":
    unittest.main()
