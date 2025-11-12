import pygame
import sys
import numpy as np
import math
# 初始化 Pygame
pygame.init
# 初始化字体系统
pygame.font.init()
# 设置窗口大小和标题
size = (670, 670)
screen = pygame.display.set_mode(size)
# 绘制棋盘底色
screen.fill((238, 154, 73))
# 设置黑色线条
line_color = [0,0,0]
# 绘制棋盘
for i in range(27,670,44):
	# 先画竖线
	if i==27 or i==670-27:# 边缘线稍微粗一些
		pygame.draw.line(screen,line_color,[i,27],[i,670-27],4)
	else:
		pygame.draw.line(screen,line_color,[i,27],[i,670-27],2)
	# 再画横线
	if i==27 or i==670-27:# 边缘线稍微粗一些
		pygame.draw.line(screen,line_color,[27,i],[670-27,i],4)
	else:
		pygame.draw.line(screen,line_color,[27,i],[670-27,i],2)
		
pygame.display.set_caption("Gomoku")

#存储所有着点中心位置
allpoints = []
for i in range(27,670,44):
	for j in range(27,670,44):
		allpoints.append((j,i))
#鼠标点击，寻找最近的可用着点,理论上鼠标点击周边方格有四个可能的着点，我们的目标是寻找最近的可下的着点
#target是鼠标点击的坐标，allpoints代表所有着点，availablepoints代表剩下可以下的着点
def find_closest_points(target:tuple, allpoints:list,availablepoints:list):
	target_x,target_y = target
	for i in range(27,670,44):
		if i >= target_x:
			x = i
			break
	for j in range(27,670,44):
		if j >= target_y:
			y = j
			break
	
	if x <= 27 and y > 27:  # 修改边界判断
		nearby_points = [(27, y-44), (27, y)]
	elif y <= 27 and x > 27:
		nearby_points = [(x-44, 27), (x, 27)]
	elif x <= 27 and y <= 27:
		nearby_points = [(27, 27)]
	else:
		nearby_points = [(x-44, y-44), (x, y-44), (x-44, y), (x, y)]

    #通过和啊availablepoints对比，找到最近的可下的着点
	possiblepoints = [point for point in nearby_points if point in availablepoints]
	min = 100
	if len(possiblepoints) > 0:
		for item in possiblepoints:
			item_min = math.sqrt((target_x-item[0])**2+(target_y-item[1])**2)
			if min >= item_min:
				min = item_min
				closest_point = item
		return closest_point
	else:
		return None

#定义赢条件的方程
def wincondition(mark_points: dict):
    if len(mark_points) > 0:
        for item in mark_points:  # item 就是坐标元组，如 (27, 27)
            x, y = item  # 直接解包，不要用 .key
            
            # 定义四个方向的五个点
            left2right = [(x-88, y), (x-44, y), (x, y), (x+44, y), (x+88, y)]
            top2down = [(x, y-88), (x, y-44), (x, y), (x, y+44), (x, y+88)]
            topleft2downright = [(x-88, y-88), (x-44, y-44), (x, y), (x+44, y+44), (x+88, y+88)]
            downright2topleft = [(x-88, y+88), (x-44, y+44), (x, y), (x+44, y-44), (x+88, y-88)]
            
            # 检查水平方向
            if all(tuple_item in mark_points for tuple_item in left2right):
                values = [mark_points[tuple_item] for tuple_item in left2right]
                if all(value == values[0] for value in values):
                    return f"The winner is {values[0]}"
            
            # 检查垂直方向
            elif all(tuple_item in mark_points for tuple_item in top2down):
                values = [mark_points[tuple_item] for tuple_item in top2down]
                if all(value == values[0] for value in values):
                    return f"The winner is {values[0]}"
            
            # 检查左上到右下对角线
            elif all(tuple_item in mark_points for tuple_item in topleft2downright):
                values = [mark_points[tuple_item] for tuple_item in topleft2downright]
                if all(value == values[0] for value in values):
                    return f"The winner is {values[0]}"
            
            # 检查左下到右上对角线
            elif all(tuple_item in mark_points for tuple_item in downright2topleft):
                values = [mark_points[tuple_item] for tuple_item in downright2topleft]
                if all(value == values[0] for value in values):
                    return f"The winner is {values[0]}"
    
    return None


# 主循环
# who决定是黑子还是白字下
who = 0
mark_points = {}
availablepoints = allpoints
print(availablepoints)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:#点击“X”按钮，退出游戏
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			#mouse_down_point是现在下的着点位置，其type是tuple，（x，y），若无可下的着点，则为None
			mouse_down_point = find_closest_points(pygame.mouse.get_pos(),allpoints,availablepoints)
            
			#保险措施
			if mouse_down_point is None:
				print("无着点可下")
			else:
				if who % 2 == 0:
					pygame.draw.circle(screen,(0,0,0),mouse_down_point,10)
					#mark_points代表已下过的所有着点，并使用dictionary标记黑子还是白子
					mark_points.update({mouse_down_point:'black'})
				else:
					pygame.draw.circle(screen,(255,255,255),mouse_down_point,10)
					mark_points.update({mouse_down_point:'white'})
				who += 1
				availablepoints.remove(mouse_down_point)
			if wincondition(mark_points) == "The winner is black":
				# 创建字体对象
				font = pygame.font.SysFont(None, 36) # None 表示使用默认字体，36 是字体大小
				# 渲染文本
				congratulation_surface = font.render("congratulation black!", True, (0, 0, 0)) # 白色字体，抗锯齿开启
				screen.blit(congratulation_surface, (200, 180))
				pygame.time.wait(100)
				restart_surface = font.render("Press R to restart!", True, (255, 0, 0))
				screen.blit(restart_surface, (400, 180))
			
		if event.type == pygame.K_r:
			print(mark_points)
			mark_points.clear()
			print(mark_points)
			availablepoints = allpoints
			who = 0
			pygame.set




   # 填充背景颜色
   # 刷新屏幕
	pygame.display.flip()
