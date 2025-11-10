import pygame
import sys
# 初始化 Pygame
pygame.init
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


# 主循环
while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:#点击“X”按钮，退出游戏
           pygame.quit()
           sys.exit()
   # 填充背景颜色
   # 刷新屏幕
   pygame.display.flip()
