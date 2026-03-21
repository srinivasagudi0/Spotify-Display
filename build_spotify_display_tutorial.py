import os, zipfile, math
try:
    import cadquery as cq
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cadquery', '-q'])
    import cadquery as cq

OUT_DIR = '/mnt/data/spotify_display_tutorial_assembled'
os.makedirs(OUT_DIR, exist_ok=True)

# Tutorial dimensions from the user-provided guide
OUTER_W = 70.0   # X
OUTER_H = 50.0   # Y
OUTER_D = 60.0   # Z/front-back depth per tutorial

CAVITY_W = 60.0  # 5 mm in from each side
CAVITY_H = 40.0  # 5 mm in from top/bottom
CAVITY_D = 58.0  # leaves 2 mm front wall
FRONT_WALL = OUTER_D - CAVITY_D
TOP_FILLET = 5.0

SCREEN_W = 43.5
SCREEN_H = 38.0
SCREEN_THICK = 5.0

# Standard 1u MX switch plate cutout / pitch used by kbplate-style layouts
SWITCH_CUT = 14.0
SWITCH_PITCH = 19.05
SWITCH_BODY_W = 14.0
SWITCH_BODY_H = 14.0
SWITCH_BODY_D = 18.0

# Wemos/Lolin C3 mini placeholder sized to fit the tutorial retainer
ESP_W = 25.4
ESP_H = 34.3
ESP_T = 1.6
USB_W = 10.0
USB_H = 5.0
USB_T = 7.0

WALL_T = 2.0
RET_DEPTH = 4.0
RET_LIP_H = 1.0
CLEAR = 0.8

LID_T = 2.0
LIP_T = 2.0
LIP_D = 4.0
LIP_OFFSET = 2.0

# Coordinate conventions:
# X = left/right, Y = up/down, Z = back(0) -> front(OUTER_D)


def build_case():
    case = cq.Workplane('XY').box(OUTER_W, OUTER_H, OUTER_D, centered=(True, True, False))

    # Bore from the back, leaving a 2 mm front wall exactly like the guide.
    case = case.faces('<Z').workplane(centerOption='CenterOfBoundBox').rect(CAVITY_W, CAVITY_H).cutBlind(CAVITY_D)

    # Screen opening on the front face.
    # Cutting deeper than the front wall opens the cavity but doesn't remove more once the cavity is reached.
    case = case.faces('>Z').workplane(centerOption='CenterOfBoundBox').rect(SCREEN_W, SCREEN_H).cutBlind(-(FRONT_WALL + 1.0))

    # Round the top perimeter edges.
    case = case.faces('>Y').edges().fillet(TOP_FILLET)

    # Three keyboard switch holes on the top face, centered like a 3-key macro row.
    for x in (-SWITCH_PITCH, 0.0, SWITCH_PITCH):
        case = case.faces('>Y').workplane(centerOption='CenterOfBoundBox').center(x, 0.0).rect(SWITCH_CUT, SWITCH_CUT).cutBlind(-WALL_T)

    # Internal ESP32 retainer against the back opening: left, right, bottom walls + top lip.
    cavity_bottom_y = -CAVITY_H / 2.0
    board_center_y = cavity_bottom_y + ESP_H / 2.0
    board_back_z = 1.2
    rail_center_z = board_back_z + RET_DEPTH / 2.0

    span_h = ESP_H + CLEAR
    span_w = ESP_W + CLEAR

    left_x = -(span_w / 2.0 + WALL_T / 2.0)
    right_x = (span_w / 2.0 + WALL_T / 2.0)
    bottom_y = cavity_bottom_y + WALL_T / 2.0
    top_lip_y = cavity_bottom_y + span_h + RET_LIP_H / 2.0

    left_rail = cq.Workplane('XY').box(WALL_T, span_h, RET_DEPTH, centered=(True, True, False)).translate((left_x, board_center_y, board_back_z))
    right_rail = cq.Workplane('XY').box(WALL_T, span_h, RET_DEPTH, centered=(True, True, False)).translate((right_x, board_center_y, board_back_z))
    bottom_rail = cq.Workplane('XY').box(span_w + 2 * WALL_T, WALL_T, RET_DEPTH, centered=(True, True, False)).translate((0.0, bottom_y, board_back_z))
    top_lip = cq.Workplane('XY').box(span_w, RET_LIP_H, 1.0, centered=(True, True, False)).translate((0.0, top_lip_y, board_back_z + RET_DEPTH - 1.0))

    return case.union(left_rail).union(right_rail).union(bottom_rail).union(top_lip)


def build_back_lid():
    # Main back plate
    lid = cq.Workplane('XY').box(OUTER_W, OUTER_H, LID_T, centered=(True, True, False)).translate((0.0, 0.0, -LID_T))

    # Three-sided internal lip (left, right, top) with 2 mm offset; bottom left open per tutorial.
    lip_inner_w = CAVITY_W - 2 * LIP_OFFSET
    lip_inner_h = CAVITY_H - 2 * LIP_OFFSET
    left_x = -(lip_inner_w / 2.0 + LIP_T / 2.0)
    right_x = (lip_inner_w / 2.0 + LIP_T / 2.0)
    top_y = (lip_inner_h / 2.0 + LIP_T / 2.0)

    left_lip = cq.Workplane('XY').box(LIP_T, lip_inner_h, LIP_D, centered=(True, True, False)).translate((left_x, 0.0, -LID_T - LIP_D))
    right_lip = cq.Workplane('XY').box(LIP_T, lip_inner_h, LIP_D, centered=(True, True, False)).translate((right_x, 0.0, -LID_T - LIP_D))
    top_lip = cq.Workplane('XY').box(lip_inner_w + 2 * LIP_T, LIP_T, LIP_D, centered=(True, True, False)).translate((0.0, top_y, -LID_T - LIP_D))

    lid = lid.union(left_lip).union(right_lip).union(top_lip)

    # USB opening for the ESP32 near the bottom center of the back.
    usb_center_y = -CAVITY_H / 2.0 + USB_H / 2.0 + 1.5
    usb_cut = cq.Workplane('XY').box(USB_W, USB_H, LID_T + LIP_D + 2.0, centered=(True, True, True)).translate((0.0, usb_center_y, -LID_T / 2.0 - LIP_D / 2.0))
    lid = lid.cut(usb_cut)
    return lid


def build_screen_placeholder():
    # Simple display block just behind the front cutout.
    display = cq.Workplane('XY').box(SCREEN_W - 0.6, SCREEN_H - 0.6, SCREEN_THICK, centered=(True, True, False))
    display = display.translate((0.0, 0.0, OUTER_D - SCREEN_THICK))
    return display


def build_esp_placeholder():
    # Board sits vertically near the back with bottom aligned to the cavity bottom.
    board = cq.Workplane('YZ').box(ESP_T, ESP_H, ESP_W, centered=(False, True, True))
    # Move so thickness is along Z, width along X, height along Y.
    board = board.rotate((0,0,0), (0,1,0), 90)
    # Now board dims are X=ESP_W, Y=ESP_H, Z=ESP_T. Rebuild simply to avoid ambiguity.
    board = cq.Workplane('XY').box(ESP_W, ESP_H, ESP_T, centered=(True, True, False))
    board_center_y = -CAVITY_H / 2.0 + ESP_H / 2.0
    board = board.translate((0.0, board_center_y, 1.3))

    usb = cq.Workplane('XY').box(USB_W, USB_H, USB_T, centered=(True, True, False)).translate((0.0, -CAVITY_H / 2.0 + USB_H / 2.0 + 1.5, -USB_T + 0.2))
    return board.union(usb)


def build_switches():
    # Simple three-switch placeholders inserted from the top.
    switches = []
    top_center_y = OUTER_H / 2.0 - SWITCH_BODY_D / 2.0
    z_center = OUTER_D / 2.0
    for x in (-SWITCH_PITCH, 0.0, SWITCH_PITCH):
        body = cq.Workplane('XY').box(SWITCH_BODY_W, SWITCH_BODY_D, SWITCH_BODY_W, centered=(True, True, True))
        body = body.translate((x, top_center_y, z_center))
        switches.append(body)
    out = switches[0]
    for s in switches[1:]:
        out = out.union(s)
    return out


case = build_case()
lid = build_back_lid()
screen = build_screen_placeholder()
esp = build_esp_placeholder()
switches = build_switches()

assy = cq.Assembly(name='spotify_display_tutorial_assembled')
assy.add(case, name='case')
assy.add(lid, name='back_lid')
assy.add(screen, name='screen_placeholder')
assy.add(esp, name='esp32_placeholder')
assy.add(switches, name='switch_placeholders')

step_path = os.path.join(OUT_DIR, 'spotify_display_tutorial_assembled.step')
source_path = os.path.join(OUT_DIR, 'build_spotify_display_tutorial.py')
zip_path = '/mnt/data/spotify_display_tutorial_assembled.zip'

assy.save(step_path)
with open(source_path, 'w', encoding='utf-8') as f:
    f.write(open(__file__, 'r', encoding='utf-8').read())

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(step_path, arcname='spotify_display_tutorial_assembled.step')
    z.write(source_path, arcname='build_spotify_display_tutorial.py')

print(step_path)
print(zip_path)
