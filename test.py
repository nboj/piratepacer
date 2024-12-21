from src.PiratePacer.client_handler import ClientHandler
import asyncio
from wizwalker.utils import XYZ, Keycode
import keyboard

def quest(client):
    offsets = [0x164, 0x1E4, 0x1D0, 0x4, 0x178, 0x1D8, 0xB74]
    base = client.process_mem.base_address+0x020E75CC
    current = base
    for offset in offsets:
        current = client.process_mem.read_int(current) + offset
    return current
def boat(client):
    offsets = [0x40, 0x40]
    base = client.process_mem.base_address+0x20CFD60
    current = base
    for offset in offsets:
        current = client.process_mem.read_int(current) + offset
    return current
def boat_speed(client):
    base = client.process_mem.base_address+0x020CFD70
    offsets = [0x50]
    current = base
    for offset in offsets:
        current = client.process_mem.read_int(current) + offset
    return current

async def main():
    pacer = ClientHandler()
    await pacer.wait_for_handle()
    pacer.get_ordered_clients()
    await pacer.activate_all_client_hooks()
    clients = pacer.get_clients()
    client = clients[0]
    quest_base = quest(client)

    try:
        await client.activate_all_hooks()
        boat_speed_hack = False
        while True:
            if keyboard.is_pressed('ctrl+q'):
                x = (client.process_mem.read_float(quest_base))
                y = (client.process_mem.read_float(quest_base+0x4))
                z = (client.process_mem.read_float(quest_base+0x8))
                print('quest tp')
                await client.teleport(XYZ(x, y, z))
            if keyboard.is_pressed('ctrl+f'):
                boat_base = boat(client)
                qx = (client.process_mem.read_float(quest_base))
                qy = (client.process_mem.read_float(quest_base+0x4))
                qz = (client.process_mem.read_float(quest_base+0x8))
                print('boat tp')
                client.process_mem.write_float(boat_base, qx)
                client.process_mem.write_float(boat_base+0x4, qy)
                client.process_mem.write_float(boat_base+0x8, qz)
            if keyboard.is_pressed('ctrl+s'):
                boat_speed_base = boat_speed(client)
                if boat_speed_hack:
                    boat_speed_hack = False
                    print('disabling boat speed')
                    client.process_mem.write_float(boat_speed_base, 0.) #xspeed
                    client.process_mem.write_float(boat_speed_base+0x4, 0.) #yspeed
                else:
                    boat_speed_hack = True
                    print('enabling boat speed')
                    client.process_mem.write_float(boat_speed_base+0x4, 10000.)
                    client.process_mem.write_float(boat_speed_base, 10000.) #xspeed
            if keyboard.is_pressed('ctrl+e'):
                break
            await asyncio.sleep(0.01)
        #await client.teleport(XYZ(111344.9375, 168380.796875, 13814.595703125))
    finally:
        await client.deactivate_all_hooks()
    print()

if __name__ == "__main__":
    #open_instance()
    asyncio.run(main())

