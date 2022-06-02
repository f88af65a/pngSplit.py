from PIL import Image

input = "./input.png"
output = "./output{}.png"
subImageCount = 0
XSHIFT = [0, 0, 1, -1]
YSHIFT = [1, -1, 0, 0]


def bfs(image: Image, visitMap, x, y) -> tuple:
    subImagePixel = list()
    visitList = [(x, y)]
    minPositoinX, minPositoinY = image.size[0], image.size[1]
    maxPositoinX, maxPositoinY = 0, 0
    while len(visitList) > 0:
        visitPixel = visitList[0]
        del visitList[0]
        if visitMap[visitPixel[0]][visitPixel[1]] == 1:
            continue
        visitMap[visitPixel[0]][visitPixel[1]] = 1
        subImagePixel.append(
             ((visitPixel[0], visitPixel[1]),
              image.getpixel((visitPixel[0], visitPixel[1])))
            )
        minPositoinX = min(minPositoinX, visitPixel[0])
        minPositoinY = min(minPositoinY, visitPixel[1])
        maxPositoinX = max(maxPositoinX, visitPixel[0])
        maxPositoinY = max(maxPositoinY, visitPixel[1])
        for i in range(4):
            positionX = visitPixel[0] + XSHIFT[i]
            positionY = visitPixel[1] + YSHIFT[i]
            if (
                positionX >= 0 and positionX < image.size[0]
                and positionY >= 0 and positionY < image.size[1]
                and visitMap[positionX][positionY] == 0
                and image.getpixel((positionX, positionY))[3] != 0
            ):
                visitList.append((positionX, positionY))
    return (subImagePixel,
            (minPositoinX, minPositoinY),
            (maxPositoinX - minPositoinX + 1, maxPositoinY - minPositoinY + 1)
            )


def createNewPng(subImagePixel, base, size):
    global subImageCount
    try:
        subImage = Image.new(mode="RGBA", size=size, color=(0, 0, 0, 0))
    except Exception as e:
        print(e)
        return
    for i in subImagePixel:
        subImage.putpixel((i[0][0] - base[0], i[0][1] - base[1]), i[1])
    subImage.save(output.format(subImageCount))
    subImage.close()
    subImageCount += 1


def pngSplit():
    try:
        image = Image.open(input).convert("RGBA")
    except Exception as e:
        print(e)
        return
    visitMap = []
    for i in range(image.size[0]):
        visitMap.append([0] * image.size[1])
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if visitMap[i][j] == 1:
                continue
            if image.getpixel((i, j))[3] != 0:
                createNewPng(*bfs(image, visitMap, i, j))
    image.close()


if __name__ == "__main__":
    pngSplit()
