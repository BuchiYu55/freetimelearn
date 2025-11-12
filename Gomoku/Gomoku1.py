import pygame
import sys
import math

class Gomoku:
    def __init__(self):
        self.who = 'black'
        self.mark_points = {}
        # 初始化 Pygame
        pygame.init()
        # 初始化字体系统
        pygame.font.init()
        # 设置窗口大小和标题
        self.size = (670, 670)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Gomoku")
        self.availablepoints = self.allpoints()  # 调用方法，不是引用
        
        # 绘制棋盘
        self.draw_board()
    
    def draw_board(self):
        """绘制棋盘"""
        # 绘制棋盘底色
        self.screen.fill((238, 154, 73))
        # 设置黑色线条
        line_color = [0, 0, 0]
        # 绘制棋盘
        for i in range(27, 670, 44):
            # 先画竖线
            if i == 27 or i == 670 - 27:
                pygame.draw.line(self.screen, line_color, [i, 27], [i, 670 - 27], 4)
            else:
                pygame.draw.line(self.screen, line_color, [i, 27], [i, 670 - 27], 2)
            # 再画横线
            if i == 27 or i == 670 - 27:
                pygame.draw.line(self.screen, line_color, [27, i], [670 - 27, i], 4)
            else:
                pygame.draw.line(self.screen, line_color, [27, i], [670 - 27, i], 2)
        
        pygame.display.flip()

    def allpoints(self):
        """生成所有着点"""
        allpoints = []
        for i in range(27, 670, 44):
            for j in range(27, 670, 44):
                allpoints.append((j, i))
        return allpoints
    
    def find_closest_points(self, target: tuple):
        """找到最近的可用着点"""
        target_x, target_y = target
        
        # 找到最接近的x坐标
        x = None
        for i in range(27, 670, 44):
            if i >= target_x:
                x = i
                break
        if x is None:
            x = 27 + ((670 - 27) // 44) * 44
        
        # 找到最接近的y坐标
        y = None
        for j in range(27, 670, 44):
            if j >= target_y:
                y = j
                break
        if y is None:
            y = 27 + ((670 - 27) // 44) * 44
        
        # 确定附近的点
        if x <= 27 and y > 27:
            nearby_points = [(27, y - 44), (27, y)]
        elif y <= 27 and x > 27:
            nearby_points = [(x - 44, 27), (x, 27)]
        elif x <= 27 and y <= 27:
            nearby_points = [(27, 27)]
        else:
            nearby_points = [(x - 44, y - 44), (x, y - 44), (x - 44, y), (x, y)]
        
        # 找到可用的点
        possiblepoints = [point for point in nearby_points if point in self.availablepoints]
        min_distance = float('inf')
        closest_point = None
        
        if possiblepoints:  # 简化判断
            for item in possiblepoints:
                item_distance = math.sqrt((target_x - item[0]) ** 2 + (target_y - item[1]) ** 2)
                if item_distance < min_distance:
                    min_distance = item_distance
                    closest_point = item
            return closest_point
        else:
            return None
        
    def wincondition(self):
        """检查获胜条件"""
        if len(self.mark_points) < 5:
            return None
            
        for (x, y), color in self.mark_points.items():  # 同时遍历坐标和颜色
            # 四个方向向量
            directions = [
                (44, 0),   # 水平
                (0, 44),   # 垂直  
                (44, 44),  # 对角线
                (44, -44)  # 反对角线
            ]
            
            for dx, dy in directions:
                count = 1  # 当前棋子
                
                # 正向检查
                temp_x, temp_y = x + dx, y + dy
                while (temp_x, temp_y) in self.mark_points and self.mark_points[(temp_x, temp_y)] == color:
                    count += 1
                    temp_x += dx
                    temp_y += dy
                
                # 反向检查
                temp_x, temp_y = x - dx, y - dy
                while (temp_x, temp_y) in self.mark_points and self.mark_points[(temp_x, temp_y)] == color:
                    count += 1
                    temp_x -= dx
                    temp_y -= dy
                
                if count >= 5:
                    return color  # 直接返回获胜颜色
        
        return None
    
    def draw_game_over(self, winner):
        """绘制游戏结束界面"""
        # 创建字体对象
        font = pygame.font.SysFont(None, 48)
        
        # 渲染文本
        congratulation_text = f"恭喜 {winner} 获胜!"
        congratulation_surface = font.render(congratulation_text, True, (255, 0, 0))
        restart_surface = font.render("按 R 键重新开始", True, (0, 0, 255))
        
        # 获取文本矩形并居中
        congrat_rect = congratulation_surface.get_rect(center=(self.size[0]//2, self.size[1]//2 - 30))
        restart_rect = restart_surface.get_rect(center=(self.size[0]//2, self.size[1]//2 + 30))
        
        # 绘制半透明背景
        overlay = pygame.Surface(self.size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))  # 半透明白色
        self.screen.blit(overlay, (0, 0))
        
        # 绘制文本
        self.screen.blit(congratulation_surface, congrat_rect)
        self.screen.blit(restart_surface, restart_rect)
        
        pygame.display.flip()
    
    def reset_game(self):
        """重置游戏"""
        self.mark_points.clear()
        self.availablepoints = self.allpoints()  # 重新生成可用点
        self.who = 'black'
        self.draw_board()  # 重绘棋盘
        
        # 重绘之前下的棋子（实际上清空了）
        for pos, color in self.mark_points.items():
            stone_color = (0, 0, 0) if color == "black" else (255, 255, 255)
            pygame.draw.circle(self.screen, stone_color, pos, 10)
            if color == "white":
                pygame.draw.circle(self.screen, (0, 0, 0), pos, 10, 2)  # 白子加黑边
    
    def run(self):
        """运行游戏主循环"""
        clock = pygame.time.Clock()
        game_over = False
        winner = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:  # 键盘按下事件
                    if event.key == pygame.K_r and game_over:  # 按R键且游戏结束
                        game_over = False
                        winner = None
                        self.reset_game()
                        print("游戏已重置")

                if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down_point = self.find_closest_points(pygame.mouse.get_pos())
                    
                    if mouse_down_point is None:
                        print("无着点可下")
                    elif mouse_down_point in self.availablepoints:
                        # 下棋
                        stone_color = (0, 0, 0) if self.who == 'black' else (255, 255, 255)
                        pygame.draw.circle(self.screen, stone_color, mouse_down_point, 10)
                        
                        # 白子加黑边
                        if self.who == 'white':
                            pygame.draw.circle(self.screen, (0, 0, 0), mouse_down_point, 10, 2)
                        
                        # 记录棋子
                        self.mark_points[mouse_down_point] = self.who
                        self.availablepoints.remove(mouse_down_point)
                        
                        # 检查获胜
                        winner = self.wincondition()
                        if winner:
                            game_over = True
                            self.draw_game_over(winner)
                            print(f"游戏结束! {winner}获胜!")
                        else:
                            # 切换玩家
                            self.who = 'white' if self.who == 'black' else 'black'
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Gomoku()
    game.run()