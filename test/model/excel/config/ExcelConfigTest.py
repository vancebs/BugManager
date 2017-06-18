#!/usr/bin/python
# -*- coding: UTF-8 -*-

from unittest import TestCase

from script.model.excel.ExcelHelper import ExcelHelper
from script.model.excel.config.ExcelConfig import ExcelConfig
from script.model.excel.config.Key import Key
from script.model.excel.config.StyledValue import StyledValue


class ExcelConfigTest(TestCase):

    def tearDown(self):
        super(ExcelConfigTest, self).tearDown()
        if self._mBook is not None:
            self._mBook.close()

    # DIR = 'excel'
    #
    # def test_load(self):
    #     if not os.path.exists(ExcelConfigTest.DIR):
    #         os.makedirs(ExcelConfigTest.DIR)
    #     path = '%s/test_load.xlsm' % ExcelConfigTest.DIR
    #
    #     # copy from template
    #     if os.path.exists(path):
    #         os.remove(path)
    #     shutil.copy('../template/template.xlsm', path)
    #
    #     # load
    #     cfg = ExcelConfig(path)
    #     cfg.load()
    #
    #     # close
    #     cfg.close()

    def test_save(self):
        helper = ExcelHelper()
        self._mBook = helper.create_from_template(
            './excel/test_marco.xlsm',
            ExcelHelper.CREATE_OVERRIDE_YES,
            '../%s' % ExcelHelper.PATH_TEMPLATE_GENERAL)
        sheet = self._mBook.sheets['Config']

        # root = Key('root')
        # root.bg_color = None
        # root.font_color = StyledValue.COLOR_RED
        # root.font_bold = True
        #
        # sec1 = root.add_child(Key('second1'))
        # sec1.bg_color = StyledValue.COLOR_DEF_BLUE
        # sec2 = root.add_child(Key('second2'))
        # sec2.bg_color = StyledValue.COLOR_DEF_BLUE
        # sec3 = root.add_child(Key('second3'))
        # sec3.bg_color = StyledValue.COLOR_DEF_BLUE
        #
        # k_1_1 = sec1.add_child(Key('1.1'))
        # k_1_1.bg_color = StyledValue.COLOR_DEF_ORANGE
        # k_1_2 = sec1.add_child(Key('1.2'))
        # k_1_2.bg_color = StyledValue.COLOR_DEF_ORANGE
        # k_1_3 = sec1.add_child(Key('1.3'))
        # k_1_3.bg_color = StyledValue.COLOR_DEF_ORANGE
        #
        # k_2_1 = sec2.add_child(Key('2.1'))
        # k_2_1.bg_color = StyledValue.COLOR_DEF_ORANGE
        # k_2_2 = sec2.add_child(Key('2.2'))
        # k_2_2.bg_color = StyledValue.COLOR_DEF_ORANGE
        # k_2_3 = sec2.add_child(Key('2.3'))
        # k_2_3.bg_color = StyledValue.COLOR_DEF_ORANGE
        #
        # k_3_1 = sec3.add_child(Key('3.1'))
        # k_3_1.bg_color = StyledValue.COLOR_DEF_ORANGE
        # k_3_2 = sec3.add_child(Key('3.2'))
        # k_3_2.bg_color = StyledValue.COLOR_DEF_ORANGE
        # k_3_3 = sec3.add_child(Key('3.3'))
        # k_3_3.bg_color = StyledValue.COLOR_DEF_ORANGE
        #
        # k_1_1.add_value(StyledValue('v1_1_1'))
        # k_1_1.add_value(StyledValue('v1_1_2'))
        # k_1_1.add_value(StyledValue('v1_1_3'))
        # k_1_1.add_value(StyledValue('v1_1_4'))
        # k_1_1.add_value(StyledValue('v1_1_5'))
        #
        # k_1_2.add_value(StyledValue('v1_2_1'))
        # k_1_2.add_value(StyledValue('v1_2_2'))
        # k_1_2.add_value(StyledValue('v1_2_3'))
        # k_1_2.add_value(StyledValue('v1_2_4'))
        # k_1_2.add_value(StyledValue('v1_2_5'))
        #
        # k_1_3.add_value(StyledValue('v1_3_1'))
        # k_1_3.add_value(StyledValue('v1_3_2'))
        # k_1_3.add_value(StyledValue('v1_3_3'))
        # k_1_3.add_value(StyledValue('v1_3_4'))
        # k_1_3.add_value(StyledValue('v1_3_5'))
        #
        # k_2_1.add_value(StyledValue('v2_1_1'))
        # k_2_1.add_value(StyledValue('v2_1_2'))
        # k_2_1.add_value(StyledValue('v2_1_3'))
        #
        # k_2_2.add_value(StyledValue('v2_2_1'))
        # k_2_2.add_value(StyledValue('v2_2_2'))
        # k_2_2.add_value(StyledValue('v2_2_3'))
        #
        # k_2_3.add_value(StyledValue('v2_3_1'))
        # k_2_3.add_value(StyledValue('v2_3_2'))
        # k_2_3.add_value(StyledValue('v2_3_3'))
        #
        cfg = ExcelConfig()
        #
        # # save test
        # cfg.save(sheet, 1, 1, root)

        # load test
        root2 = cfg.load(sheet, 1, 1)

        # verify loaded data
        sheet2 = self._mBook.sheets.add('load_test')
        cfg.save(sheet2, 1, 1, root2)

        self._mBook.close()
        self._mBook = None

    def _test_marco(self):
        helper = ExcelHelper()
        self._mBook = helper.create_from_template(
            './excel/test_marco.xlsm',
            ExcelHelper.CREATE_OVERRIDE_YES,
            '../%s' % ExcelHelper.PATH_TEMPLATE_GENERAL)
        sheet = self._mBook.sheets['Config']

        value = StyledValue()

        print value.load(sheet.range(1, 1)).font_color
        print value.load(sheet.range(2, 1)).font_color
        print value.load(sheet.range(3, 1)).font_color

        print value.load(sheet.range(1, 1)).bg_color
        print value.load(sheet.range(2, 1)).bg_color
        print value.load(sheet.range(3, 1)).bg_color

        value.load(sheet.range(2, 1))
        value.font_color = StyledValue.COLOR_RED
        value.save(sheet.range(2, 1))

        value.load(sheet.range(3, 1))
        value.font_color = StyledValue.COLOR_BLUE
        value.save(sheet.range(3, 1))

        value.load(sheet.range(3, 2))
        value.bg_color = StyledValue.COLOR_RED
        value.save(sheet.range(3, 2))

        value.load(sheet.range(3, 3))
        value.bg_color = StyledValue.COLOR_BLUE
        value.save(sheet.range(3, 3))

        print value.load(sheet.range(3, 2)).font_bold
        value.font_bold = True
        value.save(sheet.range(3, 2))

        print value.load(sheet.range(3, 3)).font_italic
        value.font_italic = True
        value.save(sheet.range(3, 3))

        print value.load(sheet.range(3, 4)).font_size
        value.font_size = 20
        value.save(sheet.range(3, 4))

        self._mBook.close()
        self._mBook = None








