#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xlwt import Borders, Font, Alignment, Pattern, XFStyle


def get_sheet_title_style(bg_color=0x39, font_color=0x0, font_size=400,
                          has_pattern=True, horz_center=True):
    fnt = Font()
    fnt.name = 'Arial'
    fnt.colour_index = font_color
    fnt.bold = True
    fnt.height = font_size

    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    al = Alignment()
    if horz_center:
        al.horz = Alignment.HORZ_CENTER
    else:
        al.horz = Alignment.HORZ_LEFT
    al.vert = Alignment.VERT_CENTER

    pattern = None
    if has_pattern:
        pattern = Pattern()
        pattern.pattern = 1
        pattern.pattern_fore_colour = bg_color
        pattern.pattern_back_colour = bg_color

    style = XFStyle()
    style.font = fnt
    style.borders = borders
    style.alignment = al
    if pattern:
        style.pattern = pattern
    return style


def get_body_title_style(bg_color=0x34, font_color=0x0, font_size=200,
                         has_pattern=True, horz_center=True):
    return get_sheet_title_style(bg_color, font_color, font_size,
                                 has_pattern, horz_center)


def get_body_info_style(color=0x0, is_horz_center=True, font_size=200):
    return get_body_title_style(font_color=color, has_pattern=False,
                                horz_center=is_horz_center)


def get_desc_style(color=0x0, horz_center=False):
    return get_body_info_style(color, horz_center)
