import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルに対応する方向を向いた画像Surfaceの辞書を返す
    """
    img0 = pg.image.load("fig/3.png")
    # 左向きが基本の場合の反転・回転例
    img1 = pg.transform.flip(img0, True, False)  # 右向き
    
    kk_dict = {
        (0, 0):   pg.transform.rotozoom(img0, 0, 0.9),    # 静止 演習3の途中
        (+5, 0):  pg.transform.rotozoom(img1, 0, 0.9),    # 右
        (+5, -5): pg.transform.rotozoom(img1, 45, 0.9),   # 右上
        (0, -5):  pg.transform.rotozoom(img1, 90, 0.9),   # 上
        (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
        (-5, 0):  pg.transform.rotozoom(img0, 0, 0.9),    # 左
        (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),   # 左下
        (0, +5):  pg.transform.rotozoom(img0, -90, 0.9),  # 下
        (+5, +5): pg.transform.rotozoom(img1, -45, 0.9),  # 右下
    }
    return kk_dict

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrectか、ばくだんrect
    戻り値：タプル（横方向、縦方向）
    """
    
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    black_out = pg.Surface((WIDTH, HEIGHT))
    black_out.fill((0, 0, 0)) 
    black_out.set_alpha(150)  
    
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    kk_img = pg.image.load("fig/8.png") 
    kk_rct_l = kk_img.get_rect()
    kk_rct_l.center = (WIDTH//2 - 250, HEIGHT//2)
    kk_rct_r = kk_img.get_rect()
    kk_rct_r.center = (WIDTH//2 + 250, HEIGHT//2)

    black_out.blit(txt, txt_rct)
    black_out.blit(kk_img, kk_rct_l)
    black_out.blit(kk_img, kk_rct_r)
    screen.blit(black_out, [0, 0])

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  
    
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    bb_imgs, bb_accs = init_bb_imgs()
    idx = 0 
    bb_img = bb_imgs[idx]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
            if kk_rct.colliderect(bb_rct):
                return
                
        screen.blit(bg_img, [0, 0]) 


        idx = min(tmr // 500, 9)     
        bb_img = bb_imgs[idx]     
 
        avx = vx * bb_accs[idx]       
        avy = vy * bb_accs[idx]
        

        original_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = original_center
        
        bb_rct.move_ip(avx, avy)
  

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1] #練習1

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1    
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct) 
        pg.display.update()
        tmr += 1
        clock.tick(50)


        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
