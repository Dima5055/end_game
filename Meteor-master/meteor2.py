import random
import sys

import pygame
from pygame.locals import *


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # кнопка выхода
                    terminate()
                return
            if event.type == K_SPACE:
                if game_over:
                    game_over = False
                    print(game_over)


def playerHasHitRock(playerRect, rock):
    for b in rock:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_tip():
    Rules_backgroudImage = pygame.image.load("Image/rules.png").convert()
    Rules_backgroudImage = pygame.transform.smoothscale(Rules_backgroudImage, screen.get_size())
    screen.blit(Rules_backgroudImage, (0, 0))
    drawText('Управление:', font_big, screen, (WINDOWWIDTH / 3),
             (WINDOWHEIGHT / 10) + 30)
    drawText('z - обратный ход', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 80)
    drawText('x - замедление времени', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 110)
    drawText('q - пауза, информация об управлении', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 140)
    drawText('w, a, s, d - перемещение в пространстве', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 170)
    drawText('Также возможно перемещение при помощи компьютерной мыши', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 200)
    drawText(' и стрелок на клавиатуре компьютера', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 230)
    pygame.display.update()


WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
FPS = 60
ROCKMINSIZE = 10
ROCKMAXSIZE = 40
ROCKMINSPEED = 1
ROCKMAXSPEED = 8
ADDNEWROCKRATE = 6
PLAYERMOVERATE = 5


# Начинаем игру
pygame.init()
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Метеор')
pygame.mouse.set_visible(False)


# Добовляем шрифт
font = pygame.font.SysFont(None, 48)
font2 = pygame.font.SysFont(None, 20)
font3 = pygame.font.SysFont(None, 30)
font_big = pygame.font.SysFont(None, 60)


# Добовляем музыку
gameOverSound = pygame.mixer.Sound('Sound/zvuki-quotkonets-igryiquot-game-over-sounds-30249.ogg')
pygame.mixer.music.load('Sound/Mathias Rehfeldt Dark Matter Projekt - Ice Field.mp4')


# Добовляем картинки
playerImage = pygame.image.load('Image/character.png')
playerRect = playerImage.get_rect()
rockImage = pygame.image.load('Image/rock.png')
backgroudImage = pygame.image.load("Image/background.jpg").convert()
backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())


# покащываем стартовый экран
Start_backgroudImage = pygame.image.load("Image/start_background.png").convert()
Start_backgroudImage = pygame.transform.smoothscale(Start_backgroudImage, screen.get_size())
screen.blit(Start_backgroudImage, (0, 0))
drawText('Для получения информации об управлении нажмите на клавишу Q', font2, screen, (WINDOWWIDTH / 15), (WINDOWHEIGHT / 12))
drawText('Метеор', font, screen, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 3))
drawText('Нажмите для начала', font, screen, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
drawText('Пояс астероидов, наверное, самое опасное место в немом космосе. И именно за корабль', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 350)
drawText('попавший в это место вам и предстоит играть. Как долго вы сможете продержаться в этом', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 380)
drawText('ужасном месте? Наша игра позволит вам получить такой опыт. В нашей игре вы сможете', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 410)
drawText('отдохнуть, но и потренировать свою реакцию в нашей игре. А соревновательная часть, ', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 440)
drawText('не даст заскучать ещё долгое время.', font3, screen, (WINDOWWIDTH / 15),
             (WINDOWHEIGHT / 12) + 470)

rock = []
pygame.display.update()
waitForPlayerToPressKey()
pause = False
game_over = False
topScore = 0


speed_score = 1
score = 0
playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)
moveLeft = moveRight = moveUp = moveDown = False
reverseCheat = slowCheat = False
rockAddCounter = 0
pygame.mixer.music.play(-1, 0.0)


while True:
    # начинаем игру
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        if event.type == KEYDOWN:
            if event.key == ord('z'):
                reverseCheat = True
            if event.key == ord('x'):
                slowCheat = True
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
            if event.key == K_DOWN or event.key == ord('q'):
                pause = not pause
                draw_tip()

        if event.type == KEYUP:

            if event.key == ord('z'):
                reverseCheat = False
                score = 0
            if event.key == ord('x'):
                slowCheat = False
                score = 0
            if event.key == K_ESCAPE:
                terminate()

            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False

        if event.type == MOUSEMOTION:
            # Можно управлять курсором мышки
            playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

    # добовляем новые метеоры
    if not pause:
        score += speed_score  # изменяем значение набранных очков
        if not reverseCheat and not slowCheat:
            rockAddCounter += 1
        if rockAddCounter == ADDNEWROCKRATE:
            rockAddCounter = 0
            rockSize = random.randint(ROCKMINSIZE, ROCKMAXSIZE)
            newrock = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - rockSize), 0 - rockSize, rockSize,
                                             rockSize),
                         'speed': random.randint(ROCKMINSPEED, ROCKMAXSPEED),
                         'surface': pygame.transform.scale(rockImage, (rockSize, rockSize)),
                         }

            rock.append(newrock)


        # движение игорока
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # подключаем мышь
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Движение метеоров учитывая читы
        for b in rock:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # удаляем метеоры
        for b in rock[:]:
            if b['rect'].top > WINDOWHEIGHT:
                rock.remove(b)

        # картинка на фон
        if score == 100:
            playerImage = pygame.image.load('Image/character3.png')
            backgroudImage = pygame.image.load("Image/background2.jpg").convert()
            backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())
            screen.blit(backgroudImage, (0, 0))

        if score == 300:
            playerImage = pygame.image.load('Image/character3.png')
            backgroudImage = pygame.image.load("Image/background6.jpg").convert()
            backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())
            screen.blit(backgroudImage, (0, 0))

        if score == 500:
            backgroudImage = pygame.image.load("Image/background3.jpg").convert()
            backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())
            screen.blit(backgroudImage, (0, 0))

        if score == 1000:
            playerImage = pygame.image.load('Image/character2.png')
            backgroudImage = pygame.image.load("Image/background4.webp").convert()
            backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())
            screen.blit(backgroudImage, (0, 0))

        if score == 2500:
            backgroudImage = pygame.image.load("Image/background5.jpg").convert()
            backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())
            screen.blit(backgroudImage, (0, 0))

        if score == 3500:
            backgroudImage = pygame.image.load("Image/background7.jpg").convert()
            backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())
            screen.blit(backgroudImage, (0, 0))


        screen.blit(backgroudImage, (0, 0))

        # пишем значение очков
        drawText('Score: %s' % (score), font, screen, 10, 0)
        drawText('Top Score: %s' % (topScore), font, screen, 10, 40)

        # Рисуем игорока
        screen.blit(playerImage, playerRect)

        # Рисуем метеоры
        for b in rock:
            screen.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Проверяем столкнулся ли игрок с камнем
        if playerHasHitRock(playerRect, rock):
            if score > topScore:
                topScore = score  # выставляем новое значение
            game_over = True
        mainClock.tick(FPS)

        if game_over:
            # Останавливаем игру и выводим экран проигрыша
            pygame.mixer.music.stop()
            gameOverSound.play()
            End_backgroudImage = pygame.image.load("Image/lose.jpg").convert()
            End_backgroudImage = pygame.transform.smoothscale(End_backgroudImage, screen.get_size())
            screen.blit(End_backgroudImage, (0, 0))
            drawText('GAME OVER', font, screen, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
            drawText('Press a key to play again.', font, screen, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
            drawText('К сожалению, ваша экспедиция потерпела крушение. Не переживайте, у вас ещё будет', font3, screen, (WINDOWWIDTH / 15),
                     (WINDOWHEIGHT / 12) + 350)
            drawText('для совершенства своих навыков. Всегда помните "путь в тысячу ли начинается с первого', font3, screen, (WINDOWWIDTH / 15),
                     (WINDOWHEIGHT / 12) + 380)
            drawText('шага". Не оставляйте своих попыток и продолжайте двигаться навстречу рекордам.', font3, screen,
                     (WINDOWWIDTH / 15),
                     (WINDOWHEIGHT / 12) + 410)

            pygame.display.update()
            waitForPlayerToPressKey()
            gameOverSound.stop()
