
import maya.cmds as cmds
# copiar el metodo aca
import maya_scr.utils.mayaNodeSelector as mayaNodeSelector


class mayaMeshCore(object):

    def __init__(self):
        self.mns = mayaNodeSelector.mayaNodeSelector(self)

    def deleteHistory(self):
        ''' deletes history '''
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
        allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
        if allSel is None:
            return "Select Meshes first."

        for each in allSel:
            cmds.delete(each, all=True, ch=True)

        return "History deleted on ({}) transform nodes".format(len(allSel))

    def freezeTransformations(self):
        ''' freezes transformations of selection  '''
        rawSel = cmds.ls(sl=True)  # raw selection
        if cmds.nodeType(rawSel) == "mesh":
            # get transforms names of the shapes
            allSel = cmds.listRelatives(rawSel, parent=True, fullPath=False)
        else:
            allSel = rawSel
        if allSel is None:
            return "Select Meshes first."

        for each in allSel:
            cmds.FreezeTransformations(each)
        return "Transformations freezed on ({}) transform nodes".format(len(allSel))

    def centerPivot(self):
        ''' reset pivot of transforms meshes '''
        allSel = cmds.ls(sl=True)
        if allSel is None:
            return "Select Meshes to center pivot first."
        for each in allSel:
            if cmds.nodeType(each) == "transform":
                cmds.CenterPivot(each)
        return "Pivot Centered on ({}) transform nodes".format(len(allSel))

    def cleanCombine(self):
        ''' Combines selection and deletes history '''
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
        # get transforms names of the shapes
        allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
        if allSel is None:
            return "Select Meshes first."
        try:
            cmds.polyUnite(rawSel, ch=False)  # combines and deletehistory
        except RuntimeError as e:
            return str(e)
        return "Shapes combined with no history: ({})".format(len(allSel))

    def cleanSeparate(self):
        ''' Separates selection and deletes history '''
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
        # get transforms names of the shapes
        allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
        if allSel is None:
            return "Select Meshes first."
        try:
            cmds.polySeparate(rawSel, ch=False)  # combines and deletehistory
            return "Shapes separated with no history: ({})".format(len(allSel))
        except Exception as e:
            return str(e)

    def cleanDuplicate(self):
        ''' Duplicate and delete current selected meshes '''
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
        # get transforms names of the shapes
        allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
        if allSel is None:
            return "Nothing Selected"

        for each in allSel:
            cmds.duplicate(each, renameChildren=True)

        cmds.delete(allSel)
        return "Shapes duplicated: ({})".format(len(allSel))

    def copyPivot(self):
        ''' Copy the pivot from source mesh to others objects. '''
        if len(cmds.ls(sl=True)) < 2:
            return "Select 2 or more objects."
        sourceObj = cmds.ls(sl=True)[len(cmds.ls(sl=True)) - 1]
        targetObj = cmds.ls(sl=True)[0:(len(cmds.ls(sl=True)) - 1)]
        parentList = []
        for obj in targetObj:
            if cmds.listRelatives(obj, parent=True):
                parentList.append(cmds.listRelatives(obj, parent=True)[0])
            else:
                parentList.append('')
        pivotTranslate = cmds.xform(sourceObj, q=True, ws=True, rotatePivot=True)
        cmds.parent(targetObj, sourceObj)
        cmds.makeIdentity(targetObj, a=True, t=True, r=True, s=True)
        cmds.xform(targetObj, ws=True, pivots=pivotTranslate)
        for ind in range(len(targetObj)):
            if parentList[ind] != '':
                cmds.parent(targetObj[ind], parentList[ind])
            else:
                cmds.parent(targetObj[ind], world=True)

        return "Pivot Copied"

    def restoreShapesNames(self, selection=False, uibar=False):
        '''
        Reset shapes names for transforms
        Args:
            selection (boolean) if true uses current selection instead of maya scene
            uiBar ::: class ::: uibar class for message control ui
        '''

        baseShapeName = False

        if selection:
            listMeshFilter = self.mns.getSelectionMesh(True, False)
        else:
            listMeshFilter = self.mns.getSceneMesh(True, False)

        if listMeshFilter is None:
            return False

        if len(listMeshFilter) > 0:
            failedMesh = 0
            for index, mesh in enumerate(listMeshFilter):
                shapeRelatives = cmds.listRelatives(mesh, pa=True, type="shape")

                if len(shapeRelatives) == 1:
                    baseShapeName = shapeRelatives[0]
                else:
                    # If more than one shape is connected, taking only the shape
                    # who has .inMesh' connection.
                    for shape in shapeRelatives:
                        connections = cmds.listConnections(shape, sh=1, c=1)
                        if connections is None:
                            continue

                        for con in connections:
                            if '.inMesh' in con:
                                baseShapeName = shape

                if not baseShapeName:
                    return False

                validShapeName = str(mesh) + "Shape"
                if baseShapeName == validShapeName:
                    return False

                print 'AutoRenaming {} Mesh to {}'.format(baseShapeName, validShapeName)

                try:
                    newShapeName = str(mesh) + "Shape"
                except UnicodeEncodeError:
                    print 'WARNING: INVALID NAME CHARACTER: ', mesh, baseShapeName
                    continue
                if "|" in newShapeName:
                    cmds.warning("WARNING: Nameclash on: ", newShapeName)
                else:
                    if baseShapeName != newShapeName:
                        failedMesh += 1
                        print "BadShapeName: Replacing ({}) with ({})".format(baseShapeName, newShapeName)
                        cmds.rename(baseShapeName, newShapeName)
            msg = "Shapes Renamed in ( {} ) of ( {} ) Meshes.".format(str(failedMesh), str(index))
            if uibar:
                uibar.ok(msg)
                return True
            else:
                return msg
