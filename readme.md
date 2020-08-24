<center><h2>Maya Workflow Tools</h2></center>

A small set of workflow tools for maya

Tested on:
Maya 2017/2018/2019

#### Install

Download and add the folder to your PYTHONPATH environment variable or copy into your maya/scripts folder.

PYTHONPATH += 'D:\install_directory\Workflow'

### 3DSMAX STYLE RENAMER
A renamer/replace based on the 3dsmax renamer.

This tool support maya undo feature. (Ctrl + Z)
There are some limitations from the maya naming system, you cannot have a number prefix, or duplicated names in the same hierarchy.
You can rename maya non-DAG Objects, like shading nodes, etc, from outliner.
The numbering feature works reading the selection order, if you want identical results on numbering, just select items in the same order. (Ej. select Top item, shift click bottom)

<center>![renamer screenshot](https://github.com/MaxRocamora/MayaWorkflow/blob/master/workflow/img/renamer.png?raw=true>)</center>

Create a shelf button with this python command:

```python

import workflow.renamer.main as wf_renamer
wf_renamer.load()

```

### REFERENCE MINIPANEL
Manage reference nodes from scene selection.

#### SAVE INCREMENTAL
A simple script to save incremental your current file even if it is not modified.
