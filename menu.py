import nuke
import nukescripts
import sys
sys.path.append("/home/network/kfrantz/pythonProject/nuke_things")

import check_bbox

menu_bar = nuke.menu("Nuke")
custom_menu = menu_bar.addMenu("My Tools")
custom_menu.addCommand("Check Bbox Sizes", check_bbox.launch_window())

nuke.knobDefault('Shuffle2.label','[value in1]')
nuke.menu('Nodes').addCommand('Other/Backdrop', lambda:nukescripts.autoBackdrop(), 'ctrl+b')
nuke.menu("Nuke").findItem("Edit").addCommand("Add Premult", "nuke.createNode('Premult')", "ctrl+p")
nuke.menu("Nuke").findItem("Edit").addCommand("Add Unpremult", "nuke.createNode('Unpremult')", "ctrl+u")