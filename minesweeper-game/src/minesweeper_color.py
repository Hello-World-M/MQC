#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
5x5 扫雷游戏（彩色增强版）
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
    TIMEOUT = 3  # 超时


class Difficulty(Enum):
    """游戏难度枚举"""
    EASY = 1  # 简单：15 分钟
    HARD = 2  # 困难：10 分钟
    EXTREME = 3  # 极限：5 分钟
    CUSTOM = 4  # 自定义


class Colors:
    """终端颜色类，跨平台兼容"""
    
    # 默认支持颜色，大多数现代终端都支持ANSI颜色代码
    SUPPORTS_COLOR = True
    
    # 只在特定条件下禁用颜色
    if not hasattr(sys, 'stdout') or not sys.stdout.isatty():
        # 如果输出不是终端（例如重定向到文件），禁用颜色
        SUPPORTS_COLOR = False
    
    if SUPPORTS_COLOR:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    else:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
        BOLD = UNDERLINE = END = ''
    
    @staticmethod
    def colorize(text, color):
        """给文本添加颜色"""
        if not Colors.SUPPORTS_COLOR:
            return text
        return f"{color}{text}{Colors.END}"
    
    @staticmethod
    def get_number_color(num):
        """获取数字对应的颜色"""
        color_map = {
            1: Colors.BLUE,
            2: Colors.GREEN,
            3: Colors.RED,
            4: Colors.MAGENTA,
            5: Colors.YELLOW,
            6: Colors.CYAN,
            7: Colors.BOLD + Colors.RED,
            8: Colors.BOLD + Colors.MAGENTA
        }
        return color_map.get(num, '')


class Minesweeper:
    """扫雷游戏主类"""
    
    def __init__(self, size=5, mines=None, time_limit=None):
        """
        初始化游戏

        Args:
            size: 游戏网格大小（默认5x5）
            mines: 地雷数量（None 表示随机 3-5 个，否则使用指定数量）
            time_limit: 时间限制（秒），None 表示无限制
        """
        self.size = size
        # 如果未指定地雷数量，则在 3-5 之间随机
        self.mines = mines if mines is not None else random.randint(3, 5)
        self.show_mine_count = mines is not None  # 是否显示地雷数量
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # 0表示空地，-1表示地雷
        self.state = [[CellState.HIDDEN for _ in range(size)] for _ in range(size)]  # 单元格状态
        self.game_status = GameStatus.PLAYING
        self.moves = 0  # 移动次数
        self.first_move = True  # 是否第一次移动
        self.time_limit = time_limit  # 时间限制（秒）
        self.start_time = None  # 游戏开始时间
        
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

        # 检查是否超时
        if self.check_timeout():
            self.game_status = GameStatus.TIMEOUT
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
            return Colors.colorize('.', Colors.WHITE)
        elif self.state[row][col] == CellState.FLAGGED:
            return Colors.colorize('F', Colors.RED)
        elif self.state[row][col] == CellState.REVEALED:
            if self.grid[row][col] == -1:
                return Colors.colorize('*', Colors.RED)
            elif self.grid[row][col] == 0:
                return ' '
            else:
                # 根据数字显示不同颜色
                num = self.grid[row][col]
                color = Colors.get_number_color(num)
                return Colors.colorize(str(num), color)
        return '?'
    
    def display(self, show_mines=False):
        """显示游戏网格"""
        # 显示标题和列号
        title = Colors.colorize("  5x5 扫雷游戏", Colors.BOLD + Colors.CYAN)
        print(title)
        print('   ' + ' '.join(str(i) for i in range(self.size)))
        print('   ' + '-' * (2 * self.size + 1))
        
        for row in range(self.size):
            # 行号
            row_header = Colors.colorize(str(row), Colors.BOLD)
            row_line = f'{row_header} |'
            
            for col in range(self.size):
                cell_display = self.get_cell_display(row, col)
                
                # 游戏结束时显示所有地雷
                if show_mines and self.grid[row][col] == -1 and self.state[row][col] != CellState.FLAGGED:
                    cell_display = Colors.colorize('*', Colors.RED)
                
                row_line += f' {cell_display}'
            
            print(row_line)
        
        # 显示游戏状态
        status_text = self.get_status_text()
        if self.game_status == GameStatus.WON:
            status_color = Colors.GREEN
        elif self.game_status == GameStatus.LOST:
            status_color = Colors.RED
        else:
            status_color = Colors.YELLOW
            
        print(f'\n游戏状态: {Colors.colorize(status_text, status_color)}')

        # 如果是随机地雷模式，不显示具体数量
        if self.show_mine_count:
            mines_text = f'剩余地雷: {self.get_remaining_mines()}'
        else:
            mines_text = '剩余地雷: ???'
        print(Colors.colorize(mines_text, Colors.BOLD))

        # 显示剩余时间
        if self.time_limit is not None and self.start_time is not None:
            remaining_time = self.get_remaining_time()
            if remaining_time > 0:
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                time_color = Colors.GREEN if remaining_time > 60 else Colors.YELLOW if remaining_time > 30 else Colors.RED
                time_text = f'剩余时间: {minutes:02d}:{seconds:02d}'
                print(Colors.colorize(time_text, time_color))
        
        # 显示操作提示
        if self.game_status == GameStatus.PLAYING:
            print(Colors.colorize("\n提示:", Colors.BOLD))
            print("  输入坐标揭开格子 (例如: 12)")
            print("  输入 f+坐标标记地雷 (例如: f12)")
            print("  输入 r 重新开始, d 更改难度, q 退出")
    
    def get_status_text(self):
        """获取游戏状态文本"""
        if self.game_status == GameStatus.PLAYING:
            return '游戏中'
        elif self.game_status == GameStatus.WON:
            return '你赢了! 🎉'
        elif self.game_status == GameStatus.TIMEOUT:
            return '时间到! ⏰'
        else:
            return '你输了 💣'
    
    def get_remaining_mines(self):
        """获取剩余地雷数"""
        flagged_count = sum(1 for row in self.state for cell in row if cell == CellState.FLAGGED)
        return self.mines - flagged_count

    def get_remaining_time(self):
        """
        获取剩余时间（秒）

        Returns:
            int: 剩余时间（秒），如果游戏未开始则返回 time_limit
        """
        import time
        if self.start_time is None:
            return self.time_limit
        elapsed = int(time.time() - self.start_time)
        remaining = self.time_limit - elapsed
        return max(0, remaining)

    def start_timer(self):
        """开始计时"""
        import time
        self.start_time = time.time()

    def check_timeout(self):
        """
        检查是否超时

        Returns:
            bool: 是否超时
        """
        import time
        if self.time_limit is None:
            return False
        if self.start_time is None:
            return False
        elapsed = time.time() - self.start_time
        return elapsed >= self.time_limit

    def check_win(self):
        """检查游戏是否获胜"""
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] != -1 and self.state[row][col] != CellState.REVEALED:
                    return  # 还有非地雷格子未揭开，游戏继续

        # 所有非地雷格子都已揭开，游戏胜利
        self.game_status = GameStatus.WON
    
    def reset(self):
        """重置游戏"""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.state = [[CellState.HIDDEN for _ in range(self.size)] for _ in range(self.size)]
        self.game_status = GameStatus.PLAYING
        self.moves = 0
        self.first_move = True
        self.start_time = None  # 重置开始时间


def clear_screen():
    """清屏，跨平台兼容"""
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


def get_input(prompt):
    """获取用户输入，处理EOF错误"""
    try:
        return input(Colors.colorize(prompt, Colors.CYAN)).strip()
    except EOFError:
        print(Colors.colorize("\n再见!", Colors.YELLOW))
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


def print_welcome_message():
    """打印欢迎信息"""
    welcome_text = """
╔════════════════════════════════════╗
║         5x5 扫雷游戏              ║
║     兼容Python 3.11              ║
║        跨平台支持                ║
╚════════════════════════════════════╝
"""
    print(Colors.colorize(welcome_text, Colors.CYAN + Colors.BOLD))
    print(Colors.colorize("游戏规则:", Colors.BOLD))
    print("1. 输入坐标来揭开格子，格式: 行列 (例如: 12 表示第1行第2列)")
    print("2. 输入 f + 坐标来标记地雷，格式: f 行列 (例如: f12)")
    print("3. 输入 r 重新开始，输入 q 退出游戏")
    print("4. 数字表示周围地雷的数量")
    print()
    get_input("按回车键开始游戏...")


def print_goodbye_message():
    """打印告别信息"""
    goodbye_text = """
╔════════════════════════════════════╗
║           感谢游玩                ║
║            再见!                  ║
╚════════════════════════════════════╝
"""
    print(Colors.colorize(goodbye_text, Colors.YELLOW + Colors.BOLD))


def select_difficulty():
    """
    选择游戏难度

    Returns:
        int: 时间限制（秒）
    """
    print(Colors.colorize("=" * 40, Colors.BOLD))
    print(Colors.colorize("选择游戏难度", Colors.BOLD + Colors.CYAN))
    print(Colors.colorize("=" * 40, Colors.BOLD))
    print("1. 简单（15 分钟）")
    print("2. 困难（10 分钟）")
    print("3. 极限（5 分钟）")
    print("4. 自定义")
    print()

    while True:
        choice = get_input("请输入难度选择 (1-4): ")
        if choice == '1':
            return 15 * 60  # 15 分钟
        elif choice == '2':
            return 10 * 60  # 10 分钟
        elif choice == '3':
            return 5 * 60  # 5 分钟
        elif choice == '4':
            while True:
                minutes = get_input("请输入倒计时时长（分钟）: ")
                try:
                    minutes = int(minutes)
                    if minutes <= 0:
                        error_text = Colors.colorize("时间必须大于 0！", Colors.RED)
                        print(error_text)
                        continue
                    return minutes * 60
                except ValueError:
                    error_text = Colors.colorize("请输入有效的数字！", Colors.RED)
                    print(error_text)
        else:
            error_text = Colors.colorize("无效选择，请输入 1-4！", Colors.RED)
            print(error_text)


def main():
    """游戏主循环"""
    # 不指定地雷数量，让游戏随机生成 3-5 个地雷
    time_limit = select_difficulty()
    game = Minesweeper(size=5, time_limit=time_limit)

    print_welcome_message()
    
    while True:
        clear_screen()
        game.display()

        if game.game_status != GameStatus.PLAYING:
            game.display(show_mines=True)

            if game.game_status == GameStatus.WON:
                stats_text = f"恭喜! 你用 {game.moves} 步完成了游戏!"
                print(Colors.colorize(stats_text, Colors.GREEN + Colors.BOLD))
            elif game.game_status == GameStatus.TIMEOUT:
                timeout_text = Colors.colorize("很遗憾，时间到了！游戏失败。", Colors.RED + Colors.BOLD)
                print(timeout_text)
            else:
                print(Colors.colorize("很遗憾，你踩到地雷了!", Colors.RED + Colors.BOLD))

            choice = get_input("\n输入 r 重新开始，输入 d 更改难度，输入 q 退出: ").lower()
            if choice == 'r':
                game.reset()
                continue
            elif choice == 'd':
                game.__init__(size=5, time_limit=select_difficulty())
                continue
            elif choice == 'q':
                print_goodbye_message()
                break
            else:
                continue

        # 首次操作时开始计时
        if game.start_time is None:
            game.start_timer()
        
        # 获取用户输入
        user_input = get_input("请输入操作: ").lower()
        
        # 处理命令
        if user_input == 'q':
            print_goodbye_message()
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
            error_text = Colors.colorize("无效输入! 请使用格式: 行列 (例如: 12)", Colors.RED)
            print(error_text)
            get_input("按回车继续...")
            continue
        
        row, col = coords
        
        # 检查坐标是否在有效范围内
        if not game.is_valid_cell(row, col):
            error_text = Colors.colorize(f"坐标超出范围! 请输入 0-{game.size-1} 之间的数字", Colors.RED)
            print(error_text)
            get_input("按回车继续...")
            continue
        
        # 执行操作
        if flag_mode:
            if game.toggle_flag(row, col):
                # 标记成功，继续游戏
                continue
            else:
                error_text = Colors.colorize("无法标记该位置!", Colors.RED)
                print(error_text)
        else:
            if game.reveal_cell(row, col):
                # 揭开成功，继续游戏
                continue
            else:
                error_text = Colors.colorize("无法揭开该位置!", Colors.RED)
                print(error_text)
        
        get_input("按回车继续...")


if __name__ == "__main__":
    main()