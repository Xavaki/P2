import subprocess
import os
import sys

allowed_formats = ['mp4', 'mov', 'avi', 'gif']
outdir = "output_files/"


def choose_file(message):

    print(message)
    i = 1
    files = {}
    for f in os.listdir():
        if f.split('.')[-1] in allowed_formats:
            print(f'{i} ····· {f}')
            files[i] = f
            i += 1
    choice = int(input())
    filename = files[choice]
    return filename


def n_seconds():

    filename = choose_file("Which file would you like to shorten?")

    print("How long would you like the output file to be [s]?")

    n = input()

    print("Choose output format:")
    print("1 ····· mp4 ")
    print("2 ····· mov ")
    print("3 ····· avi ")
    print("4 ····· gif ")

    choice = input()

    try:
        outformat = allowed_formats[int(choice) - 1]
        if outformat:
            outfile = f'{filename.split(".")[0]}_{n}.{outformat}'
        else:
            outfile = f'{filename.split(".")[0]}_{n}.{filename.split(".")[-1]}'
        subprocess.call(['ffmpeg', '-i', filename,
                         "-t", str(n), outfile])
    except Exception as e:
        print(f'Please enter a valid input {e}')


def yuv_histogram(filename="BBB_5.mp4", mode="view"):

    filename = choose_file(
        "Which file would you like to view the histogram of?")

    print("Choose mode:")
    print("1 ····· view")
    print("2 ····· save")
    modes = {1: "view", 2: "save"}

    choice = int(input())
    mode = modes[choice]

    try:
        if mode == "view":
            subprocess.call(
                ['ffplay', filename, '-vf', "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay"])
        elif mode == "save":
            outfile = f'{filename.split(".")[0]}_yuvhist.mp4'
            subprocess.call(['ffmpeg',
                             '-i',
                             filename,
                             '-vf',
                             "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay",
                             outdir + outfile])

    except Exception as e:
        print(f'Please enter a valid input {e}')


def resize_video():

    filename = choose_file("Which file would you like to resize?")

    resolutions = {
        1: [1280, 720],
        2: [640, 480],
        3: [360, 240],
        4: [160, 120],
    }

    print("What's your desired output resolution?")
    print("1 ····· 1280x720 (720p)")
    print("2 ····· 640x480 (480p)")
    print("3 ····· 360x240")
    print("4 ····· 160x120")

    try:

        option = int(input())

        res = resolutions[option]
        outfile = f'{filename.split(".")[0]}_{res[0]}x{res[1]}.mp4'
        # ffmpeg -i input.mp4 -filter:v scale=1280:720 -c:a copy output.mp4
        subprocess.call(['ffmpeg',
                         '-i',
                         filename,
                         "-filter:v",
                         f'scale={res[0]}:{res[1]}',
                         "-c:a",
                         "copy",
                         outdir + outfile])

    except Exception as e:
        print(f'Please enter a valid input {e}')


def audio_manip():

    filename = choose_file(
        "Which file would you like to manipulate the audio of?")

    print("Choose mode:")
    print("1 ····· mono")
    print("2 ····· codec")
    print("3 ····· both")
    modes = {1: "mono", 2: "codec", 3: "both"}

    choice = int(input())
    mode = modes[choice]

    try:
        if mode == "both":
            outfile = f'{filename.split(".")[0]}_mono_mp3.mp4'
            # ffmpeg -i BBB_5.mp4 -acodec mp3 -vcodec copy test_codec.mp4
            subprocess.call(['ffmpeg', '-i', filename, '-acodec',
                             'mp3', '-vcodec', 'copy', 'aux_file.mp4'])
            subprocess.call(['ffmpeg', '-i', 'aux_file.mp4',
                             '-ac', '1', outdir + outfile])
            subprocess.call(['rm', 'aux_file.mp4'])
        elif mode == "mono":
            outfile = f'{filename.split(".")[0]}_mono.mp4'
            subprocess.call(['ffmpeg', '-i', filename,
                             '-ac', '1', outdir + outfile])
        elif mode == "codec":
            outfile = f'{filename.split(".")[0]}_mp3.mp4'
            subprocess.call(['ffmpeg', '-i', filename, '-acodec',
                             'mp3', '-vcodec', 'copy', outdir + outfile])
    except Exception as e:
        print(f'Please enter a valid input {e}')


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Please call any of the following functions")
        print("··· n_seconds")
        print("··· yuv_histogram")
        print("··· resize_video")
        print("··· audio_manip")
        exit()

    elif len(sys.argv) == 2:
        function = sys.argv[1]
        if function == "n_seconds":
            print(f'Running {function}')
            n_seconds()
        elif function == "yuv_histogram":
            print(f'Running {function}')
            yuv_histogram()
        elif function == "resize_video":
            print(f'Running {function}')
            resize_video()
        elif function == "audio_manip":
            print(f'Running {function}')
            audio_manip()
        else:
            print("Function not in allowed list, please specify correct input")
            exit()

    else:
        print("Please call any of the following functions")
        print("··· n_seconds")
        print("··· yuv_histogram")
        print("··· resize_video")
        print("··· audio_manip")
        exit()
