from sguif import App
from udef import main_model, main_view, icon_path, window_title


def main():
    App(main_model, main_view, icon_path, window_title).forever_loop(dark=True)


if __name__ == '__main__':
    main()
