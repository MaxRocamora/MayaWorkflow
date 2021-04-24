# -*- coding: utf-8 -*-

# CSS Button Stylesheet
base_css = """
            QPushButton {
                color: {text_color};
                background-color: rgb(45, 45, 45);
                border: 1px solid rgb(75, 75, 75);
                border-radius: 1;
                }
            QPushButton:hover:pressed {
                background-color: rgb(20, 20, 20);
                border-radius: 1;
                border: 1px solid {text_color};
                }
            QPushButton:hover {
                background-color: rgb(60, 60, 60);
                border: 1px solid rgb(235, 245, 251);
               }
            """

css_select = base_css.replace('{text_color}', 'rgb(85, 170, 255)')
css_reload = base_css.replace('{text_color}', 'rgb(255, 170, 0)')
css_load = base_css.replace('{text_color}', 'rgb(170, 255, 0)')
css_unload = base_css.replace('{text_color}', 'rgb(255, 85, 127)')
css_duplicate = base_css.replace('{text_color}', 'rgb(170, 85, 255)')
css_remove = base_css.replace('{text_color}', 'rgb(205, 0, 0)')
css_replace = base_css.replace('{text_color}', 'rgb(230, 230, 0)')
css_namespace = base_css.replace('{text_color}', 'rgb(160, 160, 160)')

__all__ = ['css_select', 'css_reload', 'css_load', 'css_unload',
           'css_duplicate', 'css_remove', 'css_replace', 'css_namespace', ]
