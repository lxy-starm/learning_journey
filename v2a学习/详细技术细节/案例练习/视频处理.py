import skvideo.io
import os
import numpy as np
import torch
import argparse
from PIL import Image
import clip
import glob
import math
#帧率类型转换函数
def covert(frame_rate):
    '''
    将帧率转化为浮点型。
    '''
    try:
        return np.float64(frame_rate)
    except ValueError:
        num,denom=frame_rate.split('/')
        return np.float64(num)/np.float64(denom)
#视频读取函数
def read_video(video,global_info):
    '''
    视频读取函数：
    video:输入视频路径
    global_info:全局信息

    return：[videodata, video_secs, frame_num, videoname]
    '''
    try:
        videoname=os.path.basename(video).split(".")[0]
        #读取视频数据。返回视频数据，格式：[帧数，高度，宽度，通道数]
        videodata=skvideo.io.vread(video)
        frame_num=videodata.shape[0]
        
        #读取视频元数据,提取帧率
        video_metadata=skvideo.io.ffprobe(video)
        frame_rate = video_metadata['video']['@avg_frame_rate']
        frame_rate=covert(frame_rate)
        
        #计算视频时长（秒数）
        video_secs=frame_num/frame_rate
        
        #如果全局信息中对于视频秒数有限制时，需要对比时长是否正确
        if global_info["videos_length"] is not None:  
            if global_info["videos_length"]!=video_secs:
                print(f"视频时长为{video_secs}，不符合要求，删除视频{videoname}")
                #os.remove(video)   
                return [None,None,None,videoname]
        print(f"读取视频{videoname}成功")
        return [videodata, video_secs, frame_num, videoname]
    except Exception as e:
        print(f"{e}Error while reading video:{video}")
        #os.remove(video)
        return [None,None,None,None]

def get_video_clip(video, model, global_info,device):
    '''
        video:准确来讲是Image对象形式的videodata，由read_video+转换类型得到。
        return:经model提取后的numpy格式特征，[帧数，512]
        '''
    with torch.no_grad():
        # 提取每一帧（并经过Clip中图像预处理pipeline后）拼接成[帧数，通道数，高度，宽度]
        images = torch.cat([global_info["preprocess"](frame).unsqueeze(0).to(device) for frame in video])

        # 使用clip中的图像编码器将图像编码为图像特征向量
        # 形状为[帧数，512]
        images_feature = model.encode_image(images)
        # 对特征进行L2归一化（让每个特征向量的模长 = 1），原因：
        # 1. CLIP 的输出本身就是设计用来做余弦相似度的，归一化可以使得特征向量的长度为1，便于后续的相似度计算。
        # 2.不同特征维度的数值范围可能不同，归一化可以消除这种差异，使得各个维度对相似度计算的贡献更加均衡。
        images_feature = images_feature / images_feature.norm(-1, keepdim=True)
        #.cpu().numpy()原因：
        #1.如果后面对于特征做处理时使用的numpy类的方法，则需转化为numpy()数组。（当然，也有tensor的等价处理方式。）
        #2.最终要存成.npy文件
        #3.如果张量在Gpu上，则直接.numpy()会报错，需先转移到cpu中。
        images_feature=images_feature.cpu().numpy()
        return images_feature

def handle_video(video,global_info):
    '''
    video:视频路径
    return:None。该函数对原始视频进行处理，最终保留提取后的.npy格式的视频特征在global_info["save_dir"]目录下
    '''
    try:
        #设置保存路径
        videodata,video_secs,frame_num,vedioname=read_video(video,global_info)
        save_dir=global_info["save_dir"]
        np_name=f"{save_dir}/{vedioname}.npy"

        if os.path.exists(np_name):
            return
        video_to_embed=[Image.fromarray(frame) for frame in videodata]
        images_feature=get_video_clip(video_to_embed,global_info["model"],global_info,global_info["device"])
        #对[帧数，512]形状的images_feature做时间维度平均池化，把多有帧的特征求平均
        #得到一个视频的全局“平均”特征
        images_feature=np.mean(images_feature,axis=0) #形状[512,]
        np.reshape(images_feature,[1,512])
        np.save(np_name,images_feature)
    except Exception as e:
        #任何异常都不中断流程，只打印，然后继续处理下个视频。
        print(f"{e}Error while handling video:{video}")

def parse_args():
    '''
    存储命令行参数，并以字典形式返回。
    '''
    #该参数解析器的描述文字是“collect CLIP”，会在输入"python scripts --help时显示"
    parser=argparse.ArgumentParser(description='collect CLIP')
    parser.add_argument("-batch_size",default=12,type=int,dest="batch_size",action="store")
    parser.add_argument("-save_dir", dest='save_dir', action='store', type=str, default="video_CLIP")
    parser.add_argument("-videos_dir", dest='videos_dir', action='store', type=str)
    parser.add_argument("-videos_length", dest='videos_length', action='store', type=float)  # 视频秒数限制
    #是否启用多进程
    parser.add_argument("-multi_thread", dest='multi_thread', action='store', type=bool,default=False)
    #parse_args()方法返回的是NameSpace对象，此处将其转化为字典类型
    v=vars(parser.parse_args())
    #print(v)
    return v

#这是 Python 脚本的"入口保护器"。当你在命令行直接运行这个文件时才会执行下面的代码；
#如果其他文件通过 import collect_video_CLIP 导入，则不会执行
if __name__=="__main__":
    #批处理提取特征脚本
    #对global_info进行赋值

    global_info=parse_args()
    global_info["device"] = torch.device("cuda" if torch.cuda.is_available() else 'cpu')
    print(f'device:{global_info["device"]}')

    # 扫描指定目录下的所有 .mp4 文件，得到一个路径列表 videos，同时保存视频总数 videos_num。
    global_info["videos"]=glob.glob(os.path.join(global_info["videos_dir"],"*.mp4"))
    global_info["videos_num"]=len(global_info["videos"])
    print(f'一共有{global_info["videos_num"]}个视频')

    #计算分多少个 batch 处理完所有视频。math.ceil 向上取整，确保不会漏掉最后一批（即使不满的那批）。
    global_info["batches_num"]=math.ceil(global_info["videos_num"]/float(global_info["batch_size"]))
    print(f'一共有{global_info["batches_num"]}个batch')

    with torch.no_grad():
        # CLIP_VERSION = "ViT-B/32"，即 CLIP 的视觉-文本模型
        # clip.load() 返回两个东西：模型本身和一个 torchvision transforms 的预处理 pipeline
        global_info["model"], global_info["preprocess"] = clip.load("ViT-B/32", global_info["device"])
        #依次遍历每个视频，利用CLIP模型提取其特征
        try:
            for i,video in enumerate(global_info["videos"]):
                handle_video(video,global_info)
                if i%50==0:
                    print(f'已处理{i+1}个视频')
            print(f'视频特征提取完成，保存在{global_info["save_dir"]}目录下')
        except Exception as e:
            print("视频特征提取失败")
