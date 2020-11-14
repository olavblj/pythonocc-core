#!/usr/bin/env python

##Copyright 2009 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.Core.TopoDS import TopoDS_Compound

from OCC.Extend.TopologyUtils import TopologyExplorer

from OCC.Extend.DataExchange.STEP import (read_step_file, write_step_file,
                                          read_step_file_with_names_colors)
from OCC.Extend.DataExchange.STL import read_stl_file, write_stl_file
from OCC.Extend.DataExchange.IGES import read_iges_file, write_iges_file
from OCC.Extend.DataExchange.SVG import export_shape_to_svg, HAVE_SVGWRITE
from OCC.Extend.DataExchange.XDE import DocFromSTEP, SceneGraphFromDoc
from OCC.Extend.DataExchange.X3D import (X3DShapeExporter, X3DCurveExporter,
                                         X3DSceneExporter, X3DFromSceneGraph)


SAMPLES_DIRECTORY = os.path.join('.', 'test_io')

def get_test_fullname(filename):
    return os.path.join(SAMPLES_DIRECTORY, filename)

# the sample files
STEP_AP203_SAMPLE_FILE = get_test_fullname('as1_pe_203.stp')
STEP_AP214_SAMPLE_FILE = get_test_fullname('as1-oc-214.stp')
STEP_MULTIPLE_ROOT = get_test_fullname('stp_multiple_shp_at_root.stp')
IGES_SAMPLE_FILE = get_test_fullname('sunglasses_lens.igs')
STL_ASCII_SAMPLE_FILE = get_test_fullname('bottle_ascii.stl')
STL_BINARY_SAMPLE_FILE = get_test_fullname('cube_binary.stl')

# the basic geometry to test exporters
A_TOPODS_SHAPE = BRepPrimAPI_MakeTorus(200, 50).Shape()

class TestExtendDataExchange(unittest.TestCase):

    def test_read_step_file(self):
        read_step_file(STEP_AP203_SAMPLE_FILE)
        read_step_file(STEP_AP214_SAMPLE_FILE)


    def test_deprecation_warning(self):
        from OCC.Extend.DataExchange import read_step_file
        with self.assertWarns(DeprecationWarning):
            read_step_file(STEP_AP203_SAMPLE_FILE)

    def test_read_step_file_multiple_shape_as_root(self):
        t = read_step_file(STEP_MULTIPLE_ROOT, as_compound=True)
        self.assertTrue(isinstance(t, TopoDS_Compound))

        l = read_step_file(STEP_MULTIPLE_ROOT, as_compound=False)
        self.assertEqual(len(l), 3)


    def test_read_step_file_names_colors(self):
        read_step_file_with_names_colors(STEP_AP203_SAMPLE_FILE)
        read_step_file_with_names_colors(STEP_AP214_SAMPLE_FILE)


    def test_read_iges_file(self):
        read_iges_file(IGES_SAMPLE_FILE)


    def test_read_stl_file(self):
        read_stl_file(STL_ASCII_SAMPLE_FILE)
        read_stl_file(STL_BINARY_SAMPLE_FILE)


    def test_export_shape_to_svg(self):
        if HAVE_SVGWRITE:
            svg_filename = get_test_fullname('sample.svg')
            export_shape_to_svg(A_TOPODS_SHAPE, svg_filename)
            self.assertTrue(os.path.isfile(svg_filename))


    def test_write_step_ap203(self):
        ap203_filename = get_test_fullname("sample_ap_203.stp")
        write_step_file(A_TOPODS_SHAPE,
                        ap203_filename,
                        application_protocol="AP203")
        self.assertTrue(os.path.isfile(ap203_filename))


    def test_write_step_ap214(self):
        as214_filename = get_test_fullname("sample_214.stp")
        write_step_file(A_TOPODS_SHAPE,
                        as214_filename,
                        application_protocol="AP214IS")
        self.assertTrue(os.path.isfile(as214_filename))


    def test_write_step_ap242(self):
        ap242_filename = get_test_fullname("sample_242.stp")
        write_step_file(A_TOPODS_SHAPE,
                        ap242_filename,
                        application_protocol="AP242DIS")
        self.assertTrue(os.path.isfile(ap242_filename))


    def test_write_iges(self):
        iges_filename = get_test_fullname("sample.igs")
        write_iges_file(A_TOPODS_SHAPE, iges_filename)
        self.assertTrue(os.path.isfile(iges_filename))


    def test_stl_ascii(self):
        stl_ascii_filename  = get_test_fullname("sample_ascii.stl")
        write_stl_file(A_TOPODS_SHAPE,
                       stl_ascii_filename,
                       mode="ascii")
        self.assertTrue(os.path.isfile(stl_ascii_filename))


    def test_stl_binary(self):
        stl_binary_filename = get_test_fullname("sample_binary.stl")
        write_stl_file(A_TOPODS_SHAPE,
                       stl_binary_filename,
                       mode="binary")
        self.assertTrue(os.path.isfile(stl_binary_filename))


    def test_doc_from_step(self):
        json_out = get_test_fullname("sc.json")
        doc_exp = DocFromSTEP(STEP_AP203_SAMPLE_FILE)
        document = doc_exp.get_doc()
        sg = SceneGraphFromDoc(document, log=True)
        sg.save_as_json(json_out)
        self.assertTrue(os.path.isfile(json_out))


    def test_x3d_shape_exporter(self):
        x3d_shp_exporter_1 = X3DShapeExporter(A_TOPODS_SHAPE, compute_normals=False, compute_edges=False)
        x3d_shp_exporter_1.to_x3d_graph()
        x3d_shp_exporter_2 = X3DShapeExporter(A_TOPODS_SHAPE, compute_normals=False, compute_edges=True)
        x3d_shp_exporter_2.to_x3d_graph()
        x3d_shp_exporter_3 = X3DShapeExporter(A_TOPODS_SHAPE, compute_normals=True, compute_edges=True)
        x3d_shp_exporter_3.to_x3d_graph()


    def test_step_to_x3d(self):
        doc_exp = DocFromSTEP(STEP_AP203_SAMPLE_FILE)
        document = doc_exp.get_doc()
        scenegraph = SceneGraphFromDoc(document)
        x3d_xml = X3DFromSceneGraph(scenegraph.get_scene(), scenegraph.get_internal_face_entries(), log=True)
        x3d_xml.to_xml()
        x3d_xml.to_x3dom_html()


    def test_x3d_curve_exporter(self):
        for e in TopologyExplorer(A_TOPODS_SHAPE).edges():
            X3DCurveExporter(e)
        for w in TopologyExplorer(A_TOPODS_SHAPE).wires():
            X3DCurveExporter(w)


    def test_x3d_scene(self):
        x3d_scene = X3DSceneExporter()
        x3d_scene.add_shape(A_TOPODS_SHAPE, shape_color=(0.5, 0.5, 0.5), emissive=True)
        x3d_scene.to_x3dom_html()


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestExtendDataExchange))
    return test_suite

if __name__ == "__main__":
    unittest.main()
