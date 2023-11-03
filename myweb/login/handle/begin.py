from urllib import request
import cv2
import numpy as np
from django.shortcuts import render,HttpResponse
import joblib
import torch
import torch.nn as nn
from torchvision import models


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")# 检测设备
dic1 = {0: "其他", 1:"寻常型银屑病-轻度", 2:"寻常型银屑病-中重度" }
dic2 = {0: "您患有寻常型银屑病的风险较低。如您感到身体不适，建议您及时前往医院进行诊断。我们衷心祝愿您早日康复！",
        1: "您无需为病情过分焦虑，轻度寻常型银屑病彻底治愈、不再次发作的几率较高。建议您尽快前往皮肤科门诊就医，以免病情发展，错过最佳治疗时机。一般而言，轻度寻常型银屑病的治疗以外用药物为主，卤米松、达力士、得肤宝、他克莫司等等外用都是安全有效的，还要注意多润肤、避免感冒。如果皮疹不消退或者加重，需要根据具体情况，尝试紫外线光疗和口服药物。我们衷心祝愿您早日康复！",
        2: "您不要有过多心理负担，保持心情舒畅和健康的生活方式十分有助于病情的缓解。请您务必尽快前往皮肤科门诊就医，以免病情迅速扩散、恶化。对于中重度银屑病患者，除局部用药外，往往需结合系统治疗。目前最常用的治疗方法是药物治疗，使用维甲酸类药物如阿维A或免疫抑制剂如甲氨蝶呤、雷公藤多甙、环孢素A和麦考酚酸酯等。紫外线光疗以及近年研发的生物制剂也有良好的疗效。我们衷心祝愿您早日康复！"}
    

def fileToCv2Img(file):#接受django的文件对象，返回cv2使用的frame
    byteimg=bytes()
    for i in file.chunks():
        byteimg+=i
    
    return cv2.imdecode(np.fromstring(byteimg,"uint8"), 1)


def ToBatch(sample):#数据转换
        image, quest = sample
        image = cv2.resize(image, (224, 224))
        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        image = image.transpose((2, 0, 1)).copy()
        return torch.from_numpy(image).float().to(device).unsqueeze(0), torch.Tensor(quest).to(device).unsqueeze(0)

class JointNet(nn.Module):# 模型
    def __init__(self,feature_extract=True, num_classes=3, hidden1=2048, hidden2=512, dropout=0.3):
        super(JointNet, self).__init__()
        model = models.vgg16(pretrained=True)
        self.features = model.features
        set_parameter_requires_grad(self.features, feature_extract)#固定特征提取层参数
        self.avgpool=model.avgpool
        self.hidden = nn.Sequential(
            nn.Linear(512*7*7 , hidden1),
            nn.ReLU(),
            nn.Linear(hidden1 , hidden2),
            nn.ReLU(),
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden2+37, hidden2+37),
            nn.Dropout(p=dropout),
            nn.ReLU(),
            nn.Linear(hidden2+37, num_classes)
        )
        
    def forward(self, x):
        img, quest = x
        img = self.features(img)
        img = self.avgpool(img)
        img = img.view(img.size(0), 512*7*7)
        img = self.hidden(img)
        joint = torch.cat([img, quest],1)
        out=self.classifier(joint)
        return out
    
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False




def start(answers,image):
    # 加载模型
    model = JointNet(feature_extract=False).to(device)
    if torch.cuda.is_available():
        model.load_state_dict(torch.load("login/handle/jointmodel.pth"))
    else:
        model.load_state_dict(torch.load("login/handle/jointmodel.pth", map_location='cpu'))

    # 问卷数据归一化
    mm = joblib.load('login/handle/minmaxscaler.joblib')
    quest = mm.transform(np.array(list(map(int, answers))).reshape(1, -1))[0]

    #接受django的文件对象，返回cv2使用的frame
    img = fileToCv2Img(image)

    # 把数据转换成batch
    mydata = ToBatch((img, quest))

    # 预测患病类型
    model.eval()
    with torch.no_grad():
        outputs = model(mydata)
        _, predicted = torch.max(outputs.data, 1)
    
    # 把输出的预测结果转化为文字，返回一个字典
    value = {
    'result': dic1[predicted.item()],
    'suggest': dic2[predicted.item()]
    }
    return value

