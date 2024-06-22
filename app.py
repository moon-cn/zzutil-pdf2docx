from flask import Flask
from flask_cors import CORS
import os
import uuid

from flask import request, send_file

from pdf2docx import Converter

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'Hello, World！ PDF'


@app.route('/pdf_to_docx', methods=['POST'])
def pdf_to_docx():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    print("上传文件：", file.filename)

    filename = str(uuid.uuid4()).replace('-', '') + '.pdf'
    pdf_path = os.path.join("/tmp", filename)

    file.save(pdf_path)
    print("保存路径", pdf_path)

    # 创建输出文件夹
    output_file = os.path.join("/tmp", filename.split(".")[0] + ".docx")
    print("output_folder " + output_file)

    print("开始转换...")
    # pypandoc.convert_file(pdf_path, "docx", outputfile=output_file)
    cv = Converter(pdf_path)

    # 转换PDF到DOCX
    cv.convert(output_file, start=0, end=None)

    # 关闭转换器
    cv.close()
    print("转换完成")

    # 提供ZIP文件下载
    return send_file(output_file, as_attachment=True)


if __name__ == '__main__':
    print("app start...")
    port = os.getenv("PORT", default=5000)
    print("app port: " + str(port))
    app.run(debug=True, port=port, host='0.0.0.0')
