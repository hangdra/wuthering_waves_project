import ffmpeg
import os

file_dir = r"G:/NV_VIDEO/Wuthering Waves/"
filename = "Wuthering Waves 2026.07.08 - 16.13.04.09.DVR.mp4"
ffmpeg_exe = r"F:\code\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"  # 示例路径

f1 = file_dir + "2820.mp4"
f2 = file_dir + "char_info.mp4"
out_put_f3 = "2820_char_info.mp4"
# 输入两个不同的视频文件
video_files = [
    f1,
    f2,
]

# 1. 构建 concat demuxer 所需的文本内容（等价于 files.txt 里的内容）
# 注意：Windows 路径中的反斜杠需要转义，或者直接替换为正斜杠 "/"
file_list_content = "\n".join([f"file '{f.replace(os.sep, '/')}'" for f in video_files])

print(file_list_content.encode('utf-8'))
print("over")
# exit()
try:
    (
        ffmpeg
        .input('pipe:', format='concat', safe=0, protocol_whitelist='file,pipe')  # 从标准输入读取列表
        .output(file_dir + out_put_f3, c='copy')  # c='copy' 无损快速合并
        .run(
            overwrite_output=True,
            input=file_list_content.encode('utf-8')  # 关键：将文本内容直接传入 stdin
            , cmd=ffmpeg_exe
        )
    )
    print("合并成功！")
except ffmpeg.Error as e:
    print(e.stderr.decode())
