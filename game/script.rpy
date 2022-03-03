style default_bar:
    left_bar Frame('blue.png', 0, 0)
    right_bar Frame('red.jpg', 0, 0)

style inversion_bar:
    left_bar Frame('red.jpg', 0, 0)
    right_bar Frame('blue.png', 0, 0)


init python:
    import pygame
    from random import randint

    def get_random_value(x):
        return randint(int(x*0.4), int(x*0.9))

    class MoveRect(renpy.Displayable):

        def __init__(self, xsize, ysize, screen_x_size, bars_values, img=None, **kwargs):
            super(MoveRect, self).__init__(**kwargs)

            if not img:
                self.img = renpy.displayable(Solid('#FF0000', xsize=xsize, ysize=ysize))
            else:
                self.img = renpy.displayable(Crop((0, 0, xsize, ysize), img))
            self.x_size = xsize
            self.x_pos = 0
            self.speed = int(screen_x_size * 0.02)
            self.screen_x_size = screen_x_size
            self.valid_range = range(
                int(bars_values[0]),
                int(screen_x_size*0.1+bars_values[0]+bars_values[1]*2)
            )

        def render(self, width, height, st, at):
            img_render = renpy.render(self.img, width, height, st, at)
            render = renpy.Render(width, height)
            render.blit(img_render, (self.x_pos, 0))

            if self.x_pos > self.screen_x_size - int(self.screen_x_size * 0.1) - self.x_size:
                self.speed = -self.speed
            elif self.x_pos < 0:
                self.speed = -self.speed
            self.x_pos += self.speed

            renpy.redraw(self.img, 0)

            return render

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.x_pos in self.valid_range:
                    return 'win'
                else:
                    return 'lose'
            else:
                raise renpy.IgnoreEvent()

        def visit(self):
            return [self.img,]


label start:

    # Здесь передаём кофигурацию для экрана
    call screen bg_screen(500, 130, 0.8, 0.8)

    # Обрабатывается конечный результат
    'return result: [_return]'


screen bg_screen(x_size, y_size, x_align, y_align, img=None):
    default bars_value = get_random_value(int(x_size*0.4))
    default bars_value2 = int(x_size*0.4) - bars_value

    frame:
        xalign x_align yalign x_align
        xsize x_size ysize y_size

        if img:
            add Crop((0, 0, x_size, y_size), img)
        else:
            add Solid('#FFFF00', xsize=x_size, ysize=y_size, xpos=-3, ypos=-3)
        bar value ScreenVariableValue('bars_value', int(x_size*0.4), style='default_bar') yalign 0.5 xpos int(x_size*0.1) xsize int(x_size*0.4) ysize int(y_size*0.7)
        bar value ScreenVariableValue('bars_value2', int(x_size*0.4), style='inversion_bar') yalign 0.5 xpos int(x_size*0.5) xsize int(x_size*0.4) ysize int(y_size*0.7)
        add MoveRect(ysize=int(y_size*0.9), xsize=int(x_size*0.07), screen_x_size=x_size, bars_values=[bars_value, bars_value2], img='button.png'):
            yalign 0.5
            xpos int(x_size*0.05)
