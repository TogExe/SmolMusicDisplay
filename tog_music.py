import dbus
import os
import subprocess
import time

time.sleep(2)
#Downloads/1_20250606_175728_0000.png

def get_player():
    bus = dbus.SessionBus()
    # Getting the list of all registered MPRIS players
    mpris_players = bus.list_names()
    mpris_players = [player for player in mpris_players if player.startswith('org.mpris.MediaPlayer2.')]

    if not mpris_players:
        print("No MPRIS players found.")
        return None

    # Using the first MPRIS player found
    player = dbus.Interface(bus.get_object(mpris_players[0], '/org/mpris/MediaPlayer2'), 'org.mpris.MediaPlayer2.Player')
    return player, bus, mpris_players[0]

def get_img(size,wich):
    command = f"pixterm -s 2 -tc {size} -tr {size} '{wich}'"

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output = result.stdout

    if result.stderr:
        print("Error:", result.stderr)

    output_lines = output.splitlines()

    #for y in output_lines:
    #    print(f"{y}")
    return (output_lines)

def get_current_track_info(player, bus, player_name):
    # Getting the properties interface
    properties = dbus.Interface(bus.get_object(player_name, '/org/mpris/MediaPlayer2'), 'org.freedesktop.DBus.Properties')

    # Getting the Metadata property
    metadata = properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    # Extracting track information
    track_info = {
        'title': metadata.get('xesam:title', 'Unknown Title'),
        'artist': metadata.get('xesam:artist', ['Unknown Artist'])[0],
        'album': metadata.get('xesam:album', 'Unknown Album'),
        #'track_number': metadata.get('xesam:trackNumber', 'Unknown Track Number'),
        'length': metadata.get('mpris:length', 0) / 1000000  # Convert microseconds to seconds
    }

    return track_info

def get_album_art_url(player, bus, player_name):
    properties = dbus.Interface(bus.get_object(player_name, '/org/mpris/MediaPlayer2'), 'org.freedesktop.DBus.Properties')
    metadata = properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    # Getting the artwork URL if available
    art_url = metadata.get('mpris:artUrl', '')

    # Handling file URLs (e.g., "file:///home/user/.cache/...") and HTTP(S)
    if art_url.startswith("file://"):
        # Converting to local path
        import urllib.parse
        art_path = urllib.parse.unquote(art_url[7:])
        return art_path
    elif art_url.startswith("http://") or art_url.startswith("https://"):
        #os.system(f"pixterm -s 2 -tc 43 -tr 43 '{art_url}'")
        #txt= f"pixterm -s 2 -tc 43 -tr 43 '{art_url}'"
        #print(art_url)
        return art_url
    else:
        return None

def control_player(player, command):
    if command == 'play':
        player.Play()
    elif command == 'pause':
        player.Pause()
    elif command == 'play_pause':
        player.PlayPause()
    elif command == 'next':
        player.Next()
    elif command == 'previous':
        player.Previous()
    elif command == 'stop':
        player.Stop()
    elif command == 'info':
        return 'info'
    elif command == 'st':
        return 'stand'
    else:
        print("Unknown command")

def main():
    result = get_player()
    if not result:
        return

    player, bus, player_name = result

    print("Available commands: play, pause, play_pause, next, previous, stop, info, exit")
    while True:
        command = input("Enter command: ").strip().lower()
        if command == 'exit':
            break
        if control_player(player, command) == 'info':
            track_info = get_current_track_info(player, bus, player_name)
            print("Current Track Info:")
            print(get_album_art_url(player,bus,player_name))
            for key, value in track_info.items():
                print(f"{key}: {value}")

        elif control_player(player, command) == 'stand':
            fl = True
            while True:
                time.sleep(1)
                if fl or track_info.items != get_current_track_info(player, bus, player_name).items:
                    if fl: fl =False
                    track_info = get_current_track_info(player, bus, player_name)
                    #print("Current Track Info:")
                    #Downloads/1_20250606_175728_0000.png
                    image =get_img(37,get_album_art_url(player,bus,player_name))
                    #image =get_img(37,"Downloads/1_20250606_175728_0000.png")
                    #for row in image:
                    #    print(f"{row}")
                    text = []
                    i = 0
                    #print(image)
                    l = 0
                    for key, value in track_info.items():
                        #print(f"{key}: {value}")
                        text.append(f"{key} : {value} ")
                        l+=1
                    os.system(f"clear")
                    print()
                    print
                    print("   ╭━━━━━━━━━━━━━━━━━━━━━━━╮")
                    print("   │ Tog's music display : │")
                    print("   ╰━━━━━━━━━━━━━━━━━━━━━━━╯")
                    #━━━━━━━━━━
                    print("   ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮")
                    for row in image:
                        if (i%2==0)and i>2 and len(text)>i/2-2:
                            print(f"   │ {row} │ ▢ {text[int(i/2-2)]}")
                            pass
                        else :
                            print(f"   │ {row} │ ")
                            pass
                        i+=1
                    print("   ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯")

if __name__ == "__main__":
    main()

#╭━━━━╮
#│test│  
#╰━━━━╯
