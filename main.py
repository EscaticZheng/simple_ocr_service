from fastapi import FastAPI, Body
import uvicorn
from rapidocr_onnxruntime import RapidOCR
import base64
import numpy as np
from pydantic import BaseModel, Field
from PIL import Image
from io import BytesIO
from fastapi.responses import JSONResponse
app = FastAPI()
class OCRRequest(BaseModel):
    image_base64: str = Field(..., example="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/", description="图片的base64编码")
class OCRResponse(BaseModel):
    text: str = Field(description="从图片中提取的文字内容")
def base64_to_cv2_image(base64_string):
    # 解码Base64字符串为字节数据
    image_data = base64.b64decode(base64_string)
    
    image = Image.open(BytesIO(image_data))
    return image
def determine_orientation(coords):
    # 提取x和y坐标
    x_coords = [point[0] for point in coords]
    y_coords = [point[1] for point in coords]
    
    # 计算宽度和高度
    width = max(x_coords) - min(x_coords)
    height = max(y_coords) - min(y_coords)
    
    # 判断方向
    if width > height:
        return "horizontal"  # 横着的
    elif height > width:
        return "vertical"    # 竖着的
    else:
        return "square"      # 正方形
engine = RapidOCR()

@app.post('/ocr',response_model=OCRResponse)
async def ocr(request: OCRRequest):
    horizontal_count = 0
    vertical_count = 0
    square_count = 0
    url = request.image_base64
    # 如果URL是Base64编码的，解码为图像
    if url.startswith('data:image/png;base64,') or url.startswith('data:image/jpeg;base64,'):
        base64_string = url.split(',')[1]
        image = base64_to_cv2_image(base64_string)
        result, elapse = engine(image)
    else:
        result, elapse = engine(url)
    combined_string = ""
    if result is not None:
        for x in result:
            orientation = determine_orientation(x[0])
            if orientation == "horizontal":
                horizontal_count += 1
            elif orientation == "vertical":
                vertical_count += 1
            else:
                square_count += 1
            combined_string += x[1].strip().replace(" ", "")
    if vertical_count > horizontal_count:
        print(f"检测到竖行文字{vertical_count}行，大于横向文字{horizontal_count}行，将启动横向旋转")
        image = image.rotate(90, expand=True)
        combined_string = ""
        result, elapse = engine(image)
        if result is not None:
            for x in result:
                combined_string += x[1].strip().replace(" ", "")
    response = OCRResponse(text=combined_string)
    return JSONResponse(response.model_dump())

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
