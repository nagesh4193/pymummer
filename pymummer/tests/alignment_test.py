import unittest
import os
import pyfastaq
from pymummer import alignment, snp, variant

modules_dir = os.path.dirname(os.path.abspath(alignment.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')

class TestNucmer(unittest.TestCase):
    def test_init_nucmer(self):
        '''test __init__ nucmer'''
        line = '\t'.join(['1', '100', '2', '200', '101', '202', '42.42', '123', '456', '-1', '0', 'ref', 'qry', '[FOO]'])
        a = alignment.Alignment(line)
        self.assertEqual(a.ref_start, 0)
        self.assertEqual(a.ref_end, 99)
        self.assertEqual(a.qry_start, 1)
        self.assertEqual(a.qry_end, 199)
        self.assertEqual(a.hit_length_ref, 101)
        self.assertEqual(a.hit_length_qry, 202)
        self.assertEqual(a.percent_identity, 42.42)
        self.assertEqual(a.ref_length, 123)
        self.assertEqual(a.qry_length, 456)
        self.assertEqual(a.frame, -1)
        self.assertEqual(a.ref_name, 'ref')
        self.assertEqual(a.qry_name, 'qry')


    def test_init_promer(self):
        '''test __init__ promer'''
        line = '\t'.join(['1', '1398', '4891054', '4892445', '1398', '1392', '89.55', '93.18', '0.21', '1398', '5349013', '1', '1', 'ref', 'qry', '[CONTAINED]'])

        a = alignment.Alignment(line)
        self.assertEqual(a.ref_start, 0)
        self.assertEqual(a.ref_end, 1397)
        self.assertEqual(a.qry_start, 4891053)
        self.assertEqual(a.qry_end, 4892444)
        self.assertEqual(a.hit_length_ref, 1398)
        self.assertEqual(a.hit_length_qry, 1392)
        self.assertEqual(a.percent_identity, 89.55)
        self.assertEqual(a.ref_length, 1398)
        self.assertEqual(a.qry_length, 5349013)
        self.assertEqual(a.frame, 1)
        self.assertEqual(a.ref_name, 'ref')
        self.assertEqual(a.qry_name, 'qry')


    def test_swap(self):
        ''' test swap'''
        l_in = ['1', '100', '2', '200', '101', '202', '42.42', '123', '456', '-1', '0', 'ref', 'qry']
        l_out = ['2', '200', '1', '100', '202', '101', '42.42', '456', '123', '-1', '0', 'qry', 'ref']
        a_in = alignment.Alignment('\t'.join(l_in))
        a_in._swap()
        self.assertEqual(a_in, alignment.Alignment('\t'.join(l_out)))
        a_in._swap()
        self.assertEqual(a_in, alignment.Alignment('\t'.join(l_in)))


    def test_qry_coords(self):
        '''Test qry_coords'''
        hits = ['\t'.join(['1', '100', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'qry']),
                '\t'.join(['1', '101', '100', '1', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'qry'])
        ]
        for h in hits:
            a = alignment.Alignment(h)
            self.assertEqual(pyfastaq.intervals.Interval(0,99), a.qry_coords())


    def test_ref_coords(self):
        '''Test ref_coords'''
        hits = ['\t'.join(['1', '100', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref']),
                '\t'.join(['100', '1', '100', '1', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref'])
        ]
        for h in hits:
            a = alignment.Alignment(h)
            self.assertEqual(pyfastaq.intervals.Interval(0,99), a.ref_coords())


    def test_on_same_strand(self):
        '''test on_same_strand'''
        self.assertTrue(alignment.Alignment('\t'.join(['1', '100', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref'])).on_same_strand())
        self.assertTrue(alignment.Alignment('\t'.join(['100', '1', '100', '1', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref'])).on_same_strand())
        self.assertFalse(alignment.Alignment('\t'.join(['1', '100', '100', '1', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref'])).on_same_strand())
        self.assertFalse(alignment.Alignment('\t'.join(['100', '1', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref'])).on_same_strand())


    def test_is_self_hit(self):
        '''Test is_self_hit'''
        tests = [('\t'.join(['1', '100', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref']), True),
            ('\t'.join(['1', '101', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref']), False),
            ('\t'.join(['2', '100', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref']), False),
            ('\t'.join(['1', '100', '1', '100', '100', '100', '100.00', '1000', '1000', '1', '1', 'ref', 'ref2']), False),
            ('\t'.join(['1', '100', '1', '100', '100', '100', '99.9', '1000', '1000', '1', '1', 'ref', 'ref']), False),
        ]

        for t in tests:
            a = alignment.Alignment(t[0])
            self.assertEqual(a.is_self_hit(), t[1])


    def test_reverse_reference(self):
        '''Test reverse_reference'''
        aln = alignment.Alignment('\t'.join(['100', '142', '1', '42', '43', '42', '100.00', '150', '100', '1', '1', 'ref', 'qry']))
        expected = alignment.Alignment('\t'.join(['51', '9', '1', '42', '43', '42', '100.00', '150', '100', '1', '1', 'ref', 'qry']))
        aln.reverse_reference()
        self.assertEqual(expected, aln)


    def test_reverse_query(self):
        '''Test reverse_query'''
        aln = alignment.Alignment('\t'.join(['100', '142', '1', '42', '43', '42', '100.00', '150', '100', '1', '1', 'ref', 'qry']))
        expected = alignment.Alignment('\t'.join(['100', '142', '100', '59', '43', '42', '100.00', '150', '100', '1', '1', 'ref', 'qry']))
        aln.reverse_query()
        self.assertEqual(expected, aln)


    def test_str(self):
        '''Test __str__'''
        l_in = ['1', '100', '2', '200', '101', '202', '42.42', '123', '456', '-1', '0', 'ref', 'qry']
        # the 10th column (counting from zero) is ignored and so not output by __str__
        l_out = l_in[:10] + l_in[11:]
        a = alignment.Alignment('\t'.join(l_in))
        self.assertEqual(str(a), '\t'.join(l_out))


    def test_to_msp_crunch(self):
        '''Test to_msp_crunch'''
        l_in = ['100', '110', '1', '10', '10', '11', '80.00', '123', '456', '-1', '0', 'ref', 'qry']
        a = alignment.Alignment('\t'.join(l_in))
        expected = '8 80.00 1 10 qry 100 110 ref'
        self.assertEqual(expected, a.to_msp_crunch())


    def test_qry_coords_from_ref_coord_test_bad_ref_coord(self):
        '''Test qry_coords_from_ref_coord with bad ref coords'''
        aln = alignment.Alignment('\t'.join(['100', '200', '1', '100', '100', '100', '100.00', '300', '300', '1', '1', 'ref', 'qry']))
        with self.assertRaises(alignment.Error):
            got = aln.qry_coords_from_ref_coord(98, [])

        with self.assertRaises(alignment.Error):
            got = aln.qry_coords_from_ref_coord(200, [])


    def test_qry_coords_from_ref_coord_test_same_strand(self):
        '''Test qry_coords_from_ref_coord on same strand'''
        aln = alignment.Alignment('\t'.join(['100', '200', '1', '101', '100', '100', '100.00', '300', '300', '1', '1', 'ref', 'qry']))
        snp1 = snp.Snp('\t'.join(['140', 'A', '.', '40', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from qry
        snp2 = snp.Snp('\t'.join(['141', 'C', '.', '40', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from qry
        del1 = variant.Variant(snp1)
        del2 = variant.Variant(snp1)
        self.assertTrue(del2.update_indel(snp2))
        snp3 = snp.Snp('\t'.join(['150', '.', 'A', '50', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from ref
        snp4 = snp.Snp('\t'.join(['150', '.', 'C', '51', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from ref
        snp5 = snp.Snp('\t'.join(['150', '.', 'G', '52', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from ref
        ins1 = variant.Variant(snp3)
        ins2 = variant.Variant(snp3)
        self.assertTrue(ins2.update_indel(snp4))
        self.assertTrue(ins2.update_indel(snp5))

        tests = [
            (99, [], (0, False)),
            (100, [], (1, False)),
            (199, [], (100, False)),
            (119, [del1], (20, False)),
            (149, [], (50, False)),
            (149, [del1], (49, False)),
            (149, [del2], (48, False)),
            (159, [], (60, False)),
            (159, [ins1], (61, False)),
            (159, [ins2], (63, False)),
            (159, [del1, ins1], (60, False)),
            (159, [del1, ins2], (62, False)),
            (159, [del2, ins1], (59, False)),
            (159, [del2, ins2], (61, False)),
            (139, [del1], (39, True)),
            (149, [ins1], (49, True)),
        ]

        for ref_coord, variant_list, expected in tests:
            got = aln.qry_coords_from_ref_coord(ref_coord, variant_list)
            self.assertEqual(expected, got)
            # if we reverse the direction of hit in query and reference, should get the same answer
            aln.qry_start, aln.qry_end = aln.qry_end, aln.qry_start
            aln.ref_start, aln.ref_end = aln.ref_end, aln.ref_start
            got = aln.qry_coords_from_ref_coord(ref_coord, variant_list)
            self.assertEqual(expected, got)
            aln.qry_start, aln.qry_end = aln.qry_end, aln.qry_start
            aln.ref_start, aln.ref_end = aln.ref_end, aln.ref_start


    def test_qry_coords_from_ref_coord_test_different_strand(self):
        '''Test qry_coords_from_ref_coord on different strand'''
        aln = alignment.Alignment('\t'.join(['100', '200', '101', '1', '100', '100', '100.00', '300', '300', '1', '1', 'ref', 'qry']))
        snp1 = snp.Snp('\t'.join(['140', 'A', '.', '40', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from qry
        snp2 = snp.Snp('\t'.join(['141', 'C', '.', '40', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from qry
        del1 = variant.Variant(snp1)
        del2 = variant.Variant(snp1)
        self.assertTrue(del2.update_indel(snp2))
        snp3 = snp.Snp('\t'.join(['150', '.', 'A', '50', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from ref
        snp4 = snp.Snp('\t'.join(['150', '.', 'C', '51', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from ref
        snp5 = snp.Snp('\t'.join(['150', '.', 'G', '52', 'x', 'x', '300', '300', 'x', 'x', 'ref', 'qry'])) # del from ref
        ins1 = variant.Variant(snp3)
        ins2 = variant.Variant(snp3)
        self.assertTrue(ins2.update_indel(snp4))
        self.assertTrue(ins2.update_indel(snp5))

        tests = [
            (99, [], (100, False)),
            (100, [], (99, False)),
            (199, [], (0, False)),
            (119, [], (80, False)),
            (119, [del1], (80, False)),
            (149, [], (50, False)),
            (149, [del1], (51, False)),
            (149, [del2], (52, False)),
            (159, [], (40, False)),
            (159, [ins1], (39, False)),
            (159, [ins2], (37, False)),
            (159, [del1, ins1], (40, False)),
            (159, [del1, ins2], (38, False)),
            (159, [del2, ins1], (41, False)),
            (159, [del2, ins2], (39, False)),
            (139, [del1], (39, True)),
            (149, [ins1], (49, True)),
        ]

        for ref_coord, variant_list, expected in tests:
            got = aln.qry_coords_from_ref_coord(ref_coord, variant_list)
            self.assertEqual(expected, got)
            # if we reverse the direction of hit in query and reference, should get the same answer
            aln.qry_start, aln.qry_end = aln.qry_end, aln.qry_start
            aln.ref_start, aln.ref_end = aln.ref_end, aln.ref_start
            got = aln.qry_coords_from_ref_coord(ref_coord, variant_list)
            self.assertEqual(expected, got)
            aln.qry_start, aln.qry_end = aln.qry_end, aln.qry_start
            aln.ref_start, aln.ref_end = aln.ref_end, aln.ref_start


