import json
import os
import subprocess
import sys
from os.path import expanduser
from find import find_path, find_sub

#bug  pl office 7 23    
def dmenu_chose(s: list) -> str:
    subs = ""
    for i in s:
        subs += i
        subs += "\n"
    a = os.popen("echo " + "\"" + subs[:-1] + "\"" + "|" + "dmenu " + d_args)
    return a.read()[:-1]

def print_info(path :str , sub:str="no sub" ) -> None:
    print()
    print("#####***************************************#####")
    print()
    print()
    print("playing: ",path)
    print()
    print("sub:",sub)
    print()
    print("options:",options)
    print()
    print()
    print("#####***************************************#####")
    print()

def play(name: str, season: int, episode: int):
    path = find_path(name, season, episode)
    if is_sub:
        sub_list = find_sub(name, season, episode)
        # print(sub_list)
        if sub_list:
            if len(sub_list) > 1:
                sub_list[0] = dmenu_chose(sub_list)
                if not sub_list[0]:
                    print_info(path)
                    subprocess.run([player,path,*options])
                    return
            print_info(path,sub_list[0])
            subprocess.run([player, path,*options, "--sub-file=" + sub_list[0]])
            return
    print_info(path)
    subprocess.run([player,path,*options])


def main():
    play(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))


if __name__ == "__main__":
    with open(sys.argv[0][:-7] + "conf.json") as f:
        data = json.load(f)
    conf = data["conf"]
    print(conf)
    video_dir = expanduser(conf["video_dir"])
    os.chdir(video_dir)
    player = conf["player"]
    options = conf["options"]
    if conf["is_full_screen"]:
       options.append("--fs")
    print(options)
    is_sub = conf["open_sub"]
    d_args = " ".join(conf["dmenu-options"])
    main()