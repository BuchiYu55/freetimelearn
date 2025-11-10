import pygame
import sys
# 初始化 Pygame
pygame.init()
# 设置窗口大小和标题
size = (640, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hello Pygame!")
# 主循环
while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
   # 填充背景颜色
   screen.fill((255, 255, 255))
   # 刷新屏幕
   pygame.display.flip()