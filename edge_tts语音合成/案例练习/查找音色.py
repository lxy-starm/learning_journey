import os
import edge_tts
from edge_tts import VoicesManager
import asyncio

async def print_available_voices(language:str,gender:str)->None:
    """
    查找符合要求的音色
    :param language: 语言要求，如"zh"
    :param gender: 性别要求,如"Female"
    """
    voices=await VoicesManager.create()
    filtered_voice=voices.find(Language=language,Gender=gender)
    if(filtered_voice):
        for voice in filtered_voice:
            print(f"语言:{voice['Name']},性别：{voice['Gender']}")
    else:
        print("无符合筛选条件的音色")
async def main()->None:
    await print_available_voices('zh','Female')
if __name__=='__main__':
    asyncio.run(main())
