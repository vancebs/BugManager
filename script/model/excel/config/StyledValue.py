#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlwings as xw
from script.model.excel.config.Value import Value


class StyledValue(Value):
    _EXTRA_STYLE_FONT_BOLD = 'extra-style-font-bold'
    _EXTRA_STYLE_FONT_COLOR = 'extra-style-font-color'
    _EXTRA_STYLE_FONT_ITALIC = 'extra-style-font-italic'
    _EXTRA_STYLE_FONT_SIZE = 'extra-style-font-size'
    _EXTRA_STYLE_BG_COLOR = 'extra-style-bg-color'

    COLOR_BG_NONE = 0xFFFFFF
    COLOR_BLACK = 0x000000
    COLOR_WHITE = 0xFFFFFF
    COLOR_RED = 0x0000FF
    COLOR_GREEN = 0x00FF00
    COLOR_BLUE = 0xFF0000
    COLOR_DEF_BLUE = (91, 155, 213)
    COLOR_DEF_ORANGE = (255, 192, 0)

    @property
    def bg_color(self):
        return self.get_extra(StyledValue._EXTRA_STYLE_BG_COLOR)

    @bg_color.setter
    def bg_color(self, color):
        self.put_extra(StyledValue._EXTRA_STYLE_BG_COLOR, color)

    @property
    def font_color(self):
        return self.get_extra(StyledValue._EXTRA_STYLE_FONT_COLOR)

    @font_color.setter
    def font_color(self, color):
        self.put_extra(StyledValue._EXTRA_STYLE_FONT_COLOR, color)

    @property
    def font_bold(self):
        return self.get_extra(StyledValue._EXTRA_STYLE_FONT_BOLD)

    @font_bold.setter
    def font_bold(self, bold):
        self.put_extra(StyledValue._EXTRA_STYLE_FONT_BOLD, bold)

    @property
    def font_italic(self):
        return self.get_extra(StyledValue._EXTRA_STYLE_FONT_ITALIC)

    @font_italic.setter
    def font_italic(self, italic):
        self.put_extra(StyledValue._EXTRA_STYLE_FONT_ITALIC, italic)

    @property
    def font_size(self):
        return self.get_extra(StyledValue._EXTRA_STYLE_FONT_SIZE)

    @font_size.setter
    def font_size(self, size):
        self.put_extra(StyledValue._EXTRA_STYLE_FONT_SIZE, size)

    def load(self, cell):
        super(StyledValue, self).load(cell)

        self.value = cell.value
        self.bg_color = cell.color
        self.font_color = StyledValue._marco_get_font_color(cell)
        self.font_bold = StyledValue._marco_get_font_bold(cell)
        self.font_italic = StyledValue._marco_get_font_italic(cell)
        self.font_size = StyledValue._marco_get_font_size(cell)
        return self

    def save(self, cell):
        # set value
        value = self.value
        if value != cell.value:
            cell.value = value

        # set bg color
        bg_color = cell.color
        if bg_color != self.bg_color:
            cell.color = self.bg_color

        # set font color
        font_color = StyledValue._marco_get_font_color(cell)
        if font_color is not None and font_color != self.font_color:
            StyledValue._marco_set_font_color(cell, self.font_color)

        # set font bold
        font_bold = StyledValue._marco_get_font_bold(cell)
        if font_bold is not None and font_bold != self.font_bold:
            StyledValue._marco_set_font_bold(cell, self.font_bold)

        # set font italic
        font_italic = StyledValue._marco_get_font_italic(cell)
        if font_italic is not None and font_italic != self.font_italic:
            StyledValue._marco_set_font_italic(cell, self.font_italic)

        # set font size
        font_size = StyledValue._marco_get_font_size(cell)
        if font_size is not None and font_size != self.font_size:
            StyledValue._marco_set_font_size(cell, self.font_size)

        return self

    @staticmethod
    def to_excel_color(color):
        if type(color) == int or type(color) == float:
            color = int(color)
            r = (color & 0x00FF0000) >> 16
            g = (color & 0x0000FF00)
            b = (color & 0x000000FF) << 16
        elif (type(color) == tuple or type(color) == list) and len(color) == 3:
            r = color[2]
            g = color[1]
            b = color[0]
        else:
            raise TypeError('Invalid type of parameter [color]')

        return float(r | g | b)

    @staticmethod
    def _marco_get_font_color(ranges):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        f_get_color = ranges.sheet.book.macro('python_extend.get_Range_Font_color')
        return f_get_color(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column)

    @staticmethod
    def _marco_set_font_color(ranges, color):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        if color is None:
            return

        f_set_color = ranges.sheet.book.macro('python_extend.set_Range_Font_color')
        f_set_color(
            ranges.sheet.name,
            ranges.row, ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column,
            color)

    @staticmethod
    def _marco_get_font_bold(ranges):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        f_get_bold = ranges.sheet.book.macro('python_extend.get_Range_Font_bold')
        return f_get_bold(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column)

    @staticmethod
    def _marco_set_font_bold(ranges, bold):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        if bold is None:
            return

        f_set_bold = ranges.sheet.book.macro('python_extend.set_Range_Font_bold')
        return f_set_bold(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column,
            bold)

    @staticmethod
    def _marco_get_font_italic(ranges):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        f_get_italic = ranges.sheet.book.macro('python_extend.get_Range_Font_italic')
        return f_get_italic(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column)

    @staticmethod
    def _marco_set_font_italic(ranges, italic):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        if italic is None:
            return

        f_set_italic = ranges.sheet.book.macro('python_extend.set_Range_Font_italic')
        return f_set_italic(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column,
            italic)

    @staticmethod
    def _marco_get_font_size(ranges):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        f_get_size = ranges.sheet.book.macro('python_extend.get_Range_Font_size')
        return f_get_size(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column)

    @staticmethod
    def _marco_set_font_size(ranges, size):
        if not isinstance(ranges, xw.Range):
            raise TypeError('Invalid type of parameter [ranges]')

        if size is None:
            return

        f_set_size = ranges.sheet.book.macro('python_extend.set_Range_Font_size')
        return f_set_size(
            ranges.sheet.name,
            ranges.row,
            ranges.column,
            ranges.last_cell.row,
            ranges.last_cell.column,
            size)

