#
# import ffmpeg
# import os
# import subprocess
#
# # 截取 input.mp4 从 10秒 到 20秒 的片段
# # 使用 -c copy 参数可以避免重新编码，实现快速无损截取[reference:12]
# file_dir =r"G:\\NV_VIDEO\\Wuthering Waves\\"
# filename = "Wuthering Waves 2026.07.08 - 17.14.54.12.DVR.mp4"
# ffmpeg_exe = r"F:\code\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"   # 示例路径
#
#
# input_path = os.path.join(file_dir, filename)
# output_path = os.path.join(file_dir, "2820.mp4")
#
# # 确保目录存在
# if not os.path.exists(file_dir):
#     print("目录不存在！")
#     exit()
#
# if not os.path.exists(input_path):
#     print("输入文件不存在！")
#     exit()
#
# # try:
# (
#     ffmpeg
#     .input(input_path, ss=2*60+6, to=5*60)
#     .output(output_path, c='copy')
#     .run(overwrite_output=True,cmd=ffmpeg_exe)   # 加上覆盖参数，避免询问
# )
#     print("成功！")
# except Exception as e:
#     print("ffmpeg 执行出错:", e)

a = 1.
if a == 1:
    print("ok")