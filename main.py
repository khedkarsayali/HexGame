from ui import HexUI

if __name__ == "__main__":
    size = int(input("Enter board size (9 or 11): "))
    if size not in [9, 11]:
        print("Invalid board size!")
    else:
        game_ui = HexUI(size)
        game_ui.run()
