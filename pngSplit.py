from PIL import Image

input = "./input.png"
output = "./output{}.png"
subImageCount = 0
XSHIFT = [0, 0, 1, -1]
YSHIFT = [1, -1, 0, 0]


def findSubImagePixel(image: Image, visitMap, x, y) -> tuple:
    subImagePixels = list()
    needVisitPos = [(x, y)]
    minPosX, minPosY = image.size[0], image.size[1]
    maxPosX, maxPosY = 0, 0
    while len(needVisitPos) > 0:
        visitPos = needVisitPos[0]
        del needVisitPos[0]
        if visitMap[visitPos[0]][visitPos[1]] == 1:
            continue
        visitMap[visitPos[0]][visitPos[1]] = 1
        subImagePixels.append(
             ((visitPos[0], visitPos[1]),
              image.getpixel((visitPos[0], visitPos[1])))
            )
        minPosX = min(minPosX, visitPos[0])
        minPosY = min(minPosY, visitPos[1])
        maxPosX = max(maxPosX, visitPos[0])
        maxPosY = max(maxPosY, visitPos[1])
        for i in range(4):
            adjoinPosX = visitPos[0] + XSHIFT[i]
            adjoinPosY = visitPos[1] + YSHIFT[i]
            if (
                adjoinPosX >= 0 and adjoinPosX < image.size[0]
                and adjoinPosY >= 0 and adjoinPosY < image.size[1]
                and visitMap[adjoinPosX][adjoinPosY] == 0
                and image.getpixel((adjoinPosX, adjoinPosY))[3] != 0
            ):
                needVisitPos.append((adjoinPosX, adjoinPosY))
    return (subImagePixels,
            (minPosX, minPosY),
            (maxPosX - minPosX + 1, maxPosY - minPosY + 1)
            )


def createSubImage(subImagePixel, base, size):
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
                createSubImage(*findSubImagePixel(image, visitMap, i, j))
    image.close()


if __name__ == "__main__":
    pngSplit()
