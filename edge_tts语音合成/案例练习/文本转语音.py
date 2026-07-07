import edge_tts
import asyncio
import os
def generate_audio(text:str,voice:str,output_file:str)->None:#->None表示函数无返回值
    """
    根据输入的文本生成音频
    param text:输入文本
    param voice:使用的语音类型
    param output_file:输出的音频文件名
    """

    #异常处理，执行成功返回值为1，便于在if中判断.
    try:
        async def generate_audio_async()->int:
            """异步生成语音"""
            communicate=edge_tts.Communicate(text=text,voice=voice)
            await communicate.save(output_file)
        asyncio.run(generate_audio_async())
        return 1
    except Exception as e:
        print("生成音频失败")
        return 0
#调用函数
#获取当前目录
current_path=os.getcwd()
dirpath=os.path.dirname(current_path)
output_path=os.path.join(dirpath,"output")
os.makedirs(output_path,exist_ok=True)
output_file=os.path.join(output_path,"starm.mp3")

if(generate_audio("你好,Starm","zh-CN-XiaoyiNeural",output_file)):
    print(f"输出音频文件成功到{output_file}")