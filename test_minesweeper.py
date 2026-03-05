#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
扫雷游戏自动化测试脚本
测试基础版本和彩色版本的所有核心功能
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minesweeper-game', 'src'))

from minesweeper import Minesweeper, CellState, GameStatus, Difficulty

def test_game_initialization():
    """测试游戏初始化"""
    print("测试1: 游戏初始化")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    assert game.size == 5, "网格大小应该为5"
    assert game.mines == 5, "地雷数量应该为5"
    assert game.game_status == GameStatus.PLAYING, "初始状态应该为游戏中"
    assert game.first_move == True, "应该标记为首次移动"
    assert game.time_limit == 300, "时间限制应该为300秒"
    print("✓ 游戏初始化测试通过")

def test_random_mines():
    """测试随机地雷数量"""
    print("\n测试2: 随机地雷数量")
    game = Minesweeper(size=5, mines=None, time_limit=300)
    assert 3 <= game.mines <= 5, f"随机地雷数量应该在3-5之间，实际为{game.mines}"
    assert game.show_mine_count == False, "随机模式不应显示地雷数量"
    print(f"✓ 随机地雷数量测试通过 (地雷数: {game.mines})")

def test_mine_placement():
    """测试地雷放置"""
    print("\n测试3: 地雷放置和首次点击保护")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.place_mines(0, 0)
    assert game.grid[0][0] != -1, "首次点击位置不应该有地雷"
    neighbors = game.get_neighbors(0, 0)
    for nr, nc in neighbors:
        assert game.grid[nr][nc] != -1, f"首次点击周围({nr},{nc})不应该有地雷"
    mine_count = sum(1 for row in game.grid for cell in row if cell == -1)
    assert mine_count == 5, f"应该有5个地雷，实际为{mine_count}"
    print("✓ 地雷放置测试通过")

def test_cell_reveal():
    """测试揭开格子"""
    print("\n测试4: 揭开格子")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.place_mines(0, 0)
    initial_moves = game.moves
    success = game.reveal_cell(1, 1)
    assert success == True, "揭开应该成功"
    assert game.state[1][1] == CellState.REVEALED, "格子状态应该是已揭开"
    assert game.moves > initial_moves, "移动次数应该增加"
    success = game.reveal_cell(1, 1)
    assert success == False, "重复揭开应该失败"
    print("✓ 揭开格子测试通过")

def test_flag_toggle():
    """测试标记地雷"""
    print("\n测试5: 标记地雷")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.place_mines(0, 0)
    success = game.toggle_flag(0, 1)
    assert success == True, "标记应该成功"
    assert game.state[0][1] == CellState.FLAGGED, "格子状态应该是已标记"
    success = game.toggle_flag(0, 1)
    assert success == True, "取消标记应该成功"
    assert game.state[0][1] == CellState.HIDDEN, "格子状态应该是未揭开"
    game.reveal_cell(1, 1)
    success = game.toggle_flag(1, 1)
    assert success == False, "标记已揭开的格子应该失败"
    print("✓ 标记地雷测试通过")

def test_lose_condition():
    """测试失败条件"""
    print("\n测试6: 失败条件（踩到地雷）")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.place_mines(0, 0)
    mine_pos = None
    for row in range(game.size):
        for col in range(game.size):
            if game.grid[row][col] == -1:
                mine_pos = (row, col)
                break
        if mine_pos:
            break
    assert mine_pos is not None, "应该找到地雷"
    game.reveal_cell(mine_pos[0], mine_pos[1])
    assert game.game_status == GameStatus.LOST, "游戏状态应该是失败"
    print("✓ 失败条件测试通过")

def test_win_condition():
    """测试胜利条件"""
    print("\n测试7: 胜利条件")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.mines = 0
    game.grid = [[0 for _ in range(5)] for _ in range(5)]
    for row in range(game.size):
        for col in range(game.size):
            game.reveal_cell(row, col)
    assert game.game_status == GameStatus.WON, "游戏状态应该是胜利"
    print("✓ 胜利条件测试通过")

def test_timeout():
    """测试超时功能"""
    print("\n测试8: 超时功能")
    game = Minesweeper(size=5, mines=5, time_limit=1)
    game.place_mines(0, 0)
    game.start_timer()
    game.reveal_cell(1, 1)
    import time
    time.sleep(1.5)
    is_timeout = game.check_timeout()
    assert is_timeout == True, "应该超时"
    print("✓ 超时功能测试通过")

def test_remaining_mines():
    """测试剩余地雷数计算"""
    print("\n测试9: 剩余地雷数计算")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.place_mines(0, 0)
    mine_count = 0
    for row in range(game.size):
        for col in range(game.size):
            if game.grid[row][col] == -1 and mine_count < 2:
                game.toggle_flag(row, col)
                mine_count += 1
    remaining = game.get_remaining_mines()
    assert remaining == 3, f"应该剩余3个地雷，实际为{remaining}"
    print("✓ 剩余地雷数计算测试通过")

def test_reset():
    """测试重置功能"""
    print("\n测试10: 重置功能")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    game.place_mines(0, 0)
    game.reveal_cell(1, 1)
    game.toggle_flag(2, 2)
    game.reset()
    assert game.game_status == GameStatus.PLAYING, "游戏状态应该重置为游戏中"
    assert game.moves == 0, "移动次数应该重置为0"
    assert game.first_move == True, "应该重置为首次移动"
    assert game.start_time is None, "开始时间应该重置为None"
    for row in range(game.size):
        for col in range(game.size):
            assert game.state[row][col] == CellState.HIDDEN, "所有格子状态应该重置为未揭开"
    print("✓ 重置功能测试通过")

def test_difficulty_enum():
    """测试难度枚举"""
    print("\n测试11: 难度枚举")
    assert Difficulty.EASY.value == 1, "简单难度值应该为1"
    assert Difficulty.HARD.value == 2, "困难难度值应该为2"
    assert Difficulty.EXTREME.value == 3, "极限难度值应该为3"
    assert Difficulty.CUSTOM.value == 4, "自定义难度值应该为4"
    print("✓ 难度枚举测试通过")

def test_coordinate_validation():
    """测试坐标验证"""
    print("\n测试12: 坐标验证")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    assert game.is_valid_cell(0, 0) == True, "(0,0)应该是有效坐标"
    assert game.is_valid_cell(4, 4) == True, "(4,4)应该是有效坐标"
    assert game.is_valid_cell(-1, 0) == False, "(-1,0)应该是无效坐标"
    assert game.is_valid_cell(0, 5) == False, "(0,5)应该是无效坐标"
    assert game.is_valid_cell(5, 5) == False, "(5,5)应该是无效坐标"
    print("✓ 坐标验证测试通过")

def test_recursive_reveal():
    """测试递归展开"""
    print("\n测试13: 递归展开（空白区域自动展开）")
    game = Minesweeper(size=5, mines=1, time_limit=300)
    game.grid = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1]
    ]
    game.mines = 1
    game.reveal_cell(0, 0)
    revealed_count = sum(1 for row in game.state for cell in row if cell == CellState.REVEALED)
    assert revealed_count > 10, f"应该自动展开多个格子，实际为{revealed_count}个"
    print(f"✓ 递归展开测试通过 (自动展开{revealed_count}个格子)")

def test_neighbor_calculation():
    """测试邻居计算"""
    print("\n测试14: 邻居计算")
    game = Minesweeper(size=5, mines=5, time_limit=300)
    neighbors = game.get_neighbors(0, 0)
    assert len(neighbors) == 3, f"角落格子应该有3个邻居，实际为{len(neighbors)}"
    neighbors = game.get_neighbors(0, 2)
    assert len(neighbors) == 5, f"边缘格子应该有5个邻居，实际为{len(neighbors)}"
    neighbors = game.get_neighbors(2, 2)
    assert len(neighbors) == 8, f"中心格子应该有8个邻居，实际为{len(neighbors)}"
    print("✓ 邻居计算测试通过")

def test_parse_coordinates():
    """测试坐标解析"""
    print("\n测试15: 坐标解析")
    from minesweeper import parse_coordinates
    coords = parse_coordinates("12")
    assert coords == (1, 2), f"\"12\"应该解析为(1,2)，实际为{coords}"
    coords = parse_coordinates("123")
    assert coords == (1, 23), f"\"123\"应该解析为(1,23)，实际为{coords}"
    coords = parse_coordinates("1 2")
    assert coords == (1, 2), f"\"1 2\"应该解析为(1,2)，实际为{coords}"
    coords = parse_coordinates("abc")
    assert coords is None, f"\"abc\"应该返回None，实际为{coords}"
    coords = parse_coordinates("1")
    assert coords is None, f"\"1\"应该返回None，实际为{coords}"
    print("✓ 坐标解析测试通过")

def test_color_version():
    """测试彩色版本"""
    print("\n测试16: 彩色版本兼容性")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minesweeper-game', 'src'))
    from minesweeper_color import Minesweeper as ColorMinesweeper, Colors
    game = ColorMinesweeper(size=5, mines=5, time_limit=300)
    assert game.size == 5, "彩色版本网格大小应该为5"
    colored_text = Colors.colorize("test", Colors.RED)
    assert "test" in colored_text, "颜色化应该包含原文本"
    assert Colors.get_number_color(1) == Colors.BLUE, "数字1应该映射为蓝色"
    assert Colors.get_number_color(2) == Colors.GREEN, "数字2应该映射为绿色"
    print("✓ 彩色版本测试通过")

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("扫雷游戏自动化测试")
    print("=" * 50)
    print()

    tests = [
        test_game_initialization,
        test_random_mines,
        test_mine_placement,
        test_cell_reveal,
        test_flag_toggle,
        test_lose_condition,
        test_win_condition,
        test_timeout,
        test_remaining_mines,
        test_reset,
        test_difficulty_enum,
        test_coordinate_validation,
        test_recursive_reveal,
        test_neighbor_calculation,
        test_parse_coordinates,
        test_color_version
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 测试出错: {e}")
            failed += 1

    print()
    print("=" * 50)
    print(f"测试完成！")
    print(f"通过: {passed}/{len(tests)}")
    print(f"失败: {failed}/{len(tests)}")
    print("=" * 50)

    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
