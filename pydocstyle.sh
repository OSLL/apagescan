#!/usr/bin/env bash
pip3 install pydocstyle
cd tree_dialog/
pydocstyle --explain pidNode.py
pydocstyle --explain treeDialogFacade.py
pydocstyle --explain treeDialog_view.py
cd ../qt_models/
pydocstyle --explain pagemapModel.py
pydocstyle --explain pidTreeModel.py
cd ../handling/
pydocstyle --explain device_handler.py
pydocstyle --explain listener.py
cd ../
pydocstyle --explain cairo_draw.py
pydocstyle --explain custom_signals.py
pydocstyle --explain dataDialog_view.py
pydocstyle --explain device_interaction.py
pydocstyle --explain dynamicsDialog_view.py
pydocstyle --explain graph_view.py
pydocstyle --explain main.py
pydocstyle --explain main_view.py
pydocstyle --explain pages_graphics.py
pydocstyle --explain picture_view.py
pydocstyle --explain selectDialog_view.py
pydocstyle --explain tableDialog_view.py
pydocstyle --explain utilities.py

