from re import S
import sys
from tkinter import E
import pygame
from pygame.sprite import  Sprite, Group
import time
import os

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1440, 720))
        self.screen_rect = self.screen.get_rect()
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('Giải Cứu Phi Thuyền')
        self.image = pygame.image.load('manhinhchinh.jpg')
        self.image = pygame.transform.scale(self.image, (1440, 720))

        self.phithuyen = PhiThuyen(self)

        self.dan = pygame.sprite.Group()
        self.vu_no = pygame.sprite.Group()

        self.quaivat = pygame.sprite.Group()
        tam =QuaiVat(self)
        self.soquaivat = self.screen.get_width() // (tam.rect.width*2) -1
        self.sohang = 2
        
        self.taoquaivat()

        self.sophithuyen = 3
        

        self.nut_bam = nutbam(self)

        self.dang_choi = False
        self.diem = 0
        self.kyluc = 0
        self.bang_diem = bangdiem(self)
        

        self.clock = pygame.time.Clock()

        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)
        self.ban = pygame.mixer.Sound('shotgun.mp3')
        self.no = pygame.mixer.Sound('exo.mp3')
    
    def taoquaivat(self):
        
        for i in range(self.soquaivat):
            for j in range(self.sohang):
                quaivat = QuaiVat(self)
                quaivat.rect.x = quaivat.rect.width + i*quaivat.rect.width*2
                quaivat.rect.y = quaivat.rect.height + j*quaivat.rect.width*2
                self.quaivat.add(quaivat)
    
    def kiemtra(self):
        for quaivat in self.quaivat.sprites():
            if quaivat.rect.bottom >= self.screen_rect.bottom:
                self.dan.empty()
                self.quaivat.empty()
                self.phithuyen.rect.midbottom = self.screen_rect.midbottom
                self.sophithuyen -=1
                self.bang_diem.tinhsomang(self)
                time.sleep(1)
                self.taoquaivat()
               
                

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.phithuyen.phai = True
                        self.phithuyen.quay_mat = False
                    elif event.key == pygame.K_LEFT:
                        self.phithuyen.trai = True
                        self.phithuyen.quay_mat = True

                    elif event.key == pygame.K_UP:
                        self.phithuyen.tren = True
                    elif event.key == pygame.K_DOWN:
                        self.phithuyen.duoi = True
                    
                    
                    elif event.key == pygame.K_SPACE:
                        n = self.phithuyen.soviendan
                        for i in range(n):
                            dan = Dan(self)
                            w = dan.rect.width
                            dan.rect.x += (-1)**i*w* ((i+n % 2)//2 + ((n+1) % 2)*1/2)
                            self.dan.add(dan)
                        pygame.mixer.Sound.play(self.ban)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.phithuyen.phai = False
                    elif event.key == pygame.K_UP:
                        self.phithuyen.tren = False
                    elif event.key == pygame.K_DOWN:
                        self.phithuyen.duoi = False
                    elif event.key == pygame.K_LEFT:
                        self.phithuyen.trai = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    da_nhan = self.nut_bam.rect.collidepoint(mouse)
                    if da_nhan and not self.dang_choi:
                        self.dang_choi = True
                        self.sophithuyen = 3
                        self.bang_diem.tinhsomang(self)
                        

            self.screen.blit(self.image, (0, 0))
            self.kiemtra()

            if not self.dang_choi:
                self.nut_bam.draw()

            self.phithuyen.draw() 
            self.bang_diem.draw()

            for i in self.dan:
                i.draw()
            for a in self.quaivat:
                a.draw()

            va_cham = pygame.sprite.groupcollide(self.dan, self.quaivat, True, True)
            if va_cham:
                vuno = Vuno(self)
                for vacham in va_cham:
                    vuno.rect.center = vacham.rect.center
                    self.vu_no.add(vuno)
                pygame.mixer.Sound.play(self.no)

                self.diem += 10
                self.bang_diem.tinhdiem(self)
                for i in va_cham.values():
                    self.diem += 10 * len(i)
                self.bang_diem.tinhdiem(self)
                self.bang_diem.kiemtrakyluc(self)

            for vuno in self.vu_no.sprites():
                    vuno.draw()
                    if vuno.xoa is True:
                        self.vu_no.remove(vuno)

            self.vu_no.update()
            
            va_cham1 = pygame.sprite.spritecollideany(self.phithuyen, self.quaivat)
            if va_cham1:
                vuno = Vuno(self)
                vuno.rect.center = va_cham1.rect.center
                self.vu_no.add(vuno)
                pygame.mixer.Sound.play(self.no)
                self.dan.empty()
                self.quaivat.empty()
                self.phithuyen.rect.midbottom = self.screen_rect.midbottom
                self.sophithuyen -= 1
                self.bang_diem.tinhsomang(self)
                print(f'Số phi thuyền: {self.sophithuyen}')
                time.sleep(1)

            for vuno in self.vu_no.sprites():
                    vuno.draw()
                    if vuno.xoa is True:
                        self.vu_no.remove(vuno)
            
            
            # self.dan.empty()
            # self.quaivat.empty()
            # self.phithuyen.rect.midbottom = self.screen_rect.midbottom
            #     # self.sophithuyen -= 1
            #     # print(f'Số phi thuyền: {self.sophithuyen}')
            # time.sleep(1)
            
            if self.sophithuyen == 0:
                self.dang_choi = False
                self.diem =0
                self.bang_diem.tinhdiem(self)
                
                

            if not self.quaivat:
                self.dan.empty()
                self.taoquaivat()

            if self.dang_choi:
                self.phithuyen.update() 
                self.dan.update()
                self.quaivat.update()

            for dan in self.dan:
                if dan.rect.bottom <=0:
                    self.dan.remove(dan)

            for quaivat in self.quaivat:
                if quaivat.rect.right >= self.screen_rect.right:
                    quaivat.phai = False
                    quaivat.trai = True
                    quaivat.rect.y += quaivat.rect.height
                if quaivat.rect.left <= 0:
                    quaivat.phai = True
                    quaivat.trai = False
                    quaivat.rect.y += quaivat.rect.height

            self.clock.tick(60)

            pygame.display.flip()
            
        

class PhiThuyen(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image = pygame.image.load('phithuyen1.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.phai = False
        self.trai = False
        self.tren = False
        self.duoi = False

        self.soviendan = 3
        self.index =0
        self.qua_phai = []
        self.qua_trai = []
        self.quay_mat = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.phai == True and self.rect.right < self.screen_rect.right:
            self.rect.x +=5
        elif self.trai == True and self.rect.left > 0:
            self.rect.x -=5
        elif self.tren == True and self.rect.top > 0:
            self.rect.y -=5
        elif self.duoi == True and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y +=5

        self.amanition()

    def lay_anh(self, path):
        ds_anh_phai = []
        ds_anh_trai = []

        for _,_, files in os.walk(path):
            for file in files:
                img = pygame.image.load(path + '/' + file)
                ds_anh_phai.append(img)
                img = pygame.transform.flip(img ,True, False)
                ds_anh_trai.append(img)
        return ds_anh_phai, ds_anh_trai

    def amanition(self):
        self.qua_phai ,self.qua_trai= self.lay_anh('./rote/')
        if self.quay_mat is False:

         if self.phai is True:
            self.image =self.qua_phai[self.index]
            self.index +=1
            if self.index == len(self.qua_phai):
                self.index -= 1
         else:
            self.canbang()
        
        else:

         if self.trai is True:
            self.image = self.qua_trai[self.index]
            self.index += 1
            if self.index == len(self.qua_phai):
                self.index -= 1
         else:
             self.canbang()

    def canbang(self):
        while self.index >= 0:
            self.image = self.qua_phai[self.index]
            self.index -=1
        self.index =0

class Dan(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load('dan1.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = game.phithuyen.rect.midtop 
    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y -=5 

class QuaiVat(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load('alien.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = self.screen_rect.midtop 
        self.phai = True
        self.trai = False
    def draw(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        if self.phai is True:
            self.rect.x += 2
        elif self.trai is True:
            self.rect.x -= 2
        
class nutbam:

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.rect = pygame.Rect(0, 0, 100, 50)
        self.rect.center = self.screen_rect.center

        self.image = pygame.image.load('2.png')
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.screen_rect.center

    def draw(self):
        # self.screen.fill('', self.rect)
        self.screen.blit(self.image, self.image_rect)


class Vuno(Sprite):
    def __init__(self,game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.xoa = False

        self.ds_anh =[]

        for _,_, files in os.walk('./Exposion'):
            for  file in files:
                img = pygame.image.load('./Exposion/' + file)
                img = pygame.transform.scale(img, (75,75))
                self.ds_anh.append(img)
        
        self.index =0
        self.image = self.ds_anh[self.index]
        self.rect =self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.index += 1
        if self.index == len(self.ds_anh) - 1:
            self.xoa = True
        self.image = self.ds_anh[self.index]

class bangdiem:
    def __init__(self,game):
        self.screen= game.screen
        self.screen_rect = game.screen.get_rect()
        self.font = pygame.font.Font(None, 50)
        self.color = (255, 255, 255)
        # self.bgcolor = (0, 0, 0)
        self.tinhdiem(game)
        self.tinhkyluc(game)
        self.kiemtrakyluc(game)
        self.tinhsomang(game)
        

    def tinhdiem(self, game):
        self.text = self.font.render(str(game.diem) ,True, self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.x = 10
        self.text_rect.y = 10


    def tinhkyluc(self, game):
        self.kyluc = self.font.render(str(game.kyluc), True,self.color)
        self.kyluc_rect = self.kyluc.get_rect()
        self.kyluc_rect.midtop = game.screen_rect.midtop
        

    def kiemtrakyluc(self, game):
        if game.diem > game.kyluc:
            game.kyluc = game.diem
            self.tinhkyluc(game)
        
    def tinhsomang(self, game):
        self.phi_thuyen = Group()
        for i in range(game.sophithuyen):
            phi_thuyen = PhiThuyen(game)
            phi_thuyen.rect.topright = game.screen_rect.topright
            phi_thuyen.rect.x -= i* phi_thuyen.rect.width
            self.phi_thuyen.add(phi_thuyen)

    def draw(self):
        self.screen.blit(self.text ,self.text_rect)
        self.screen.blit(self.kyluc, self.kyluc_rect)
        self.phi_thuyen.draw(self.screen)


if __name__ == '__main__':
    game = Game()
    game.main()