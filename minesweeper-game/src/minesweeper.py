#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
5x5 扫雷游戏
兼容Python 3.11，具有良好的跨平台兼容性
"""

import os
import random
import sys
from enum import Enum


class CellState(Enum):
    """单元格状态枚举"""
    HIDDEN = 0  # 未揭开
    REVEALED = 1  # 已揭开
    FLAGGED = 2  # 已标记


class GameStatus(Enum):
    """游戏状态枚举"""
    PLAYING = 0  # 游戏中
    WON = 1  # 胜利
    LOST = 2  # 失败


class Minesweeper:
    """扫雷游戏主类"""
    
    def __init__(self, size=5, mines=5):
        """
        初始化游戏
        
        Args:
            size: 游戏网格大小（默认5x5）
            mines: 地雷数量（默认5个）
        """
        self.size = size
        self.mines = mines
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # 0表示空地，-1表示地雷
        self.state = [[CellState.HIDDEN for _ in range(size)] for _ in range(size)]  # 单元格状态
        self.game_status = GameStatus.PLAYING
        self.moves = 0  # 移动次数
        self.first_move = True  # 是否第一次移动
        
    def is_valid_cell(self, row, col):
        """检查坐标是否有效"""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def get_neighbors(self, row, col):
        """获取某个格子的所有邻居坐标"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.is_valid_cell(nr, nc):
                    neighbors.append((nr, nc))
        return neighbors
    
    def place_mines(self, first_row, first_col):
        """
        放置地雷，确保第一次点击的位置和周围都没有地雷
        
        Args:
            first_row: 第一次点击的行
            first_col: 第一次点击的列
        """
        mines_placed = 0
        protected_cells = [(first_row, first_col)] + self.get_neighbors(first_row, first_col)
        
        while mines_placed < self.mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            
            # 不在保护区域内且当前格子还没有地雷
            if (row, col) not in protected_cells and self.grid[row][col] != -1:
                self.grid[row][col] = -1  # -1表示地雷
                mines_placed += 1
        
        # 计算每个非地雷格子周围的地雷数
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] != -1:
                    count = 0
                    for nr, nc in self.get_neighbors(row, col):
                        if self.grid[nr][nc] == -1:
                            count += 1
                    self.grid[row][col] = count
    
    def reveal_cell(self, row, col):
        """
        揭开一个格子
        
        Args:
            row: 行坐标
            col: 列坐标
        
        Returns:
            bool: 是否成功揭开
        """
        if not self.is_valid_cell(row, col):
            return False
        
        if self.state[row][col] != CellState.HIDDEN:
            return False
        
        # 第一次点击时放置地雷
        if self.first_move:
            self.place_mines(row, col)
            self.first_move = False
        
        self.state[row][col] = CellState.REVEALED
        self.moves += 1
        
        # 如果点到地雷，游戏结束
        if self.grid[row][col] == -1:
            self.game_status = GameStatus.LOST
            return True
        
        # 如果是空格（周围没有地雷），自动揭开周围的格子
        if self.grid[row][col] == 0:
            for nr, nc in self.get_neighbors(row, col):
                if self.state[nr][nc] == CellState.HIDDEN:
                    self.reveal_cell(nr, nc)
        
        # 检查是否获胜
        self.check_win()
        return True
    
    def toggle_flag(self, row, col):
        """
        切换标记状态
        
        Args:
            row: 行坐标
            col: 列坐标
        
        Returns:
            bool: 是否成功切换
        """
        if not self.is_valid_cell(row, col):
            return False
        
        if self.state[row][col] == CellState.REVEALED:
            return False
        
        if self.state[row][col] == CellState.HIDDEN:
            self.state[row][col] = CellState.FLAGGED
        else:  # CellState.FLAGGED
            self.state[row][col] = CellState.HIDDEN
        
        self.check_win()
        return True
    
    def check_win(self):
        """检查游戏是否获胜"""
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] != -1 and self.state[row][col] != CellState.REVEALED:
                    return  # 还有非地雷格子未揭开，游戏继续
        
        # 所有非地雷格子都已揭开，游戏胜利
        self.game_status = GameStatus.WON
    
    def get_cell_display(self, row, col):
        """
        获取格子的显示字符
        
        Args:
            row: 行坐标
            col: 列坐标
        
        Returns:
            str: 显示字符
        """
        if self.state[row][col] == CellState.HIDDEN:
            return '.'
        elif self.state[row][col] == CellState.FLAGGED:
            return 'F'
        elif self.state[row][col] == CellState.REVEALED:
            if self.grid[row][col] == -1:
                return '*'
            elif self.grid[row][col] == 0:
                return ' '
            else:
                return str(self.grid[row][col])
        return '?'
    
    def display(self, show_mines=False):
        """显示游戏网格"""
        # 显示列号
        print('   ' + ' '.join(str(i) for i in range(self.size)))
        print('   ' + '-' * (2 * self.size + 1))
        
        for row in range(self.size):
            row_line = f'{row} |'
            for col in range(self.size):
                cell_display = self.get_cell_display(row, col)
                
                # 游戏结束时显示所有地雷
                if show_mines and self.grid[row][col] == -1 and self.state[row][col] != CellState.FLAGGED:
                    cell_display = '*'
                
                row_line += f' {cell_display}'
            
            print(row_line)
        
        # 显示游戏状态
        print(f'\n游戏状态: {self.get_status_text()}')
        print(f'剩余地雷: {self.get_remaining_mines()}')
    
    def get_status_text(self):
        """获取游戏状态文本"""
        if self.game_status == GameStatus.PLAYING:
            return '游戏中'
        elif self.game_status == GameStatus.WON:
            return '你赢了! 🎉'
        else:
            return '你输了 💣'
    
    def get_remaining_mines(self):
        """获取剩余地雷数"""
        flagged_count = sum(1 for row in self.state for cell in row if cell == CellState.FLAGGED)
        return self.mines - flagged_count
    
    def reset(self):
        """重置游戏"""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.state = [[CellState.HIDDEN for _ in range(self.size)] for _ in range(self.size)]
        self.game_status = GameStatus.PLAYING
        self.moves = 0
        self.first_move = True


def clear_screen():
    """清屏，跨平台兼容"""
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


def get_input(prompt):
    """获取用户输入，处理EOF错误"""
    try:
        return input(prompt).strip()
    except EOFError:
        print("\n再见!")
        sys.exit(0)


def parse_coordinates(input_str):
    """
    解析坐标输入
    
    Args:
        input_str: 用户输入字符串，格式如"r c"或"rc"
    
    Returns:
        tuple: (row, col) 或 None 如果输入无效
    """
    # 移除所有空格
    input_str = input_str.replace(" ", "")
    
    if len(input_str) < 2 or len(input_str) > 3:
        return None
    
    # 解析行和列
    try:
        if len(input_str) == 2:
            row = int(input_str[0])
            col = int(input_str[1])
        else:  # len == 3
            row = int(input_str[0])
            col = int(input_str[1:])
        
        return row, col
    except ValueError:
        return None


def main():
    """游戏主循环"""
    game = Minesweeper(size=5, mines=5)
    
    print("欢迎来到 5x5 扫雷游戏!")
    print("输入坐标来揭开格子，格式: 行列 (例如: 12 表示第1行第2列)")
    print("输入 f + 坐标来标记地雷，格式: f 行列 (例如: f12)")
    print("输入 r 重新开始，输入 q 退出游戏")
    print()
    
    while True:
        clear_screen()
        game.display()
        
        if game.game_status != GameStatus.PLAYING:
            game.display(show_mines=True)
            
            if game.game_status == GameStatus.WON:
                print(f"恭喜! 你用 {game.moves} 步完成了游戏!")
            else:
                print("很遗憾，你踩到地雷了!")
            
            choice = get_input("\n输入 r 重新开始，输入 q 退出: ").lower()
            if choice == 'r':
                game.reset()
                continue
            elif choice == 'q':
                print("再见!")
                break
            else:
                continue
        
        # 获取用户输入
        user_input = get_input("\n请输入坐标 (例如: 12) 或标记 (例如: f12): ").lower()
        
        # 处理命令
        if user_input == 'q':
            print("再见!")
            break
        elif user_input == 'r':
            game.reset()
            continue
        
        # 处理标记
        flag_mode = False
        if user_input.startswith('f'):
            flag_mode = True
            user_input = user_input[1:]  # 移除f前缀
        
        # 解析坐标
        coords = parse_coordinates(user_input)
        if coords is None:
            print("无效输入! 请使用格式: 行列 (例如: 12)")
            get_input("按回车继续...")
            continue
        
        row, col = coords
        
        # 执行操作
        if flag_mode:
            if game.toggle_flag(row, col):
                # 标记成功，继续游戏
                continue
            else:
                print("无法标记该位置!")
        else:
            if game.reveal_cell(row, col):
                # 揭开成功，继续游戏
                continue
            else:
                print("无法揭开该位置!")
        
        get_input("按回车继续...")


if __name__ == "__main__":
    main()