import maya.cmds as cmds
import random as r
import mtoa.utils as mutils


################### Method Definitions ###################
def createShadingNode(nameOfNode, typeName, asShader, asTexture=False):
    cmds.shadingNode(typeName, asShader=asShader, asTexture=asTexture, n=nameOfNode)


def createAiStandardSurface(nameOfMat):
    createShadingNode(nameOfMat, "aiStandardSurface", True)
    # cmds.setAttr(f"{nameOfMat}.specular", 0)
    # cmds.shadingNode('aiStandardSurface', asShader = True, n = nameOfMat)


def assignMaterial(nameOfObject, nameOfMat):
    cmds.select(nameOfObject)
    cmds.hyperShade(assign=nameOfMat)


def createAndAssignAiStandardSurface(nameOfObject, nameOfMat):
    createAiStandardSurface(nameOfMat)
    assignMaterial(nameOfObject, nameOfMat)


def createEye(isLeft, xPosition=0.75):
    rotFactor = 1
    if isLeft:
        xPosition = -xPosition
        rotFactor = -1

    eye, _ = cmds.polyCylinder(sa=5)
    cmds.scale(0.2, 0.05, 0.3, eye)
    cmds.rotate(93.799, 25.875, -44.031 * rotFactor, eye)
    cmds.move(0.4 * xPosition, 4.6, 1.05, eye)
    # cmds.move(.1, .1, 0, f'{eye}.e[13]', r = True)

    cmds.polyBevel3(
        eye,
        fraction=0.1,
        offsetAsFraction=True,
    )
    cmds.displaySmoothness(
        eye,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )


def createHead():
    head, _ = cmds.polyCube()
    cmds.scale(0.5, 0.5, 0.5, f"{head}.f[3]")
    cmds.scale(0.75, 0.75, 0.75, f"{head}.f[2]")
    cmds.scale(0.85, 1, 1, f"{head}.f[1]")
    cmds.move(0, 0.18, 0, f"{head}.f[2]", r=True)
    cmds.move(0, 4.25, -0.2, head)
    cmds.scale(4, 4, 4, head)

    assignMaterial(head, whiteMatName)

    cmds.polyChipOff(
        f"{head}.f[1:6]",
        ch=True,
        kft=1,
        dup=1,
        off=1,
    )
    headBase, hood, _ = cmds.polySeparate(head)

    headBase = cmds.rename(headBase, "head")
    hood = cmds.rename(hood, "hood")

    cmds.scale(1.5, 1.5, 1.5, hood)
    cmds.move(0, -0.25, -0.75, hood, r=True)
    cmds.polyExtrudeEdge(f"{hood}.e[0]", f"{hood}.e[10:11]", ltz=-0.05, offset=1)
    # cmds.move(0, 0, .1, f'{hood}.e[8]', r = True)
    cmds.polyExtrudeEdge(
        f"{hood}.e[8]", f"{hood}.e[17]", f"{hood}.e[15]", ltz=-0.69, offset=0.21
    )
    cmds.scale(0.75, 0.75, 0.75, f"{hood}.e[21]", f"{hood}.e[23]", f"{hood}.e[25]")
    cmds.move(0, -0.25, 0, f"{hood}.e[21]", r=True)
    cmds.scale(0.75, 1, 1, f"{hood}.e[14]")
    cmds.move(0, -0.5, 0, f"{hood}.e[14]", r=True)
    # cmds.scale(1.5, 1, 1, f"{hood}.e[15]", f"{hood}.e[17]")
    cmds.polyExtrudeEdge(
        f"{hood}.e[14]",
        f"{hood}.e[16]",
        f"{hood}.e[18]",
        f"{hood}.e[21:25]",
        ltz=-0.3,
        offset=0.125,
    )
    cmds.move(0, -0.2, -0.2, f"{hood}.e[35]", f"{hood}.e[38]", f"{hood}.e[41]", r=True)
    cmds.move(0, -0.4, 0, f"{hood}.e[28]", r=True)
    cmds.scale(0.5, 1, 1, f"{hood}.e[28]")
    cmds.polyExtrudeFacet(f"{hood}.f[0:18]", ltz=0.05)

    cmds.scale(0.75, 1, 1, f"{headBase}.f[3]")
    cmds.displaySmoothness(
        head,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )
    cmds.xform(head, centerPivots=True)

    assignMaterial(hood, whiteMatName)
    assignMaterial(f"{hood}.f[18:37]", pinkMatName)

    neck, _ = cmds.polyCylinder(n="neck")
    cmds.scale(0.1, 0.3, 0.1, neck)
    cmds.move(0, 4, -0.25)

    assignMaterial(neck, whiteMatName)

    return head, neck


def createBody():
    chest, _ = cmds.polyCylinder(
        subdivisionsHeight=7, subdivisionsCaps=8, subdivisionsAxis=12, n="chest"
    )
    cmds.polyChipOff(
        f"{chest}.f[36:95]",
        f"{chest}.f[36:95]",
        f"{chest}.f[97:104]",
        f"{chest}.f[109:110]",
        f"{chest}.f[115:116]",
        f"{chest}.f[121:122]",
        f"{chest}.f[127:128]",
        f"{chest}.f[133:134]",
        f"{chest}.f[139:140]",
        f"{chest}.f[145:152]",
        f"{chest}.f[156:215]",
        ch=True,
        kft=1,
        dup=1,
        off=1,
    )
    innerChest, outerChest, _ = cmds.polySeparate(chest)

    innerChest = cmds.rename(innerChest, "innerChest")
    outerChest = cmds.rename(outerChest, "outerChest")
    cmds.scale(1.5, 1.1, 1.1, outerChest)
    cmds.polyExtrudeFacet(
        f"{outerChest}.f[136:147]", f"{outerChest}.f[0:11]", ltz=0.015
    )
    cmds.polyExtrudeFacet(
        f"{outerChest}.f[124:135]", f"{outerChest}.f[12:23]", offset=0.075, ltz=0.01
    )
    cmds.polyExtrudeFacet(outerChest, ltz=0.001)
    cmds.scale(0.25, 0.45, 0.45, chest)
    cmds.rotate(0, 0, -90, chest)
    cmds.move(0, 3.5, -0.225, chest)
    cmds.displaySmoothness(
        chest,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )

    assignMaterial(innerChest, whiteMatName)
    assignMaterial(outerChest, blackMatName)

    waist, _ = cmds.polyCylinder(subdivisionsHeight=28, n="waist")
    for i in range(220, 521, 60):
        cmds.scale(0.5, 1, 0.5, f"{waist}.e[{i}:{i + 19}]")
    cmds.scale(0.1, 0.3, 0.1, waist)
    cmds.move(0, 3.25, -0.22, waist)
    cmds.displaySmoothness(
        waist,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )
    assignMaterial(waist, whiteMatName)

    hip, _ = cmds.polyCube(n="hip")
    cmds.scale(1.5, 1.5, 1.5, f"{hip}.f[1]")
    cmds.move(0, 0, -0.4, f"{hip}.f[1]", r=True)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=0.5, offset=0.35)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=0.01)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", offset=0.01)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", offset=0.2)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", offset=0.01)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=0.01)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=0.1)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=0.01)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", offset=0.001)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", offset=0.02)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", offset=0.001)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=-0.01)
    cmds.polyExtrudeFacet(f"{hip}.f[1]", ltz=-1)
    cmds.delete(f"{hip}.f[1]")
    cmds.scale(0.715, 0.44, 0.715, hip)
    cmds.move(0, 2.5, -0.5, hip)
    cmds.rotate(1, 180, 1, hip)
    cmds.displaySmoothness(
        hip, divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3
    )

    assignMaterial(hip, blackMatName)
    cmds.xform(hip, centerPivots=True)

    return chest, waist, hip


def createArm(side, xPosition=0.75):
    rotFactor = 1
    if side == "left":
        xPosition = -xPosition
        rotFactor = -1

    shoulder, _ = cmds.polyCube(subdivisionsWidth=2, n=f"{side}_shoulder")
    cmds.move(0, -0.5, 0, f"{shoulder}.e[18]", r=True)
    cmds.scale(0.75, 0.75, 0.75, f"{shoulder}.f[6:7]")
    cmds.move(xPosition, 3.65, -0.2, shoulder)
    cmds.rotate(0, 0, 90, shoulder)
    cmds.scale(0.4, 0.4, 0.4, shoulder)
    cmds.polyBevel3(
        shoulder,
        fraction=0.5,
        offsetAsFraction=True,
    )
    cmds.displaySmoothness(
        shoulder,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )

    assignMaterial(shoulder, whiteMatName)

    upperArm, _ = cmds.polyCylinder(n=f"{side}_upperArm")
    cmds.move(1.5 * xPosition, 3.65, -0.2, upperArm)
    cmds.rotate(0, 0, rotFactor * 90, upperArm)
    cmds.scale(0.07, 0.164, 0.07, upperArm)
    cmds.parent(upperArm, shoulder)

    assignMaterial(upperArm, whiteMatName)

    elbow, _ = cmds.polySphere(r=0.15, n=f"{side}_elbow")
    cmds.move(1.75 * xPosition, 3.65, -0.2, elbow)

    assignMaterial(elbow, whiteMatName)

    forearm, _ = cmds.polyCube(n=f"{side}_forearm")
    cmds.scale(1, 1, 1.5, f"{forearm}.f[1]")
    cmds.move(2.4 * xPosition, 3.65, -0.2, forearm)
    cmds.rotate(90, -90, rotFactor * 0, forearm)
    cmds.scale(0.205, 0.75, 0.309, forearm)
    cmds.polyBevel3(
        forearm,
        fraction=0.1,
        offsetAsFraction=True,
    )
    cmds.displaySmoothness(
        forearm,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )
    cmds.parent(forearm, elbow)

    assignMaterial(forearm, pinkMatName)

    return shoulder, upperArm, elbow, forearm


def createHand(side, xPosition=0.75):
    rotFactor = 1
    if side == "left":
        xPosition = -xPosition
        rotFactor = -1
    wrist, _ = cmds.polyCylinder()
    cmds.scale(0.054, 0.1, 0.054, wrist)
    cmds.move(2.95 * xPosition, 3.65, -0.2)

    assignMaterial(wrist, whiteMatName)

    hand, _ = cmds.polyCube(n=f"{side}_hand")
    cmds.scale(0.2, 0.449, 0.449, hand)
    cmds.rotate(0, -90, 90 * rotFactor, hand)
    cmds.move(3.2 * xPosition, 3.65, -0.2, hand)
    cmds.scale(0.8, 0.8, 0.8, f"{hand}.f[1]")
    cmds.polyBevel3(
        hand,
        fraction=0.1,
        offsetAsFraction=True,
    )
    cmds.displaySmoothness(
        hand,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )
    cmds.parent(hand, wrist)

    assignMaterial(hand, whiteMatName)
    return wrist, hand


def createLeg(side, xPosition=0.75):
    if side == "left":
        xPosition = -xPosition
    hipJoint, _ = cmds.polySphere(r=0.2, n="hipJoint")
    cmds.move(0.75 * xPosition, 2.75, -0.3, hipJoint)

    assignMaterial(hipJoint, whiteMatName)

    thigh, _ = cmds.polyCylinder(h=1, r=0.75, n=f"{side}_thigh")
    cmds.scale(0.167, 0.226, 0.167)
    cmds.move(0.75 * xPosition, 2.5, -0.3, thigh)
    cmds.polyExtrudeFacet(f"{thigh}.f[20]", offset=0.1)
    cmds.polyExtrudeFacet(f"{thigh}.f[20]", ltz=0.1)
    cmds.parent(thigh, hipJoint)

    assignMaterial(thigh, blackMatName)

    knee, _ = cmds.polySphere(
        r=1, subdivisionsAxis=8, subdivisionsHeight=8, n=f"{side}_knee"
    )
    cmds.delete(f"{knee}.f[0:23]", f"{knee}.f[48:55]")
    cmds.polyCloseBorder(f"{knee}.e[0:7]")
    cmds.polyExtrudeFacet(f"{knee}.f[32]", ltz=0.01)
    cmds.polyExtrudeFacet(f"{knee}.f[32]", ltz=0.025, offset=0.1)
    cmds.scale(0.192, 0.138, 0.192, knee)
    cmds.rotate(90, 0, 0, knee)
    cmds.move(0.75 * xPosition, 2.25, -0.12, knee)

    cmds.polyExtrudeFacet(f"{knee}.f[16:23]", offset=0.025)
    cmds.polyExtrudeFacet(f"{knee}.f[16:23]", ltz=-0.025)
    cmds.polyExtrudeFacet(f"{knee}.f[24:31]", ltz=-0.015, offset=0.015)
    cmds.polyExtrudeFacet(f"{knee}.f[8:15]", ltz=-0.015, offset=0.015)

    cmds.polyExtrudeFacet(f"{knee}.f[32]", offset=0.075)
    cmds.polyExtrudeFacet(f"{knee}.f[32]", ltz=0.2)

    cmds.polyExtrudeFacet(f"{knee}.f[116:117]", ltz=0.75)
    cmds.scale(0.25, 1, 1, f"{knee}.f[116:117]")

    assignMaterial(knee, whiteMatName)

    assignMaterial(f"{knee}.f[8:15]", pinkMatName)
    assignMaterial(f"{knee}.f[65:88]", pinkMatName)
    assignMaterial(f"{knee}.f[16:23]", pinkMatName)

    lowerLeg, _ = cmds.polyCylinder(
        r=0.75, h=2, subdivisionsAxis=6, subdivisionsHeight=1, n=f"{side}_lowerLeg"
    )
    cmds.scale(0.5, 0.5, 0.5, f"{lowerLeg}.f[7]")
    cmds.move(-xPosition / 4, 0, -0.25, f"{lowerLeg}.f[7]", r=True)
    cmds.polyExtrudeFacet(f"{lowerLeg}.f[6:7]", ltz=0.01)
    cmds.scale(0.85, 0.75, 1, lowerLeg)

    cmds.move(0, 0.5, 0, f"{lowerLeg}.f[17]", r=True)
    cmds.polyExtrudeFacet(f"{lowerLeg}.f[7]", offset=0.1)
    cmds.polyExtrudeFacet(f"{lowerLeg}.f[7]", offset=0.01)
    cmds.polyExtrudeFacet(f"{lowerLeg}.f[7]", ltz=-0.005)
    cmds.polyExtrudeFacet(f"{lowerLeg}.f[7]", ltz=-0.5, offset=0.1)

    cmds.displaySmoothness(
        lowerLeg,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )

    cmds.move(xPosition, 1.25, 0, lowerLeg)
    cmds.parent(lowerLeg, knee)

    assignMaterial(lowerLeg, blackMatName)

    return hipJoint, thigh, knee, lowerLeg


def createFoot(side, xPosition=0.75):
    if side == "left":
        xPosition = -xPosition
    ankle, _ = cmds.polyCylinder(r=0.05, h=1, n=f"{side}_ankle")
    cmds.rotate(0, 0, 90, ankle)
    cmds.move(xPosition, 0.5, -0.1, ankle)

    assignMaterial(ankle, pinkMatName)

    origFoot, _ = cmds.polyCylinder(
        r=0.75, h=0.5, subdivisionsAxis=6, subdivisionsHeight=2, n=f"{side}_foot"
    )
    cmds.scale(0.75, 0.75, 0.75, f"{origFoot}.f[13]")
    cmds.move(0, 0, -0.15, f"{origFoot}.f[13]", r=True)
    cmds.polySplitRing(f"{origFoot}.e[18:23]")
    cmds.move(xPosition, 0.25, 0, origFoot)

    cmds.polyExtrudeFacet(f"{origFoot}.f[0:5]", ltz=0.05, offset=0.02)
    cmds.move(0, 0, 0.04, f"{origFoot}.f[0:5]", r=True)
    cmds.polyExtrudeFacet(f"{origFoot}.f[13]", ltz=0.01)
    for i in [3, 16, 35]:
        cmds.move(0, 0, 0.2 + 0.0025 * i, f"{origFoot}.f[{i}]", r=True)

    assignMaterial(origFoot, blueMatName)
    assignMaterial(f"{origFoot}.f[0:5]", pinkMatName)
    for i in [21, 32, 2]:
        assignMaterial(f"{origFoot}.f[{i}]", pinkMatName)

    cmds.polySplitRing(
        f"{origFoot}.e[2]",
        f"{origFoot}.e[4]",
        f"{origFoot}.e[8]",
        f"{origFoot}.e[10]",
        f"{origFoot}.e[14]",
        f"{origFoot}.e[16]",
        f"{origFoot}.e[28]",
        f"{origFoot}.e[32]",
        f"{origFoot}.e[50]",
        f"{origFoot}.e[53]",
        f"{origFoot}.e[60]",
        f"{origFoot}.e[63]",
        f"{origFoot}.e[72]",
        f"{origFoot}.e[76]",
    )
    cmds.move(0, 0, 0.15, f"{origFoot}.e[90]", r=True)
    cmds.move(0, 0, 0.15, f"{origFoot}.e[94]", r=True)
    cmds.polySplitRing(
        f"{origFoot}.e[0]",
        f"{origFoot}.e[3]",
        f"{origFoot}.e[6]",
        f"{origFoot}.e[9]",
        f"{origFoot}.e[12]",
        f"{origFoot}.e[15]",
        f"{origFoot}.e[30]",
        f"{origFoot}.e[35]",
        f"{origFoot}.e[38]",
        f"{origFoot}.e[42]",
        f"{origFoot}.e[55]",
        f"{origFoot}.e[58]",
        f"{origFoot}.e[68]",
        f"{origFoot}.e[74]",
        f"{origFoot}.e[92]",
        f"{origFoot}.e[105]",
    )
    cmds.polyChipOff(
        f"{origFoot}.f[3]",
        f"{origFoot}.f[9]",
        f"{origFoot}.f[16]",
        f"{origFoot}.f[26:27]",
        f"{origFoot}.f[35]",
        f"{origFoot}.f[38:51]",
        f"{origFoot}.f[59:66]",
        f"{origFoot}.f[66]",
        ch=True,
        kft=1,
        dup=0,
        off=0,
    )
    foot, toe, _ = cmds.polySeparate(origFoot)
    cmds.ungroup(origFoot)

    foot = cmds.rename(foot, f"{side}_foot")
    toe = cmds.rename(toe, f"{side}_toe")

    cmds.displaySmoothness(
        foot,
        toe,
        divisionsU=3,
        divisionsV=3,
        pointsWire=16,
        pointsShaded=4,
        polygonObject=3,
    )
    cmds.xform(foot, centerPivots=True)
    cmds.xform(toe, centerPivots=True)
    return ankle, foot, toe


#################### End Method Definitions ###################
cmds.file(force=True, newFile=True)
# cmds.select(all= True)
# cmds.delete()

################# create materials ###########################
whiteMatName = "whiteMat"
createAiStandardSurface(whiteMatName)
cmds.setAttr(f"{whiteMatName}.baseColor", 1, 1, 1)
cmds.setAttr(f"{whiteMatName}.emission", 0.5)

pinkMatName = "pinkMat"
createAiStandardSurface(pinkMatName)
cmds.setAttr(f"{pinkMatName}.baseColor", 1, 0.279, 1)

blueMatName = "blueMat"
createAiStandardSurface(blueMatName)
cmds.setAttr(f"{blueMatName}.baseColor", 0.588, 1, 1)

blackMatName = "blackMat"
createAiStandardSurface(blackMatName)
cmds.setAttr(f"{blackMatName}.baseColor", 0.033, 0.033, 0.1)
cmds.setAttr(f"{blackMatName}.metalness", 0.6)
################################################################

# create red and blue skydome
skydome = mutils.createLocator("aiSkyDomeLight", asLight=True)
cmds.setAttr("aiSkyDomeLight1.aiExposure", -5)
cmds.setAttr("aiSkyDomeLight1.aiSamples", 3)
rampName = cmds.shadingNode("ramp", asTexture=True)
cmds.setAttr("ramp1.colorEntryList[0].position", 0.5)
cmds.setAttr("ramp1.colorEntryList[0].color", 0, 0, 1)
cmds.setAttr("ramp1.colorEntryList[1].position", 0.6)
cmds.setAttr("ramp1.colorEntryList[1].color", 1, 0, 0)
cmds.connectAttr(f"{rampName}.outColor", "aiSkyDomeLight1.color", force=True)

# create ground
# cmds.polyPlane(height=20, width=20)

head, neck = createHead()
# createEye(isLeft = True)
# createEye(isLeft = False)
chest, waist, hip = createBody()
leftWrist, leftHand = createHand("left")
rightWrist, rightHand = createHand("right")
leftShoulder, leftUpperArm, leftElbow, leftForearm = createArm("left")
rightShoulder, rightUpperArm, rightElbow, rightForearm = createArm("right")
leftHipJoint, leftThigh, leftKnee, leftLowerLeg = createLeg("left")
rightHipJoint, rightThigh, rightKnee, rightLowerLeg = createLeg("right")
leftAnkle, leftFoot, leftToe = createFoot("left")
rightAnkle, rightFoot, rightToe = createFoot("right")

leftLegJointList = [leftHipJoint, leftKnee, leftAnkle, leftFoot, leftToe]
rightLegJointList = [rightHipJoint, rightKnee, rightAnkle, rightFoot, rightToe]

leftArmJointList = [leftShoulder, leftElbow, leftWrist, leftHand]
rightArmJointList = [rightShoulder, rightElbow, rightWrist, rightHand]

legList = []
footList = []


def rig(root):
    controlList = []

    # hip
    v = cmds.xform(
        f"{root}", q=True, ws=True, rp=True
    )  # returns worldspace coordinates of root
    mainJoint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{root}_joint")
    cmds.parentConstraint(mainJoint, root, mo=True)

    rootControl, _ = cmds.circle(nr=(0, 1, 0), r=2, n="root_control")
    cmds.move(v[0], v[1], v[2])
    cmds.parentConstraint(rootControl, mainJoint)

    # lock attributes
    cmds.setAttr(rootControl + ".sy", k=0, cb=0, l=1)
    cmds.setAttr(rootControl + ".sz", k=0, cb=0, l=1)
    cmds.setAttr(rootControl + ".sx", k=0, cb=0, l=1)
    cmds.setAttr(rootControl + ".v", k=0, cb=0, l=1)

    controlList.append(rootControl)

    # waist
    cmds.select(mainJoint)
    v = cmds.xform(waist, q=True, ws=True, t=True)
    waistJoint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{waist}_joint")
    cmds.parentConstraint(waistJoint, waist, mo=True)

    waistControl, _ = cmds.circle(nr=(0, 1, 0), r=1, n="waist_control")
    cmds.move(v[0], v[1], v[2])
    cmds.move(v[0], v[1] - 0.3, v[2], f"{waistControl}.rotatePivot")
    cmds.parentConstraint(waistControl, waistJoint)
    cmds.parent(waistControl, rootControl)

    # lock attributes
    cmds.setAttr(waistControl + ".ty", k=0, cb=0, l=1)
    cmds.setAttr(waistControl + ".tz", k=0, cb=0, l=1)
    cmds.setAttr(waistControl + ".tx", k=0, cb=0, l=1)
    cmds.setAttr(waistControl + ".sy", k=0, cb=0, l=1)
    cmds.setAttr(waistControl + ".sz", k=0, cb=0, l=1)
    cmds.setAttr(waistControl + ".sx", k=0, cb=0, l=1)
    cmds.setAttr(waistControl + ".v", k=0, cb=0, l=1)

    # chest
    cmds.select(waistJoint)
    v = cmds.xform(chest, q=True, ws=True, t=True)
    chestJoint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{chest}_joint")
    cmds.parentConstraint(chestJoint, chest, mo=True)

    chestControl, _ = cmds.circle(nr=(0, 1, 0), r=1.5, n="chest_control")
    cmds.move(v[0], v[1], v[2])
    cmds.parentConstraint(chestControl, chestJoint)
    cmds.parent(chestControl, waistControl)

    # lock attributes
    cmds.setAttr(chestControl + ".ty", k=0, cb=0, l=1)
    cmds.setAttr(chestControl + ".tz", k=0, cb=0, l=1)
    cmds.setAttr(chestControl + ".tx", k=0, cb=0, l=1)
    cmds.setAttr(chestControl + ".sy", k=0, cb=0, l=1)
    cmds.setAttr(chestControl + ".sz", k=0, cb=0, l=1)
    cmds.setAttr(chestControl + ".sx", k=0, cb=0, l=1)
    cmds.setAttr(chestControl + ".v", k=0, cb=0, l=1)

    # neck
    cmds.select(chestJoint)
    v = cmds.xform(neck, q=True, ws=True, t=True)
    neckJoint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{neck}_joint")
    cmds.parentConstraint(neckJoint, neck, mo=True)

    neckControl, _ = cmds.circle(nr=(0, 1, 0), r=1.5, n="neck_control")
    cmds.move(v[0], v[1], v[2], neckControl)
    cmds.move(v[0], v[1] - 0.3, v[2], f"{neckControl}.rotatePivot")
    cmds.parentConstraint(neckControl, neckJoint, mo=True)
    cmds.parent(neckControl, chestControl)

    # lock attributes
    cmds.setAttr(neckControl + ".ty", k=0, cb=0, l=1)
    cmds.setAttr(neckControl + ".tz", k=0, cb=0, l=1)
    cmds.setAttr(neckControl + ".tx", k=0, cb=0, l=1)
    cmds.setAttr(neckControl + ".sy", k=0, cb=0, l=1)
    cmds.setAttr(neckControl + ".sz", k=0, cb=0, l=1)
    cmds.setAttr(neckControl + ".sx", k=0, cb=0, l=1)
    cmds.setAttr(neckControl + ".v", k=0, cb=0, l=1)

    # head
    v = cmds.xform(head, q=True, ws=True, rp=True)
    headJoint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{head}_joint")
    cmds.parentConstraint(headJoint, head, mo=True)

    def legRig(side):
        cmds.select(mainJoint)
        if side == "left":
            legJointList = leftLegJointList
        else:
            legJointList = rightLegJointList
        for i in legJointList:
            v = cmds.xform(i, q=True, ws=True, t=True)
            if i in [leftFoot, rightFoot]:
                v = cmds.xform(f"{i}.vtx[50]", q=True, ws=True, t=True)
            if i in [leftToe, rightToe]:
                v = cmds.xform(f"{i}.vtx[18]", q=True, ws=True, t=True)

            joint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{i}_joint")

            # constrain Geo to Joints
            cmds.parentConstraint(joint, i, mo=True)

        ikHandleName = f"{side}_leg_ik"
        cmds.ikHandle(
            sj=f"{legJointList[0]}_joint", ee=f"{legJointList[2]}_joint", n=ikHandleName
        )

        # knee control
        kneeControl, _ = cmds.circle(r=0.25, n=f"{side}_knee_control")
        v = cmds.xform(f"{legJointList[1]}_joint", q=True, ws=True, t=True)
        cmds.move(v[0], v[1], v[2] + 1, kneeControl)
        cmds.poleVectorConstraint(kneeControl, ikHandleName)
        controlList.append(kneeControl)

        # lock attributes
        cmds.setAttr(kneeControl + ".ty", k=0, cb=0, l=1)
        # cmds.setAttr(kneeControl + ".tx", k = 0, cb = 0, l = 1)
        cmds.setAttr(kneeControl + ".sy", k=0, cb=0, l=1)
        cmds.setAttr(kneeControl + ".sz", k=0, cb=0, l=1)
        cmds.setAttr(kneeControl + ".sx", k=0, cb=0, l=1)
        cmds.setAttr(kneeControl + ".ry", k=0, cb=0, l=1)
        cmds.setAttr(kneeControl + ".rz", k=0, cb=0, l=1)
        cmds.setAttr(kneeControl + ".rx", k=0, cb=0, l=1)
        cmds.setAttr(kneeControl + ".v", k=0, cb=0, l=1)

        # foot control
        footControl, _ = cmds.circle(nr=(0, 1, 0), r=1.25, n=f"{side}_foot_control")
        v = cmds.xform(f"{legJointList[3]}_joint", q=True, ws=True, t=True)
        cmds.move(v[0], v[1], v[2], footControl)

        v = cmds.xform(f"{legJointList[2]}_joint", q=True, ws=True, t=True)
        # cmds.move(v[0], v[1], v[2], f'{footControl}.rotatePivot')

        cmds.orientConstraint(footControl, f"{legJointList[2]}_joint", mo=True)
        cmds.pointConstraint(footControl, ikHandleName, mo=True)
        controlList.append(footControl)
        # for i in legJointList:
        #     v = cmds.xform(i, q = True, ws = True, t = True)
        #     control = cmds.circle(nr = (0, 1, 0), r = .75)
        #     cmds.move(v[0], v[1], v[2], control)
        #     cmds.orientConstraint(control, joint, mo = True)
        #     cmds.parent(control, 'Master_Control')

        # lock attributes
        cmds.setAttr(footControl + ".sy", k=0, cb=0, l=1)
        cmds.setAttr(footControl + ".sz", k=0, cb=0, l=1)
        cmds.setAttr(footControl + ".sx", k=0, cb=0, l=1)
        cmds.setAttr(footControl + ".v", k=0, cb=0, l=1)

        cmds.hide(ikHandleName)

    def armRig(side):
        cmds.select(chestJoint)
        if side == "left":
            armJointList = leftArmJointList
        else:
            armJointList = rightArmJointList
        for geo in armJointList:
            v = cmds.xform(geo, q=True, ws=True, t=True)
            joint = cmds.joint(p=(v[0], v[1], v[2]), rad=0.4, n=f"{geo}_joint")
            cmds.parentConstraint(joint, geo, mo=True)

        # shoulder control
        shoulderControl, _ = cmds.circle(
            nr=(1, 0, 0), r=0.5, n=f"{side}_shoulder_control"
        )
        v = cmds.xform(f"{armJointList[0]}_joint", q=True, ws=True, t=True)
        cmds.move(v[0], v[1], v[2], f"{shoulderControl}")

        cmds.parentConstraint(shoulderControl, f"{armJointList[0]}_joint", mo=True)

        # elbow control
        elbowControl, _ = cmds.circle(nr=(1, 0, 0), r=0.5, n=f"{side}_elbow_control")
        v = cmds.xform(f"{armJointList[1]}_joint", q=True, ws=True, t=True)
        cmds.move(v[0], v[1], v[2], f"{elbowControl}")

        cmds.parentConstraint(elbowControl, f"{armJointList[1]}_joint", mo=True)

        # hand control
        handControl, _ = cmds.circle(nr=(1, 0, 0), r=0.5, n=f"{side}_hand_control")
        v = cmds.xform(f"{armJointList[3]}_joint", q=True, ws=True, t=True)
        cmds.move(v[0], v[1], v[2], f"{handControl}")

        v = cmds.xform(f"{armJointList[2]}_joint", q=True, ws=True, t=True)
        cmds.move(v[0], v[1], v[2], f"{handControl}.rotatePivot")

        cmds.parentConstraint(handControl, f"{armJointList[3]}_joint", mo=True)

        cmds.parent(handControl, elbowControl)
        cmds.parent(elbowControl, shoulderControl)
        cmds.parent(shoulderControl, chestControl)

        # lock attributes
        cmds.setAttr(handControl + ".ty", k=0, cb=0, l=1)
        cmds.setAttr(handControl + ".tz", k=0, cb=0, l=1)
        cmds.setAttr(handControl + ".tx", k=0, cb=0, l=1)
        # cmds.setAttr(handControl + ".rz", k = 0, cb = 0, l = 1)
        cmds.setAttr(handControl + ".rx", k=0, cb=0, l=1)
        cmds.setAttr(handControl + ".sy", k=0, cb=0, l=1)
        cmds.setAttr(handControl + ".sz", k=0, cb=0, l=1)
        cmds.setAttr(handControl + ".sx", k=0, cb=0, l=1)
        cmds.setAttr(handControl + ".v", k=0, cb=0, l=1)

        cmds.setAttr(elbowControl + ".ty", k=0, cb=0, l=1)
        cmds.setAttr(elbowControl + ".tz", k=0, cb=0, l=1)
        cmds.setAttr(elbowControl + ".tx", k=0, cb=0, l=1)
        # cmds.setAttr(elbowControl + ".rz", k=0, cb=0, l=1)
        # cmds.setAttr(elbowControl + ".rx", k = 0, cb = 0, l = 1)
        cmds.setAttr(elbowControl + ".sy", k=0, cb=0, l=1)
        cmds.setAttr(elbowControl + ".sz", k=0, cb=0, l=1)
        cmds.setAttr(elbowControl + ".sx", k=0, cb=0, l=1)
        cmds.setAttr(elbowControl + ".v", k=0, cb=0, l=1)

        cmds.setAttr(shoulderControl + ".ty", k=0, cb=0, l=1)
        cmds.setAttr(shoulderControl + ".tz", k=0, cb=0, l=1)
        cmds.setAttr(shoulderControl + ".tx", k=0, cb=0, l=1)
        cmds.setAttr(shoulderControl + ".sy", k=0, cb=0, l=1)
        cmds.setAttr(shoulderControl + ".sz", k=0, cb=0, l=1)
        cmds.setAttr(shoulderControl + ".sx", k=0, cb=0, l=1)
        cmds.setAttr(shoulderControl + ".v", k=0, cb=0, l=1)

    legRig("left")
    legRig("right")
    armRig("left")
    armRig("right")

    masterControl, _ = cmds.circle(nr=(0, 1, 0), r=3, n="master_control")
    for control in controlList:
        cmds.parent(control, masterControl)
    # lock attributes
    cmds.setAttr(masterControl + ".sy", k=0, cb=0, l=1)
    cmds.setAttr(masterControl + ".sz", k=0, cb=0, l=1)
    cmds.setAttr(masterControl + ".sx", k=0, cb=0, l=1)
    cmds.setAttr(masterControl + ".v", k=0, cb=0, l=1)

    cmds.hide(mainJoint)


cmds.select(clear=True)
rig(hip)


def walk_1(x=0.75, cycleLength=25):
    cmds.setKeyframe("root_control", at="translateY", v=2.95, t=[0])
    cmds.setKeyframe("root_control", at="translateY", v=2.85, t=[6])
    cmds.setKeyframe("root_control", at="translateY", v=2.95, t=[12])

    cmds.setKeyframe("root_control", at="rotateZ", v=-15, t=[-12])
    cmds.setKeyframe("root_control", at="rotateZ", v=15, t=[0])
    cmds.setKeyframe("root_control", at="rotateZ", v=-15, t=[12])
    cmds.setKeyframe("root_control", at="rotateZ", v=15, t=[24])
    cmds.setKeyframe("root_control", at="rotateZ", v=-15, t=[36])

    cmds.setKeyframe("root_control", at="rotateY", v=15, t=[-6])
    cmds.setKeyframe("root_control", at="rotateY", v=-15, t=[6])
    cmds.setKeyframe("root_control", at="rotateY", v=15, t=[18])
    cmds.setKeyframe("root_control", at="rotateY", v=-15, t=[30])

    cmds.selectKey("root_control", time=(1, 240))
    cmds.setInfinity(pri="cycle", poi="cycle")
    # cmds.keyTangent(f"root_control", itt="linear", ott="linear")

    cmds.rotate(-10, 0, 0, "waist_control")
    cmds.setKeyframe("waist_control", at="rotateZ", v=15, t=[-12])
    cmds.setKeyframe("waist_control", at="rotateZ", v=-15, t=[0])
    cmds.setKeyframe("waist_control", at="rotateZ", v=15, t=[12])
    cmds.setKeyframe("waist_control", at="rotateZ", v=-15, t=[24])
    cmds.setKeyframe("waist_control", at="rotateZ", v=15, t=[36])

    cmds.setKeyframe("waist_control", at="rotateY", v=-25, t=[-6])
    cmds.setKeyframe("waist_control", at="rotateY", v=25, t=[6])
    cmds.setKeyframe("waist_control", at="rotateY", v=-25, t=[18])
    cmds.setKeyframe("waist_control", at="rotateY", v=25, t=[30])

    # cmds.keyTangent(f"waist_control", itt="linear", ott="linear")

    cmds.rotate(-10, 0, 0, "neck_control")
    cmds.setKeyframe("neck_control", at="rotateZ", v=-1, t=[-6])
    cmds.setKeyframe("neck_control", at="rotateZ", v=1, t=[6])
    cmds.setKeyframe("neck_control", at="rotateZ", v=-1, t=[18])
    cmds.setKeyframe("neck_control", at="rotateZ", v=1, t=[30])

    cmds.setKeyframe("neck_control", at="rotateY", v=11, t=[-6])
    cmds.setKeyframe("neck_control", at="rotateY", v=-11, t=[6])
    cmds.setKeyframe("neck_control", at="rotateY", v=11, t=[18])
    cmds.setKeyframe("neck_control", at="rotateY", v=-11, t=[30])

    # cmds.setKeyframe('root_control', at = "translateY", v = 2.25, t = [18])
    # cmds.setKeyframe('root_control', at = "translateY", v = 2.75, t = [24])

    def walkSide(x, side):
        rotShoulderZ = 80

        if side == "left":
            x = -x
            rotX = 180
        else:
            rotX = 0
            rotShoulderZ = -rotShoulderZ
        walkPath, _ = cmds.circle(nr=(1, 0, 0), r=0.3, n=f"{side}_walk_path")
        cmds.move(x, 0.3, 0, walkPath, r=True)
        cmds.rotate(rotX, 0, 0, walkPath, r=True)
        # cmds.move(0, 0, .35, f'{walkPath}.cv[2]', r = True)
        # cmds.move(0, 0, .35, f'{walkPath}.cv[4]', r = True)
        # cmds.move(0, 0, .5, f'{walkPath}.cv[3]', r = True)
        # cmds.move(0, 0, -.35, f'{walkPath}.cv[0]', r = True)
        # cmds.move(0, 0, -.35, f'{walkPath}.cv[6]', r = True)
        # cmds.move(0, 0, -.5, f'{walkPath}.cv[7]', r = True)

        pathAnimName = cmds.pathAnimation(
            f"{side}_foot_control",
            c=walkPath,
            su=0,
            eu=8,
            stu=1,
            etu=cycleLength,
            n=f"{side}_path_animation",
        )

        cmds.keyTangent(f"{pathAnimName}_uValue", itt="linear", ott="linear")

        # create clusters
        for i in range(8):
            cmds.cluster(f"{walkPath}.cv[{i}]", n=f"{side}_cluster_{i}")
            cmds.rename(f"{side}_cluster_{i}Handle", f"{side}_cv_{i}")

        # cmds.setKeyframe(walkPath, at="translateZ", v=0, t=[0])
        # cmds.setKeyframe(walkPath, at="translateZ", v=2, t=[24])
        # cmds.setKeyframe('root_control', at="translateZ", v=0, t=[0])
        # cmds.setKeyframe('root_control', at="translateZ", v=2, t=[24])
        cmds.setKeyframe("left_knee_control", at="translateX", v=-0.562, t=[2])
        cmds.setKeyframe("left_knee_control", at="translateX", v=-0.34, t=[8])
        cmds.setKeyframe("left_knee_control", at="translateX", v=-0.562, t=[12])
        cmds.setKeyframe("left_knee_control", at="translateX", v=-0.34, t=[18])
        cmds.setKeyframe("right_knee_control", at="translateX", v=0.562, t=[2])
        cmds.setKeyframe("right_knee_control", at="translateX", v=0.34, t=[8])
        cmds.setKeyframe("right_knee_control", at="translateX", v=0.562, t=[12])
        cmds.setKeyframe("left_knee_control", at="translateX", v=-0.34, t=[18])
        cmds.selectKey(f"left_knee_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")
        cmds.keyTangent(f"left_knee_control", itt="linear", ott="linear")
        cmds.selectKey(f"right_knee_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")
        cmds.keyTangent(f"right_knee_control", itt="linear", ott="linear")

        # arms
        cmds.rotate(115, 0, rotShoulderZ, f"{side}_shoulder_control")
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=15, t=[0])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=0, t=[6])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=-15, t=[12])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=0, t=[18])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=15, t=[24])

        cmds.selectKey(f"{side}_shoulder_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")

        if side == "right":
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-5, t=[4])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=25, t=[16])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-5, t=[28])
        else:
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-25, t=[4])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-5, t=[16])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-25, t=[28])

        cmds.selectKey(f"{side}_elbow_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")

        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=8, t=[0])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=0, t=[6])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=-8, t=[12])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=0, t=[18])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=8, t=[24])

    walkSide(x, "left")
    walkSide(x, "right")

    # edit shape
    cmds.move(0, 0, -0.5, "left_cv_3", "right_cv_7", r=True)
    cmds.move(0, 0, 0, "left_cv_1", "right_cv_5", r=True)
    cmds.move(0, -0.1, -0.25, "left_cv_2", "right_cv_6", r=True)
    cmds.move(0, 0.25, -0.25, "left_cv_4", "right_cv_0", r=True)
    cmds.move(0, 0, 0, "left_cv_5", "right_cv_1", r=True)
    cmds.move(0, 0.1, 0.2, "left_cv_6", "right_cv_2", r=True)
    cmds.move(0, 0.1, 1, "left_cv_7", "right_cv_3", r=True)
    cmds.move(0, -0.1, 0.2, "left_cv_0", "right_cv_4", r=True)

    cmds.move(
        -0.65,
        0,
        0,
        "right_cv_4",
        "right_cv_5",
        "right_cv_6",
        "right_cv_7",
        r=True,
    )
    cmds.move(
        0.65,
        0,
        0,
        "left_cv_0",
        "left_cv_1",
        "left_cv_2",
        "left_cv_3",
        r=True,
    )
    cmds.move(-0.45, 0, 0, "right_cv_3", r=True)
    cmds.move(0.45, 0, 0, "left_cv_7", r=True)
    # cmds.move(-0.15, 0, 0, "right_cv_2", r=True)
    # cmds.move(0.15, 0, 0, "left_cv_6", r=True)
    cmds.move(0.25, 0, 0, "right_cv_1", r=True)
    cmds.move(-0.25, 0, 0, "left_cv_5", r=True)

    cmds.playbackOptions(minTime="0sec", maxTime=".958333333333sec")


def walk_2(x=0.75, cycleLength=36):
    cmds.setKeyframe("root_control", at="translateY", v=2.5, t=[0])
    cmds.setKeyframe("root_control", at="translateY", v=2.45, t=[24])
    cmds.setKeyframe("root_control", at="translateY", v=2.5, t=[48])

    cmds.setKeyframe("root_control", at="rotateZ", v=2, t=[0])
    cmds.setKeyframe("root_control", at="rotateZ", v=-2, t=[24])
    cmds.setKeyframe("root_control", at="rotateZ", v=2, t=[48])

    cmds.setKeyframe("root_control", at="rotateY", v=15, t=[-12])
    cmds.setKeyframe("root_control", at="rotateY", v=-15, t=[12])
    cmds.setKeyframe("root_control", at="rotateY", v=15, t=[36])
    cmds.setKeyframe("root_control", at="rotateY", v=-15, t=[60])

    cmds.selectKey("root_control", time=(1, 240))
    cmds.setInfinity(pri="cycle", poi="cycle")

    cmds.rotate(10, 0, 0, "waist_control")
    cmds.setKeyframe("waist_control", at="rotateZ", v=5, t=[-24])
    cmds.setKeyframe("waist_control", at="rotateZ", v=-5, t=[0])
    cmds.setKeyframe("waist_control", at="rotateZ", v=5, t=[24])
    cmds.setKeyframe("waist_control", at="rotateZ", v=-5, t=[48])

    cmds.setKeyframe("waist_control", at="rotateY", v=-15, t=[-12])
    cmds.setKeyframe("waist_control", at="rotateY", v=15, t=[12])
    cmds.setKeyframe("waist_control", at="rotateY", v=-15, t=[36])
    cmds.setKeyframe("waist_control", at="rotateY", v=15, t=[60])

    cmds.selectKey("waist_control", time=(1, 240))
    cmds.setInfinity(pri="cycle", poi="cycle")

    cmds.rotate(10, 0, 0, "neck_control")

    cmds.setKeyframe("neck_control", at="rotateZ", v=-1, t=[-12])
    cmds.setKeyframe("neck_control", at="rotateZ", v=1, t=[12])
    cmds.setKeyframe("neck_control", at="rotateZ", v=-1, t=[36])
    cmds.setKeyframe("neck_control", at="rotateZ", v=1, t=[60])

    cmds.setKeyframe("neck_control", at="rotateY", v=2, t=[12])
    cmds.setKeyframe("neck_control", at="rotateY", v=-2, t=[12])
    cmds.setKeyframe("neck_control", at="rotateY", v=2, t=[36])
    cmds.setKeyframe("neck_control", at="rotateY", v=-2, t=[60])

    cmds.selectKey("neck_control", time=(1, 240))
    cmds.setInfinity(pri="cycle", poi="cycle")

    def walkSide(x, side):
        rotShoulderZ = 80

        if side == "left":
            x = -x
            rotX = 180
        else:
            rotX = 0
            rotShoulderZ = -rotShoulderZ
        walkPath, _ = cmds.circle(nr=(1, 0, 0), r=0.3, n=f"{side}_walk_path")
        cmds.move(x, 0.3, 0, walkPath, r=True)
        cmds.rotate(rotX, 0, 0, walkPath, r=True)

        pathAnimName = cmds.pathAnimation(
            f"{side}_foot_control",
            c=walkPath,
            su=0,
            eu=8,
            stu=1,
            etu=cycleLength,
            n=f"{side}_path_animation",
        )

        cmds.keyTangent(f"{pathAnimName}_uValue", itt="linear", ott="linear")

        # create clusters
        for i in range(8):
            cmds.cluster(f"{walkPath}.cv[{i}]", n=f"{side}_cluster_{i}")
            cmds.rename(f"{side}_cluster_{i}Handle", f"{side}_cv_{i}")

        # arms
        cmds.rotate(115, 0, rotShoulderZ, f"{side}_shoulder_control")
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=5, t=[0])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=-5, t=[24])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=5, t=[48])

        cmds.selectKey(f"{side}_shoulder_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")

        if side == "right":
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-1, t=[4])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=5, t=[16])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-1, t=[28])
        else:
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-5, t=[4])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-1, t=[16])
            cmds.setKeyframe(f"{side}_elbow_control", at="rotateZ", v=-5, t=[28])

        cmds.selectKey(f"{side}_elbow_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")

        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=1, t=[0])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=0, t=[6])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=-1, t=[12])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=0, t=[18])
        cmds.setKeyframe(f"{side}_hand_control", at="rotateZ", v=1, t=[24])

    walkSide(x, "left")
    walkSide(x, "right")

    # edit shape
    cmds.move(0, -0.3, -0.5, "left_cv_3", "right_cv_7", r=True)
    cmds.move(0, 0, 0, "left_cv_1", "right_cv_5", r=True)
    cmds.move(0, -0.1, -0.25, "left_cv_2", "right_cv_6", r=True)
    cmds.move(0, -0.4, -0.25, "left_cv_4", "right_cv_0", r=True)
    cmds.move(0, -0.4, 0, "left_cv_5", "right_cv_1", r=True)
    cmds.move(0, -0.4, 0.2, "left_cv_6", "right_cv_2", r=True)
    cmds.move(0, -0.25, 0.25, "left_cv_7", "right_cv_3", r=True)
    cmds.move(0, -0.1, 0.2, "left_cv_0", "right_cv_4", r=True)

    cmds.playbackOptions(minTime="0sec", maxTime="1.95833333sec")


def run(x=0.75, cycleLength=25):
    cmds.move(0, 0, .75, "root_control", r = True)
    cmds.setKeyframe("root_control", at="translateY", v=2.9, t=[0])
    cmds.setKeyframe("root_control", at="translateY", v=2.85, t=[9])
    cmds.setKeyframe("root_control", at="translateY", v=2.9, t=[18])

    cmds.setKeyframe("root_control", at="rotateZ", v=-8, t=[-9])
    cmds.setKeyframe("root_control", at="rotateZ", v=8, t=[0])
    cmds.setKeyframe("root_control", at="rotateZ", v=-8, t=[9])
    cmds.setKeyframe("root_control", at="rotateZ", v=8, t=[18])
    cmds.setKeyframe("root_control", at="rotateZ", v=-8, t=[27])

    cmds.setKeyframe("root_control", at="rotateY", v=8, t=[-4.5])
    cmds.setKeyframe("root_control", at="rotateY", v=-8, t=[4.5])
    cmds.setKeyframe("root_control", at="rotateY", v=8, t=[13.5])
    cmds.setKeyframe("root_control", at="rotateY", v=-8, t=[22.5])

    cmds.selectKey("root_control", time=(1, 240))
    cmds.setInfinity(pri="cycle", poi="cycle")
    # # cmds.keyTangent(f"root_control", itt="linear", ott="linear")

    cmds.rotate(35, 0, 0, "waist_control")
    cmds.setKeyframe("waist_control", at="rotateZ", v=5, t=[-9])
    cmds.setKeyframe("waist_control", at="rotateZ", v=-5, t=[0])
    cmds.setKeyframe("waist_control", at="rotateZ", v=5, t=[9])
    cmds.setKeyframe("waist_control", at="rotateZ", v=-5, t=[18])
    cmds.setKeyframe("waist_control", at="rotateZ", v=5, t=[27])

    cmds.setKeyframe("waist_control", at="rotateY", v=-25, t=[-4.5])
    cmds.setKeyframe("waist_control", at="rotateY", v=25, t=[4.5])
    cmds.setKeyframe("waist_control", at="rotateY", v=-25, t=[13.5])
    cmds.setKeyframe("waist_control", at="rotateY", v=25, t=[22.5])

    cmds.selectKey("waist_control", time=(1, 240))
    cmds.setInfinity(pri="cycle", poi="cycle")

    cmds.rotate(18, 0, 0, "chest_control")

    cmds.setAttr("neck_control.rotateOrder", 1)
    cmds.setKeyframe("neck_control", at = "rotateX", v = -55, t = [0])

    # cmds.setKeyframe("neck_control", at="rotateZ", v=-5, t=[-9])
    # cmds.setKeyframe("neck_control", at="rotateZ", v=5, t=[0])
    # cmds.setKeyframe("neck_control", at="rotateZ", v=-5, t=[9])
    # cmds.setKeyframe("neck_control", at="rotateZ", v=5, t=[18])
    # cmds.setKeyframe("neck_control", at="rotateZ", v=-5, t=[27])

    # cmds.setKeyframe("neck_control", at="rotateY", v=25, t=[-4.5])
    # cmds.setKeyframe("neck_control", at = "rotateY", v = -25, t = [4.5])
    # cmds.setKeyframe("neck_control", at="rotateY", v=25, t=[13.5])
    # cmds.setKeyframe("neck_control", at="rotateY", v=-25, t=[22.5])


    # # cmds.setKeyframe('root_control', at = "translateY", v = 2.25, t = [18])
    # # cmds.setKeyframe('root_control', at = "translateY", v = 2.75, t = [24])

    def walkSide(x, side):
        rotShoulderZ = 65
        rotElbowZ = 100

        if side == "left":
            x = -x
            rotX = 180
            rotElbowZ = -rotElbowZ
        else:
            rotX = 0
            rotShoulderZ = -rotShoulderZ
        walkPath, _ = cmds.circle(nr=(1, 0, 0), r=0.3, n=f"{side}_walk_path")
        cmds.move(x, 0.3, 0, walkPath, r=True)
        cmds.rotate(rotX, 0, 0, walkPath, r=True)
        # cmds.move(0, 0, .35, f'{walkPath}.cv[2]', r = True)
        # cmds.move(0, 0, .35, f'{walkPath}.cv[4]', r = True)
        # cmds.move(0, 0, .5, f'{walkPath}.cv[3]', r = True)
        # cmds.move(0, 0, -.35, f'{walkPath}.cv[0]', r = True)
        # cmds.move(0, 0, -.35, f'{walkPath}.cv[6]', r = True)
        # cmds.move(0, 0, -.5, f'{walkPath}.cv[7]', r = True)

        pathAnimName = cmds.pathAnimation(
            f"{side}_foot_control",
            c=walkPath,
            su=0,
            eu=8,
            stu=1,
            etu=cycleLength,
            n=f"{side}_path_animation",
        )

        cmds.keyTangent(f"{pathAnimName}_uValue", itt="linear", ott="linear")

        # create clusters
        for i in range(8):
            cmds.cluster(f"{walkPath}.cv[{i}]", n=f"{side}_cluster_{i}")
            cmds.rename(f"{side}_cluster_{i}Handle", f"{side}_cv_{i}")

        # arms
        cmds.rotate(115, 25, rotShoulderZ, f"{side}_shoulder_control")
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=65, t=[0])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=-65, t=[9])
        cmds.setKeyframe(f"{side}_shoulder_control", at="rotateY", v=65, t=[18])

        cmds.selectKey(f"{side}_shoulder_control", time=(1, 240))
        cmds.setInfinity(pri="cycle", poi="cycle")
        
        cmds.keyTangent(f"{side}_shoulder_control", itt="linear", ott="linear")

        cmds.rotate(0, 0, rotElbowZ, f"{side}_elbow_control")

    walkSide(x, "left")
    walkSide(x, "right")

    # edit shape
    cmds.move(0, .25, -2, "left_cv_3", "right_cv_7", r=True)
    cmds.move(0, 0, 0, "left_cv_1", "right_cv_5", r=True)
    cmds.move(0, -0.15, -0.5, "left_cv_2", "right_cv_6", r=True)
    cmds.move(0, 0.5, -0.35, "left_cv_4", "right_cv_0", r=True)
    cmds.move(0, .1, 0, "left_cv_5", "right_cv_1", r=True)
    cmds.move(0, 0.1, 0.2, "left_cv_6", "right_cv_2", r=True)
    cmds.move(0, 0.1, 1, "left_cv_7", "right_cv_3", r=True)
    cmds.move(0, -0.1, 0.2, "left_cv_0", "right_cv_4", r=True)

    cmds.playbackOptions(minTime="0sec", maxTime=".708333333sec")


walk_1(x=0.75, cycleLength=25)
# walk_2(x = 0.75, cycleLength = 48)
#run(x=0.75, cycleLength=19)
