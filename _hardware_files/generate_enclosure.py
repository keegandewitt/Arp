"""
MIDI Arpeggiator Enclosure - Fusion 360 Auto-Generator Script
Version: 1.0
Date: 2025-10-15

This script automatically generates the complete enclosure design in Fusion 360.

USAGE:
1. Open Fusion 360
2. Go to Tools → Add-Ins → Scripts and Add-Ins
3. Click "+" to add a script
4. Browse to this file (generate_enclosure.py)
5. Click "Run"
6. Wait ~30-60 seconds for generation to complete
7. Enclosure will be created in a new design

The script creates:
- Bottom shell with mounting features
- Front panel with MIDI and CV jack cutouts
- Rear panel with USB-C cutout
- Left side panel with slide switch cutout
- Right side panel (solid)
- Top panel with OLED window and button holes
"""

import adsk.core
import adsk.fusion
import traceback

# Global variables for the Fusion 360 application context
app = adsk.core.Application.get()
ui = app.userInterface
design = None
rootComp = None

# Enclosure dimensions (all in cm for Fusion 360 API)
ENCLOSURE_WIDTH = 14.0  # 140mm
ENCLOSURE_DEPTH = 10.0  # 100mm
ENCLOSURE_HEIGHT = 6.0  # 60mm
WALL_THICKNESS = 0.25   # 2.5mm

# Component positions and dimensions
FEATHER_LENGTH = 5.08   # 50.8mm
FEATHER_WIDTH = 2.286   # 22.86mm
FEATHER_HOLE_SPACING_X = 4.572  # 45.72mm
FEATHER_HOLE_SPACING_Y = 1.778  # 17.78mm
STANDOFF_DIAMETER = 0.5  # 5mm
STANDOFF_HEIGHT = 0.6    # 6mm
SCREW_HOLE_DIAMETER = 0.27  # 2.7mm (M2.5 clearance)

# Panel cutout dimensions
MIDI_HOLE_DIAMETER = 1.4  # 14mm (DIN-5)
TRS_HOLE_DIAMETER = 0.6   # 6mm (3.5mm jack)
USB_WIDTH = 1.0           # 10mm
USB_HEIGHT = 0.5          # 5mm
OLED_WINDOW_WIDTH = 3.0   # 30mm
OLED_WINDOW_HEIGHT = 1.5  # 15mm
BUTTON_HOLE_DIAMETER = 0.4  # 4mm

def run(context):
    try:
        global design, rootComp

        # Create a new document
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component
        rootComp = design.rootComponent

        ui.messageBox('Starting enclosure generation...\nThis will take 30-60 seconds.')

        # Create all components
        create_bottom_shell()
        create_front_panel()
        create_rear_panel()
        create_side_panels()
        create_top_panel()

        # Fit view to show entire model
        app.activeViewport.fit()

        ui.messageBox('Enclosure generation complete!\n\nNext steps:\n1. Review the design\n2. Export each component as STL\n3. Slice and print')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def create_bottom_shell():
    """Create the bottom shell with all mounting features"""

    # Create a new component for bottom shell
    bottomOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    bottomComp = bottomOcc.component
    bottomComp.name = "Bottom_Shell"

    sketches = bottomComp.sketches
    extrudes = bottomComp.features.extrudeFeatures

    # Create base rectangle sketch
    xyPlane = bottomComp.xYConstructionPlane
    baseSketch = sketches.add(xyPlane)

    # Draw outer rectangle (centered on origin)
    rectangles = baseSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(ENCLOSURE_WIDTH/2, ENCLOSURE_DEPTH/2, 0)
    )

    # Extrude base box
    profile = baseSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(ENCLOSURE_HEIGHT)
    extInput.setDistanceExtent(False, distance)
    baseExtrude = extrudes.add(extInput)

    # Shell the box (remove top face)
    shells = bottomComp.features.shellFeatures
    body = baseExtrude.bodies.item(0)
    topFace = None

    # Find top face (highest Z coordinate)
    for face in body.faces:
        if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
            centroid = face.pointOnFace
            if centroid.z > ENCLOSURE_HEIGHT - 0.1:  # Top face
                topFace = face
                break

    if topFace:
        shellInput = shells.createInput(adsk.core.ObjectCollection.create())
        shellInput.insideThickness = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
        shellInput.facesToRemove.add(topFace)
        shells.add(shellInput)

    # Create internal floor
    create_internal_floor(bottomComp, sketches, extrudes)

    # Create PCB standoffs
    create_pcb_standoffs(bottomComp, sketches, extrudes)

    # Create mounting posts for modules
    create_module_posts(bottomComp, sketches, extrudes)

    # Create battery compartment
    create_battery_compartment(bottomComp, sketches, extrudes)

    # Create corner screw posts
    create_corner_posts(bottomComp, sketches, extrudes)


def create_internal_floor(comp, sketches, extrudes):
    """Create internal floor for component mounting"""

    xyPlane = comp.xYConstructionPlane
    floorSketch = sketches.add(xyPlane)

    # Internal floor rectangle (5mm smaller than outer)
    rectangles = floorSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create((ENCLOSURE_WIDTH - 0.5)/2, (ENCLOSURE_DEPTH - 0.5)/2, 0)
    )

    # Extrude floor upward 2mm
    profile = floorSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(0.2)  # 2mm
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_pcb_standoffs(comp, sketches, extrudes):
    """Create 4 standoffs for Feather PCB stack"""

    # Create sketch on internal floor (offset 2mm from bottom)
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    standoffSketch = sketches.add(offsetPlane)
    circles = standoffSketch.sketchCurves.sketchCircles

    # Calculate standoff positions (centered, 25mm from front)
    center_x = 0
    center_y = -1.5  # 15mm from front panel (negative = toward front)

    # 4 standoff positions based on Feather hole spacing
    positions = [
        (center_x - FEATHER_HOLE_SPACING_X/2, center_y + FEATHER_HOLE_SPACING_Y/2),  # Front-left
        (center_x + FEATHER_HOLE_SPACING_X/2, center_y + FEATHER_HOLE_SPACING_Y/2),  # Front-right
        (center_x - FEATHER_HOLE_SPACING_X/2, center_y - FEATHER_HOLE_SPACING_Y/2),  # Rear-left
        (center_x + FEATHER_HOLE_SPACING_X/2, center_y - FEATHER_HOLE_SPACING_Y/2),  # Rear-right
    ]

    for x, y in positions:
        circles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            STANDOFF_DIAMETER/2
        )

    # Extrude standoffs
    for i in range(standoffSketch.profiles.count):
        profile = standoffSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(STANDOFF_HEIGHT)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

    # Create screw holes through standoffs
    holeSketch = sketches.add(offsetPlane)
    holeCircles = holeSketch.sketchCurves.sketchCircles

    for x, y in positions:
        holeCircles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            SCREW_HOLE_DIAMETER/2
        )

    # Extrude cut holes
    for i in range(holeSketch.profiles.count):
        profile = holeSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(STANDOFF_HEIGHT)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def create_module_posts(comp, sketches, extrudes):
    """Create mounting posts for boost module and DAC"""

    # Create sketch on internal floor
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    postSketch = sketches.add(offsetPlane)
    rectangles = postSketch.sketchCurves.sketchLines

    # Boost module post (left side of stack)
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(-4.5, -1.5, 0),  # Left side
        adsk.core.Point3D.create(-4.5 + 1.25, -1.5 + 0.75, 0)  # 25mm × 15mm
    )

    # DAC post (right side of stack)
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(4.5, -1.5, 0),  # Right side
        adsk.core.Point3D.create(4.5 + 1.5, -1.5 + 1.0, 0)  # 30mm × 20mm
    )

    # Extrude posts
    for i in range(postSketch.profiles.count):
        profile = postSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(0.3)  # 3mm high
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def create_battery_compartment(comp, sketches, extrudes):
    """Create battery compartment in rear section"""

    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    battSketch = sketches.add(offsetPlane)
    rectangles = battSketch.sketchCurves.sketchLines

    # Battery compartment walls (55mm × 38mm)
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, -3.5, 0),  # Rear section
        adsk.core.Point3D.create(2.75, -3.5 + 1.9, 0)
    )

    # Extrude walls
    profile = battSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(0.8)  # 8mm high
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Create Velcro strap slot
    strapSketch = sketches.add(offsetPlane)
    strapRect = strapSketch.sketchCurves.sketchLines
    strapRect.addCenterPointRectangle(
        adsk.core.Point3D.create(0, -3.5, 0),
        adsk.core.Point3D.create(2.5, -3.5 + 0.5, 0)  # 50mm × 10mm slot
    )

    # Cut slot
    profile = strapSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(0.2)  # 2mm deep
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_corner_posts(comp, sketches, extrudes):
    """Create corner posts for panel assembly screws"""

    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    postSketch = sketches.add(offsetPlane)
    circles = postSketch.sketchCurves.sketchCircles

    # 4 corner positions (5mm from edges)
    corner_offset_x = ENCLOSURE_WIDTH/2 - 0.5
    corner_offset_y = ENCLOSURE_DEPTH/2 - 0.5

    positions = [
        (-corner_offset_x, corner_offset_y),   # Front-left
        (corner_offset_x, corner_offset_y),    # Front-right
        (-corner_offset_x, -corner_offset_y),  # Rear-left
        (corner_offset_x, -corner_offset_y),   # Rear-right
    ]

    for x, y in positions:
        circles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            0.3  # 6mm diameter
        )

    # Extrude posts
    for i in range(postSketch.profiles.count):
        profile = postSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(5.5)  # 55mm high
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

    # Create screw holes in posts
    holeSketch = sketches.add(offsetPlane)
    holeCircles = holeSketch.sketchCurves.sketchCircles

    for x, y in positions:
        holeCircles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            0.16  # 3.2mm diameter (M3 clearance)
        )

    # Cut holes
    for i in range(holeSketch.profiles.count):
        profile = holeSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(5.5)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def create_front_panel():
    """Create front panel with MIDI and CV jack cutouts"""

    # Create new component
    frontOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    frontComp = frontOcc.component
    frontComp.name = "Front_Panel"

    sketches = frontComp.sketches
    extrudes = frontComp.features.extrudeFeatures

    # Create panel base on YZ plane
    yzPlane = frontComp.yZConstructionPlane
    panelSketch = sketches.add(yzPlane)

    rectangles = panelSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, ENCLOSURE_HEIGHT/2, ENCLOSURE_DEPTH/2),
        adsk.core.Point3D.create(0, ENCLOSURE_HEIGHT/2 + ENCLOSURE_HEIGHT/2, ENCLOSURE_DEPTH/2 + ENCLOSURE_DEPTH/2)
    )

    # Extrude panel
    profile = panelSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Create MIDI jack holes
    create_midi_holes(frontComp, sketches, extrudes, yzPlane)

    # Create CV/Gate jack holes
    create_cv_holes(frontComp, sketches, extrudes, yzPlane)


def create_midi_holes(comp, sketches, extrudes, basePlane):
    """Create MIDI DIN-5 jack holes"""

    holeSketch = sketches.add(basePlane)
    circles = holeSketch.sketchCurves.sketchCircles

    # MIDI IN and OUT positions (left side, centered vertically)
    midi_y = ENCLOSURE_HEIGHT/2 + 3.0  # 30mm from bottom

    # MIDI IN
    circles.addByCenterRadius(
        adsk.core.Point3D.create(0, midi_y, -4.0),  # -40mm from center
        MIDI_HOLE_DIAMETER/2
    )

    # MIDI OUT
    circles.addByCenterRadius(
        adsk.core.Point3D.create(0, midi_y, -1.0),  # -10mm from center
        MIDI_HOLE_DIAMETER/2
    )

    # Cut holes
    for i in range(holeSketch.profiles.count):
        profile = holeSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def create_cv_holes(comp, sketches, extrudes, basePlane):
    """Create CV/Gate TRS jack holes"""

    holeSketch = sketches.add(basePlane)
    circles = holeSketch.sketchCurves.sketchCircles

    # CV and Gate positions (right side, centered vertically)
    cv_y = ENCLOSURE_HEIGHT/2 + 3.0  # 30mm from bottom

    # CV (Pitch)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(0, cv_y, 2.5),  # 25mm from center
        TRS_HOLE_DIAMETER/2
    )

    # GATE
    circles.addByCenterRadius(
        adsk.core.Point3D.create(0, cv_y, 4.2),  # 42mm from center
        TRS_HOLE_DIAMETER/2
    )

    # Cut holes
    for i in range(holeSketch.profiles.count):
        profile = holeSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def create_rear_panel():
    """Create rear panel with USB-C cutout"""

    # Create new component
    rearOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    rearComp = rearOcc.component
    rearComp.name = "Rear_Panel"

    sketches = rearComp.sketches
    extrudes = rearComp.features.extrudeFeatures

    # Create panel base on YZ plane
    yzPlane = rearComp.yZConstructionPlane
    panelSketch = sketches.add(yzPlane)

    rectangles = panelSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, ENCLOSURE_HEIGHT/2, -ENCLOSURE_DEPTH/2),
        adsk.core.Point3D.create(0, ENCLOSURE_HEIGHT/2 + ENCLOSURE_HEIGHT/2, -ENCLOSURE_DEPTH/2 - ENCLOSURE_DEPTH/2)
    )

    # Extrude panel
    profile = panelSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(-WALL_THICKNESS)  # Extrude backward
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Create USB-C cutout
    usbSketch = sketches.add(yzPlane)
    usbRect = usbSketch.sketchCurves.sketchLines
    usbRect.addCenterPointRectangle(
        adsk.core.Point3D.create(0, ENCLOSURE_HEIGHT/2 + 1.5, -ENCLOSURE_DEPTH/2),  # 15mm from bottom, centered
        adsk.core.Point3D.create(USB_WIDTH/2, ENCLOSURE_HEIGHT/2 + 1.5 + USB_HEIGHT/2, -ENCLOSURE_DEPTH/2)
    )

    # Cut USB-C hole
    profile = usbSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_side_panels():
    """Create left and right side panels"""

    # Left side panel (with slide switch cutout)
    create_left_panel()

    # Right side panel (solid)
    create_right_panel()


def create_left_panel():
    """Create left side panel with slide switch cutout"""

    leftOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    leftComp = leftOcc.component
    leftComp.name = "Left_Side_Panel"

    sketches = leftComp.sketches
    extrudes = leftComp.features.extrudeFeatures

    # Create panel on XZ plane
    xzPlane = leftComp.xZConstructionPlane
    panelSketch = sketches.add(xzPlane)

    rectangles = panelSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, ENCLOSURE_HEIGHT/2),
        adsk.core.Point3D.create(ENCLOSURE_WIDTH/2, 0, ENCLOSURE_HEIGHT/2 + ENCLOSURE_HEIGHT/2)
    )

    # Extrude panel
    profile = panelSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Create slide switch cutout (centered on panel)
    switchSketch = sketches.add(xzPlane)
    switchRect = switchSketch.sketchCurves.sketchLines
    switchRect.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, ENCLOSURE_HEIGHT/2 + 3.0),  # Center, 30mm from bottom
        adsk.core.Point3D.create(0.6, 0, ENCLOSURE_HEIGHT/2 + 3.0 + 0.3)  # 12mm × 6mm
    )

    # Cut switch hole
    profile = switchSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(1.0)  # 10mm deep cutout
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_right_panel():
    """Create right side panel (solid, no cutouts)"""

    rightOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    rightComp = rightOcc.component
    rightComp.name = "Right_Side_Panel"

    sketches = rightComp.sketches
    extrudes = rightComp.features.extrudeFeatures

    # Create panel on XZ plane
    xzPlane = rightComp.xZConstructionPlane
    panelSketch = sketches.add(xzPlane)

    rectangles = panelSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, ENCLOSURE_HEIGHT/2),
        adsk.core.Point3D.create(ENCLOSURE_WIDTH/2, 0, ENCLOSURE_HEIGHT/2 + ENCLOSURE_HEIGHT/2)
    )

    # Extrude panel
    profile = panelSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(-WALL_THICKNESS)  # Extrude in negative direction
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_top_panel():
    """Create top panel with OLED window and button holes"""

    topOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    topComp = topOcc.component
    topComp.name = "Top_Panel"

    sketches = topComp.sketches
    extrudes = topComp.features.extrudeFeatures

    # Create panel on XY plane (at top of enclosure)
    planes = topComp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(ENCLOSURE_HEIGHT)
    planeInput.setByOffset(topComp.xYConstructionPlane, offsetValue)
    topPlane = planes.add(planeInput)

    panelSketch = sketches.add(topPlane)
    rectangles = panelSketch.sketchCurves.sketchLines
    rectangles.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(ENCLOSURE_WIDTH/2, ENCLOSURE_DEPTH/2, 0)
    )

    # Extrude panel
    profile = panelSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Create OLED display window
    oledSketch = sketches.add(topPlane)
    oledRect = oledSketch.sketchCurves.sketchLines
    oledRect.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 2.0, 0),  # Forward from center
        adsk.core.Point3D.create(OLED_WINDOW_WIDTH/2, 2.0 + OLED_WINDOW_HEIGHT/2, 0)
    )

    # Cut OLED window
    profile = oledSketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Create button holes
    buttonSketch = sketches.add(topPlane)
    circles = buttonSketch.sketchCurves.sketchCircles

    # 3 buttons (A, B, C) below OLED
    button_y = 0.5  # 5mm from center
    circles.addByCenterRadius(adsk.core.Point3D.create(-1.2, button_y, 0), BUTTON_HOLE_DIAMETER/2)  # Button A
    circles.addByCenterRadius(adsk.core.Point3D.create(0, button_y, 0), BUTTON_HOLE_DIAMETER/2)     # Button B
    circles.addByCenterRadius(adsk.core.Point3D.create(1.2, button_y, 0), BUTTON_HOLE_DIAMETER/2)   # Button C

    # Cut button holes
    for i in range(buttonSketch.profiles.count):
        profile = buttonSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(WALL_THICKNESS)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def stop(context):
    try:
        pass
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
