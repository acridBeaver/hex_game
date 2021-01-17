from hexogon.Game import *
from consts import *

if __name__ == '__main__':
    game = Game(SIZE)
    game.load_data()
    buttons = []

    run = True
    while run:
        game.clock.tick(FPS)
        if not game.started:
            run = game.start_screen()
        else:
            game.highlight(pg.mouse.get_pos())
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    game.tick(pg.mouse.get_pos())

            for button in buttons:
                button.highlighted()

            game.screen.blit(game.bg_img, (0, 0))
            game.show_grid()
            for button in buttons:
                button.show(game.screen)
            if game.checkWin():
                run = game.go_screen(game.checkWin())
        pg.display.flip()

    pg.quit()
