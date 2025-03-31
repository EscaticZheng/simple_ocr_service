# FastAPI-OCR-Service

## 项目简介
本项目是一个基于 **FastAPI** 和 **RapidOCR** 的轻量级 OCR（光学字符识别）服务应用。通过接收图片的 Base64 编码，提取图片中的文字内容并返回结果。项目支持对图片方向的自动检测与处理，能够优化文字提取效果。

## 功能特性
- **Base64 图像输入支持**：支持直接上传 Base64 编码的图片（JPEG/PNG 格式）。
- **文字提取**：基于 RapidOCR 实现高效的文字识别。
- **自动方向检测**：通过检测文字区域的宽高比，判断文字方向（横排、竖排或正方形），并对竖排文字图片自动旋转处理。
- **高性能**：使用 FastAPI 提供快速响应的 RESTful API。

## 使用方法

### 启动服务
运行以下命令在8000端口上启动服务：
```bash
python main.py
```  
### 调用 OCR 接口
通过 /ocr POST 接口上传图片并提取文字。    
{  
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/..."  
}  

### 依赖环境
Python 3.8+  
FastAPI  
RapidOCR  
Pillow  
NumPy  
Uvicorn  
Pydantic  
