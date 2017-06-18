#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StyledValue import StyledValue
from Value import Value


class Key(StyledValue):
    def __init__(self, name=None):
        StyledValue.__init__(self, name)
        self._mChildren = list()
        self._mValues = list()
        self._mParent = None

    @property
    def name(self):
        return self.value

    @name.setter
    def name(self, value):
        self.value = value

    @property
    def children(self):
        return self._mChildren

    @property
    def parent(self):
        return self._mParent

    @parent.setter
    def parent(self, value):
        self._mParent = value

    @property
    def values(self):
        return self._mValues

    def index_in_parent(self):
        if self.parent is None:
            return -1

        brothers = self.parent.children
        for i in range(len(brothers)):
            if brothers[i] == self:
                return i

        return -1

    def next_brother(self):
        i = self.index_in_parent()
        brothers = self.parent.children
        if 0 <= i < len(brothers) - 1:
            return brothers[i + 1]

        return None

    def prev_brother(self):
        i = self.index_in_parent()
        brothers = self.parent.children
        if 0 < i < len(brothers):
            return brothers[i - 1]

        return None


    def set_parent(self, parent):
        if not isinstance(parent, Key):
            raise TypeError('Invalid type of parameter [key]')

        # add self as child of parent
        parent.add_child(self)

    def add_child(self, child):
        if type(child) != Key:
            raise TypeError('Invalid type of parameter [child]')

        if child.name is None:
            raise ValueError('Invalid child key, the name of the key should not be None')

        self.children.append(child)
        child.parent = self

        return child

    def add_value(self, value):
        if type(value) != StyledValue and type(value) != Value:
            raise TypeError('Invalid type of parameter [value]')

        if value.value is None:
            raise ValueError('Invalid child key, the name of the key should not be None')

        self.values.append(value)

        return value









