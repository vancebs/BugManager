#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Value(object):
    def __init__(self, value=None):
        self._mValue = Value._remove_empty_value(value)
        self._mExtra = dict()

    @property
    def value(self):
        return self._mValue

    @value.setter
    def value(self, val):
        self._mValue = Value._remove_empty_value(val)

    @property
    def extras(self):
        return self._mExtra

    def get_extra(self, key, default=None):
        return self._mExtra.get(key, default)

    def put_extra(self, key, value):
        self._mExtra[key] = value

    def load(self, cell):
        self.value = cell.value
        return self

    def save(self, cell):
        # set value
        value = self.value
        if value != cell.value:
            cell.value = value

    @staticmethod
    def _remove_empty_value(value):
        if value is None:
            return None

        value = str(value).strip()
        if value == '':
            return None

        return value
