# pngSplit.py
 pngSplit.py是一个基于PIL的png图像切割工具，pngSplit.py通过bfs在原图中搜索连续的透明度不为0的像素，将搜索到的连续像素保存到新的文件中。

# 效果
 ![](zhenbucuo.png)

# 使用
 将图像改名为`input.png`放于`pngSplit.py`同一目录，运行`pngSplit.py`，切割后的图片将保存于同一目录下，命名格式为`output[第n-1个].png`  
 修改源码中的`input`与`output`可以更改默认名称和位置