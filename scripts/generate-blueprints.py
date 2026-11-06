#!/usr/bin/env python3
"""Generate original industrial starter schematics (Python 3 + nbtlib 2.0.4).
No third-party structures or assets are copied. Coordinates stay stable on upgrades.
"""
from pathlib import Path
from io import BytesIO
import gzip, json, struct, zlib
import nbtlib as n
C, S, I, H, B = n.Compound, n.String, n.Int, n.Short, n.Byte
ROOT = Path(__file__).resolve().parents[1] / 'src/main/resources/blueprints/logisticcolonies/industrial'
def pos(x,y,z): return C({'x':I(x),'y':I(y),'z':I(z)})
def state(name, **properties):
    d=C({'Name':S(name)})
    if properties: d['Properties']=C({k:S(v) for k,v in properties.items()})
    return d

def generate(kind,tier):
    center=kind=='logistics_center'
    ship=kind in ['harbor','ship_fuel_station']
    fueling=kind in ['ship_fuel_station','rail_fuel_station']
    sx,sy,sz=(11+2*(tier-1),7,11) if center else (9+6*(tier-1),7,21)
    anchor=(3,1,3)
    blocks={}; palette=[state('minecraft:air')]; tes=[]; tags=[]
    def setblock(x,y,z,name,**props):
        st=state(name,**props)
        if st not in palette: palette.append(st)
        blocks[x,y,z]=palette.index(st)
    def tile(x,y,z,id,**fields):
        tes.append(C({'id':S(id),'x':H(x),'y':H(y),'z':H(z),**fields}))
    def tag(x,y,z,*names):
        tags.append(C({'tagPos':pos(x-anchor[0],y-anchor[1],z-anchor[2]),
                       'tagNameList':n.List[C]([C({'tagName':S(v)}) for v in names])}))
    # A paved yard with an open, well-lit dispatch shelter.
    for x in range(sx):
        for z in range(sz):
            setblock(x,0,z,'minecraft:stone_bricks')
    for x in (1,6):
        for z in (1,5):
            for y in range(1,5): setblock(x,y,z,'minecraft:stripped_spruce_log',axis='y')
    for x in range(1,7):
        for z in range(1,6): setblock(x,5,z,'minecraft:stone_brick_slab',type='bottom',waterlogged='false')
    setblock(4,4,3,'minecraft:lantern',hanging='true',waterlogged='false')
    setblock(*anchor,'logisticcolonies:'+kind,facing='south')
    if center:
        # More physical storage at each tier.
        for i in range(tier):
            x=3+2*i
            setblock(x,1,7,'minecraft:barrel',facing='up',open='false')
            tile(x,1,7,'minecraft:barrel')
        tag(3,1,7,'zentrallager')
        for x in range(1,sx-1):
            setblock(x,1,sz-2,'minecraft:stone_brick_wall',up='true',waterlogged='false',north='none',south='none',east='low',west='low')
    else:
        for slot in range(1,tier+1):
            x=3+6*(slot-1)
            setblock(x,1,7,'minecraft:barrel',facing='up',open='false')
            tile(x,1,7,'minecraft:barrel'); tag(x,1,7,'lager'+str(slot), *(['treibstofflager'+str(slot)] if fueling else []))
            parts=[(x,1,9,'controller'),(x,2,9,'left_top'),(x,2,10,'bridge')] if ship else [(x,1,9,'controller'),(x,2,9,'left_top'),(x+1,2,9,'bridge')]
            for xx,y,z,part in parts:
                setblock(xx,y,z,'littlelogistics:docking_station',facing='north' if ship else 'west',part=part,color='14')
            tile(x,1,9,'littlelogistics:docking_station')
            tag(x,1,9,(('tankschiff' if ship else 'tankgleis') if fueling else ('schiffsdock' if ship else 'gleis'))+str(slot),'dockstation'+str(slot))
            if ship:
                # Two-block deep water basin. Connect its seaward edge to navigable water.
                for xx in range(x-1,x+3):
                    for z in range(10,sz):
                        setblock(xx,0,z,'minecraft:water',level='0')
                        setblock(xx,1,z,'minecraft:water',level='0')
            else:
                # Independent straight tracks under the bridge, extended by the player.
                for z in range(8,sz):
                    setblock(x+1,1,z,'minecraft:rail',shape='north_south',waterlogged='false')
            setblock(x,1,6,'minecraft:lantern',hanging='false',waterlogged='false')
    data=C({'schematicName':S(f'{kind}{tier}'),
            'corner1':pos(-3,-1,-3),'corner2':pos(sx-4,sy-2,sz-4),
            'path':S(f'logistics/{kind}{tier}.blueprint'),'pack':S('LogisticColonies Industrial'),
            'posTagMap':n.List[C](tags)})
    tile(*anchor,'minecolonies:colonybuilding',type=S('logisticcolonies:'+kind),
         blueprintDataProvider=data,colony=I(0),mirror=B(0),version=I(0),
         pack=S('LogisticColonies Industrial'),path=S(f'logistics/{kind}{tier}.blueprint'))
    flat=[blocks.get((x,y,z),0) for y in range(sy) for z in range(sz) for x in range(sx)]
    packed=[]
    for i in range(0,len(flat),2):
        value=(flat[i]<<16)|(flat[i+1] if i+1<len(flat) else 0)
        packed.append(value if value<2**31 else value-2**32)
    root=C({'version':B(1),'size_x':H(sx),'size_y':H(sy),'size_z':H(sz),
        'palette':n.List[C](palette),'blocks':n.IntArray(packed),
        'tile_entities':n.List[C](tes),'entities':n.List[C]([]),
        'required_mods':n.List[S]([S(v) for v in ['minecraft','minecolonies','structurize','littlelogistics','logisticcolonies']]),
        'mcversion':I(3955),'name':S(f'{kind}{tier}'),
        'architects':n.List[S]([S('LogisticColonies')]),
        'optional_data':C({'structurize':C({'primary_offset':pos(*anchor)})})})
    stream=BytesIO(); n.File(root).write(stream)
    output=ROOT/'logistics'/f'{kind}{tier}.blueprint'; output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(gzip.compress(stream.getvalue(),mtime=0))
    return output

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'pack.json').write_text(json.dumps({'name':'LogisticColonies Industrial','icon':'icon.png','authors':['LogisticColonies'],
        'desc':'Hafen, Bahnhof, Logistikzentrum und Schiffs-/Zugtankstellen mit fünf Ausbaustufen. Strecken und Wasseranschluss selbst verbinden.',
        'mods':['minecolonies','structurize','littlelogistics','logisticcolonies'],
        'version':'2','pack-format':'1'},ensure_ascii=False,indent=2)+'\n')
    # Original small pack symbol: three colored freight containers on a rail base.
    def chunk(kind, data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    pixels=bytearray()
    for y in range(64):
        pixels.append(0)
        for x in range(64):
            color=(24,32,43,255)
            for i,c in enumerate([(54,130,186,255),(211,112,49,255),(218,180,53,255)]):
                if 7+i*17<=x<22+i*17 and 18<=y<44:
                    color=tuple(max(0,v-35) if x%4==0 else v for v in c[:3])+(255,)
            if 9<=x<56 and 47<=y<51: color=(184,191,196,255)
            if y in (53,54) and 9<=x<56 and x%9<4: color=(120,83,57,255)
            pixels.extend(color)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,64,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(bytes(pixels)))+chunk(b'IEND',b'')
    (ROOT/'icon.png').write_bytes(png)
    for kind in ['harbor','railway_station','logistics_center','ship_fuel_station','rail_fuel_station']:
        for tier in range(1,6): print(generate(kind,tier))
if __name__=='__main__': main()
