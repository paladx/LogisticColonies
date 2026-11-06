#!/usr/bin/env python3
"""Validate dimensions, anchors, complete station multiblocks and positioned tags."""
from pathlib import Path
import nbtlib as n
import json
ROOT=Path(__file__).resolve().parents[1]/'src/main/resources/blueprints/logisticcolonies/industrial/logistics'
pack=json.loads((ROOT.parent/'pack.json').read_text())
assert all(key in pack for key in ['name','icon','authors','desc','mods','version','pack-format'])
assert (ROOT.parent/pack['icon']).read_bytes().startswith(b'\x89PNG')
count=0
for kind in ['harbor','railway_station','logistics_center','ship_fuel_station','rail_fuel_station']:
    previous_docks=[]
    for tier in range(1,6):
        f=n.load(ROOT/f'{kind}{tier}.blueprint',gzipped=True)
        sx,sy,sz=(int(f['size_'+a]) for a in 'xyz')
        values=[]
        for v in f['blocks']:
            v=int(v)&0xffffffff; values.extend([v>>16,v&65535])
        assert len(values) in (sx*sy*sz,sx*sy*sz+1)
        values=values[:sx*sy*sz]
        assert max(values)<len(f['palette'])
        def state(x,y,z): return f['palette'][values[(y*sz+z)*sx+x]]
        anchor=f['optional_data']['structurize']['primary_offset']
        ax,ay,az=(int(anchor[a]) for a in 'xyz')
        assert str(state(ax,ay,az)['Name'])=='logisticcolonies:'+kind
        hut=[te for te in f['tile_entities'] if 'blueprintDataProvider' in te]
        assert len(hut)==1
        provider=hut[0]['blueprintDataProvider']; tags={}
        for entry in provider['posTagMap']:
            xyz=tuple(int(entry['tagPos'][a])+int(anchor[a]) for a in 'xyz')
            assert all(0<=v<limit for v,limit in zip(xyz,[sx,sy,sz]))
            for label in entry['tagNameList']: tags[str(label['tagName'])]=xyz
        if kind=='logistics_center':
            assert str(state(*tags['zentrallager'])['Name'])=='minecraft:barrel'
        else:
            ship=kind in ['harbor','ship_fuel_station']
            prefix=('tankschiff' if ship else 'tankgleis') if 'fuel_station' in kind else ('schiffsdock' if ship else 'gleis')
            docks=[]
            for slot in range(1,tier+1):
                xyz=tags[prefix+str(slot)]; docks.append(xyz)
                assert xyz==tags['dockstation'+str(slot)]
                assert str(state(*xyz)['Name'])=='littlelogistics:docking_station'
                assert str(state(*xyz)['Properties']['part'])=='controller'
                x,y,z=xyz
                assert str(state(x,y+1,z)['Properties']['part'])=='left_top'
                bridge=(x,y+1,z+1) if ship else (x+1,y+1,z)
                assert str(state(*bridge)['Properties']['part'])=='bridge'
                assert str(state(*tags['lager'+str(slot)])['Name'])=='minecraft:barrel'
            assert docks[:len(previous_docks)]==previous_docks, 'Upgrade moved an existing dock'
            previous_docks=docks
        count+=1
print(f'{count} blueprint structures and all five upgrade sequences passed')
