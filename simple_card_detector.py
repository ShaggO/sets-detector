from pathlib import Path
from itertools import combinations

import cv2


folder = Path('data/')
files = folder.glob('*.jpg')

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return () # or (0,0,0,0) ?
    return (x, y, w, h)

for file in files:
    frame = cv2.imread(str(file))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0.5)
    edge = cv2.Canny(blur, 0, 50, 3)
    canny = cv2.Canny(gray, 130, 255, 1)

    #contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0 if len(contours) == 2 else 1]
    
    rectangles = [cv2.boundingRect(c) for c in contours]
    rectangles = sorted([(*r, r[2]*r[3]) for r in rectangles], key=lambda x: x[-1], reverse=True)
    rect_out = [rectangles[0]]
    for rectangle in rectangles[1:]:
        if rectangle[-1] * 1.3 < rect_out[-1][-1]:
            break
        rect_out.append(rectangle)
    rectangles = rect_out
    org_len = len(rectangles)
    rectangles = list(set(rectangles))
    set_len = len(rectangles)
    # Remove overlapping rectangles:
    discard = []
    for r1, r2 in combinations(rectangles, 2):
        r1_r2 = intersection(r1, r2)
        if r1_r2:
            print("Overlapping. Discard smallest box")
            if r1[-1] < r2[-1]:
                discard.append(r1)
            else:
                discard.append(r2)
    discard = list(set(discard))
    rectangles = [r for r in rectangles if r not in discard]
    disc_len = len(rectangles)
    
    print(f'Rectangles {file}: {disc_len}')
    if disc_len != org_len:
        print(f'Duplicates removed: {org_len - set_len}')
        print(f'Overlaps removed: {set_len - disc_len}')
    
    for rectangle in rectangles:
        (x,y,w,h,a) = rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    out_file = '/'.join(list(file.parts[:-1]) + ['contour', file.name])
    
    cv2.imwrite(out_file, frame)