"""Make the same-mean lottery illustration and its offline companion."""

import math
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


HERE=Path(__file__).resolve().parent
W,H=704,835
BG,PANEL,EDGE="#101b32","#162640","#3b5577"
TEXT,MUTED="#f7faff","#c2cee0"
AMBER, MINT, BLUE="#ffd086","#6aead7","#adbffb"
horizontal=((-1,0,.5),(1,0,.5))
vertical=((0,-1,.5),(0,1,.5))
mixture=tuple((x,y,.25) for x,y,_ in horizontal+vertical)
diagonal=((-1,1,.5),(1,-1,.5))
cases=(horizontal,vertical,mixture,diagonal)


def label(draw,xy,s,size,color=TEXT,anchor="lt"):
    draw.text(xy,s,font=ImageFont.load_default(size=size),fill=color,anchor=anchor)


def projection(angle,x,y,z=0):
    width=x*math.cos(angle)-y*math.sin(angle)
    depth=x*math.sin(angle)+y*math.cos(angle)
    return 352+139*width,429+55*depth-178*z


def plot(draw, angle, case):
    def xy(x,y,z=0):
        return projection(angle,x,y,z)
    border=[xy(-1.22,-1.22),xy(1.22,-1.22),xy(1.22,1.22),xy(-1.22,1.22)]
    draw.polygon(border,fill="#1d3150",outline=EDGE,width=2)
    for line in (-1,0,1):
        draw.line((xy(-1.22,line),xy(1.22,line)),fill="#415c7d",width=2 if line==0 else 1)
        draw.line((xy(line,-1.22),xy(line,1.22)),fill="#415c7d",width=2 if line==0 else 1)
    cx,cy=xy(0,0)
    draw.polygon([(cx-7,cy),(cx,cy-6),(cx+7,cy),(cx,cy+6)],fill=TEXT)
    points=sorted(case,key=lambda p:xy(*p[:2])[1])
    for x,y,m in points:
        color=AMBER if y==0 else BLUE if x==0 else MINT
        px,py=xy(x,y)
        qx,qy=xy(x,y,m)
        draw.line((px,py,qx,qy),fill=color,width=9)
        draw.ellipse((px-5,py-4,px+5,py+4),fill=color)
        draw.ellipse((qx-8,qy-8,qx+8,qy+8),fill=color,outline="#152743",width=2)


def frame(angle, index):
    case=cases[index]
    assert sum(m for x,y,m in case)==1
    assert sum(x*m for x,y,m in case)==sum(y*m for x,y,m in case)==0
    scene_names=("Horizontal chain","Vertical chain","Equal mixture","Antidiagonal pair")
    lines=(
        ("Two comparable outcomes.","Indifferent to the sure mean."),
        ("Two comparable outcomes.","Indifferent to the same sure mean."),
        ("Four atoms, each of mass 1/4.","Their mixture stays in the same class."),
        ("Two incomparable outcomes.","Equal means alone give no comparison."),
    )
    image=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(image)
    label(d,(36,38),"FINITE-SUPPORT LOTTERIES",24,MINT)
    label(d,(34,83),"When mixtures tie",56)
    label(d,(36,160),"Each lottery has mean (0, 0).",30,MUTED)
    d.rounded_rectangle((32,218,672,573),21,fill=PANEL,outline=EDGE,width=2)
    label(d,(55,241),"HEIGHT SHOWS PROBABILITY",23,MUTED)
    plot(d,angle,case)
    d.rounded_rectangle((32,598,672,805),21,fill=PANEL,outline=EDGE,width=2)
    label(d,(55,619),scene_names[index],36,MINT if index<3 else AMBER)
    label(d,(55,688),lines[index][0],29,TEXT)
    label(d,(55,738),lines[index][1],26,MUTED)
    return image.convert("P",palette=Image.Palette.ADAPTIVE,colors=64)


def main():
    total=84
    frames=[frame(.6+(.34*math.sin(2*math.pi*i/total)),i//21) for i in range(total)]
    frames[0].save(HERE/"lottery-mixtures.gif",save_all=True,append_images=frames[1:],
                   loop=0,duration=190,optimize=True)
    with ZipFile(HERE/"lottery-mixtures-explorer.zip","w") as archive:
        for name in ("README.md","index.html"):
            info=ZipInfo(name,(1980,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            archive.writestr(info,(HERE/name).read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__=="__main__":
    main()
