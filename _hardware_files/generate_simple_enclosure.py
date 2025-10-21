"""
MIDI Arpeggiator Enclosure - Simplified Single-Body Generator
Version: 2.0 (Simplified)
Date: 2025-10-15

This creates a complete, print-ready enclosure as a single body with all features.
Much simpler and more reliable than the multi-component version.

USAGE:
1. Open Fusion 360
2. Create New Design (Cmd+N / Ctrl+N)
3. Press Shift+S (Scripts & Add-Ins)
4. Add this script
5. Run it
6. Wait ~15 seconds
7. Export as STL and print!

Creates:
- Complete enclosure shell (140×100×60mm)
- All mounting standoffs and posts
- All panel cutouts (MIDI, CV, USB-C, switch, OLED, buttons)
- Ready to slice and print
"""

import adsk.core
import adsk.fusion
import traceback

app = adsk.core.Application.get()
ui = app.userInterface

def run(context):
    try:
        ui.messageBox('Generating simplified enclosure...\nThis will take ~15 seconds.')

        # Get active design
        design = app.activeProduct
        rootComp = design.rootComponent

        # Units are in cm for Fusion 360 API

        # Create the main enclosure box
        create_main_enclosure(rootComp)

        # Add internal features
        add_pcb_standoffs(rootComp)
        add_mounting_posts(rootComp)
        add_battery_compartment(rootComp)
        add_corner_posts(rootComp)

        # Add all panel cutouts
        add_front_panel_holes(rootComp)
        add_rear_panel_holes(rootComp)
        add_side_panel_holes(rootComp)
        add_top_panel_holes(rootComp)

        # Fit view
        app.activeViewport.fit()

        ui.messageBox('Complete!\n\nYour enclosure is ready.\n\nNext: File → 3D Print → Export STL')

    except:
        ui.messageBox('Error:\n{}'.format(traceback.format_exc()))


def create_main_enclosure(comp):
    """Create the main box with hollow interior"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Dimensions (cm)
    width = 14.0   # 140mm
    depth = 10.0   # 100mm
    height = 6.0   # 60mm
    wall = 0.25    # 2.5mm

    # Create base rectangle on XY plane
    sketch = sketches.add(comp.xYConstructionPlane)
    rect = sketch.sketchCurves.sketchLines
    rect.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width/2, depth/2, 0)
    )

    # Extrude box upward
    profile = sketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(height)
    extInput.setDistanceExtent(False, distance)
    baseExtrude = extrudes.add(extInput)

    # Shell it (remove top face)
    shells = comp.features.shellFeatures
    body = baseExtrude.bodies.item(0)

    # Find and remove top face
    topFace = None
    for face in body.faces:
        if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
            point = face.pointOnFace
            if point.z > height - 0.1:
                topFace = face
                break

    if topFace:
        faceCollection = adsk.core.ObjectCollection.create()
        faceCollection.add(topFace)
        shellInput = shells.createInput(faceCollection)
        shellInput.insideThickness = adsk.core.ValueInput.createByReal(wall)
        shells.add(shellInput)

    # Add internal floor (2mm thick, 5mm smaller than outer box)
    floorSketch = sketches.add(comp.xYConstructionPlane)
    floorRect = floorSketch.sketchCurves.sketchLines
    floorRect.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create((width - 0.5)/2, (depth - 0.5)/2, 0)
    )

    floorProfile = floorSketch.profiles.item(0)
    floorExtInput = extrudes.createInput(floorProfile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    floorDist = adsk.core.ValueInput.createByReal(0.2)  # 2mm thick
    floorExtInput.setDistanceExtent(False, floorDist)
    extrudes.add(floorExtInput)


def add_pcb_standoffs(comp):
    """Add 4 standoffs for PCB stack with M2.5 screw holes"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Create construction plane 2mm above floor
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    # Sketch for standoffs
    sketch = sketches.add(offsetPlane)
    circles = sketch.sketchCurves.sketchCircles

    # Feather mounting hole positions (45.72mm × 17.78mm spacing)
    hole_x = 4.572 / 2  # 22.86mm from center
    hole_y = 1.778 / 2  # 8.89mm from center
    center_y = -1.5      # Offset 15mm toward front

    positions = [
        (-hole_x, center_y + hole_y),  # Front-left
        (hole_x, center_y + hole_y),   # Front-right
        (-hole_x, center_y - hole_y),  # Rear-left
        (hole_x, center_y - hole_y),   # Rear-right
    ]

    # Draw standoff circles (5mm diameter)
    for x, y in positions:
        circles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            0.25  # 2.5mm radius = 5mm diameter
        )

    # Extrude standoffs upward 6mm
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(0.6)  # 6mm high
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

    # Cut M2.5 screw holes through standoffs
    holeSketch = sketches.add(offsetPlane)
    holeCircles = holeSketch.sketchCurves.sketchCircles

    for x, y in positions:
        holeCircles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            0.135  # 1.35mm radius = 2.7mm diameter (M2.5 clearance)
        )

    # Cut holes
    for i in range(holeSketch.profiles.count):
        profile = holeSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(0.6)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def add_mounting_posts(comp):
    """Add mounting posts for boost module and DAC"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Create plane 2mm above floor
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    sketch = sketches.add(offsetPlane)
    lines = sketch.sketchCurves.sketchLines

    # Boost module post (left, 25×15mm)
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(-4.5, -1.5, 0),
        adsk.core.Point3D.create(-4.5 + 1.25, -1.5 + 0.75, 0)
    )

    # DAC post (right, 30×20mm)
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(4.5, -1.5, 0),
        adsk.core.Point3D.create(4.5 + 1.5, -1.5 + 1.0, 0)
    )

    # Extrude both posts 3mm high
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(0.3)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def add_battery_compartment(comp):
    """Add battery compartment walls and strap slot"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Create plane 2mm above floor
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    # Battery compartment outline (55×38mm)
    sketch = sketches.add(offsetPlane)
    lines = sketch.sketchCurves.sketchLines
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, -3.5, 0),  # Rear section
        adsk.core.Point3D.create(2.75, -3.5 + 1.9, 0)
    )

    # Extrude walls 8mm high
    profile = sketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(0.8)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Velcro strap slot (50×10mm, 2mm deep)
    strapSketch = sketches.add(offsetPlane)
    strapLines = strapSketch.sketchCurves.sketchLines
    strapLines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, -3.5, 0),
        adsk.core.Point3D.create(2.5, -3.5 + 0.5, 0)
    )

    # Cut slot
    strapProfile = strapSketch.profiles.item(0)
    strapExtInput = extrudes.createInput(strapProfile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    strapDist = adsk.core.ValueInput.createByReal(0.2)
    strapExtInput.setDistanceExtent(False, strapDist)
    extrudes.add(strapExtInput)


def add_corner_posts(comp):
    """Add 4 corner posts with M3 screw holes for panel assembly"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Create plane 2mm above floor
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetValue = adsk.core.ValueInput.createByReal(0.2)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetValue)
    offsetPlane = planes.add(planeInput)

    sketch = sketches.add(offsetPlane)
    circles = sketch.sketchCurves.sketchCircles

    # Corner positions (5mm from edges)
    offset_x = 14.0/2 - 0.5  # 6.5cm from center
    offset_y = 10.0/2 - 0.5  # 4.5cm from center

    positions = [
        (-offset_x, offset_y),   # Front-left
        (offset_x, offset_y),    # Front-right
        (-offset_x, -offset_y),  # Rear-left
        (offset_x, -offset_y),   # Rear-right
    ]

    # Draw posts (6mm diameter)
    for x, y in positions:
        circles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            0.3
        )

    # Extrude posts 55mm high (almost to top)
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(5.5)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

    # Cut M3 screw holes
    holeSketch = sketches.add(offsetPlane)
    holeCircles = holeSketch.sketchCurves.sketchCircles

    for x, y in positions:
        holeCircles.addByCenterRadius(
            adsk.core.Point3D.create(x, y, 0),
            0.16  # 3.2mm diameter (M3 clearance)
        )

    for i in range(holeSketch.profiles.count):
        profile = holeSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(5.5)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def add_front_panel_holes(comp):
    """Add MIDI and CV/Gate jack holes to front panel"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Create construction plane for front face
    planes = comp.constructionPlanes
    planeInput = planes.createInput()

    # Front panel is at Y = +depth/2 = +5.0cm
    offsetDist = adsk.core.ValueInput.createByReal(5.0)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetDist)
    frontPlane = planes.add(planeInput)

    sketch = sketches.add(frontPlane)
    circles = sketch.sketchCurves.sketchCircles

    # All holes at 30mm (3cm) from bottom
    hole_z = 3.0

    # MIDI holes (14mm diameter, left side)
    # MIDI IN at -40mm from center
    circles.addByCenterRadius(
        adsk.core.Point3D.create(-4.0, 0, hole_z),
        0.7  # 7mm radius = 14mm diameter
    )

    # MIDI OUT at -10mm from center
    circles.addByCenterRadius(
        adsk.core.Point3D.create(-1.0, 0, hole_z),
        0.7
    )

    # CV/Gate holes (6mm diameter, right side)
    # CV at +25mm from center
    circles.addByCenterRadius(
        adsk.core.Point3D.create(2.5, 0, hole_z),
        0.3  # 3mm radius = 6mm diameter
    )

    # Gate at +42mm from center
    circles.addByCenterRadius(
        adsk.core.Point3D.create(4.2, 0, hole_z),
        0.3
    )

    # Cut all holes through wall (2.5mm)
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        # Cut outward (toward +Y)
        distance = adsk.core.ValueInput.createByReal(-0.3)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def add_rear_panel_holes(comp):
    """Add USB-C cutout to rear panel"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Rear panel is at Y = -depth/2 = -5.0cm
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetDist = adsk.core.ValueInput.createByReal(-5.0)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetDist)
    rearPlane = planes.add(planeInput)

    sketch = sketches.add(rearPlane)
    lines = sketch.sketchCurves.sketchLines

    # USB-C cutout (10mm × 5mm) centered, 15mm from bottom
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 1.5),  # 15mm from bottom
        adsk.core.Point3D.create(0.5, 0, 1.5 + 0.25)  # 10mm wide × 5mm tall
    )

    # Cut through wall
    profile = sketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(0.3)  # Cut toward -Y
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def add_side_panel_holes(comp):
    """Add slide switch cutout to left side panel"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Left panel is at X = -width/2 = -7.0cm
    planes = comp.constructionPlanes
    planeInput = planes.createInput()

    # Create YZ plane at X = -7.0
    offsetDist = adsk.core.ValueInput.createByReal(-7.0)
    planeInput.setByOffset(comp.yZConstructionPlane, offsetDist)
    leftPlane = planes.add(planeInput)

    sketch = sketches.add(leftPlane)
    lines = sketch.sketchCurves.sketchLines

    # Slide switch cutout (12mm × 6mm) centered, 30mm from bottom
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 3.0),  # Centered, 30mm from bottom
        adsk.core.Point3D.create(0.6, 0, 3.0 + 0.3)  # 12mm wide × 6mm tall
    )

    # Cut through wall
    profile = sketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(0.3)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def add_top_panel_holes(comp):
    """Add OLED window and button holes to top"""

    sketches = comp.sketches
    extrudes = comp.features.extrudeFeatures

    # Top is at Z = height = 6.0cm
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    offsetDist = adsk.core.ValueInput.createByReal(6.0)
    planeInput.setByOffset(comp.xYConstructionPlane, offsetDist)
    topPlane = planes.add(planeInput)

    sketch = sketches.add(topPlane)

    # OLED window (30mm × 15mm) forward from center
    lines = sketch.sketchCurves.sketchLines
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 2.0, 0),  # 20mm forward
        adsk.core.Point3D.create(1.5, 2.0 + 0.75, 0)  # 30mm × 15mm
    )

    # Cut OLED window
    profile = sketch.profiles.item(0)
    extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(-0.3)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # Button holes (4mm diameter, 12mm apart)
    buttonSketch = sketches.add(topPlane)
    circles = buttonSketch.sketchCurves.sketchCircles

    button_y = 0.5  # 5mm from center

    # Button A (left)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(-1.2, button_y, 0),
        0.2  # 4mm diameter
    )

    # Button B (center)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(0, button_y, 0),
        0.2
    )

    # Button C (right)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(1.2, button_y, 0),
        0.2
    )

    # Cut button holes
    for i in range(buttonSketch.profiles.count):
        profile = buttonSketch.profiles.item(i)
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(-0.3)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def stop(context):
    pass
