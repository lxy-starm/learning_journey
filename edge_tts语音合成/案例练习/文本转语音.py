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
    async def generate_audio_async()->None:
        """异步生成语音"""
        communicate=edge_tts.Communicate(text=text,voice=voice)
        await communicate.save(output_file)
    asyncio.run(generate_audio_async())

#调用函数
#获取当前目录
current_path=os.getcwd()
print(current_path)
#判断目录是否存在
print(os.path.exists(current_path))
print(os.path.exists(current_path+"/test1"))
# output_file="edge_tts语音合成\output\starm.mp3"#使用上一级路径
# generate_audio("你好,Starm","zh-CN-XiaoyiNeural",output_file)