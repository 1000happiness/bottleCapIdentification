class IdentifyModel:
    def __init__(self):
        pass

    def identify(self, inputPilImg):
        '''
        返回的list里面前两个元组表示瓶盖所在的长方体的四个点（逆时针排列）
        第三个元组表示瓶盖平面归一化的法向量(x,y,z)
        如果是正面朝上则为(0,0,1)
        如果正面朝下则为(0,0,-1)
        如果是侧面则为(1,0,0)
        具体的方向值按照结果确定
        '''
        return inputPilImg, [((50,50),(150,50),(150,150),(50, 150),(0,0,1))]