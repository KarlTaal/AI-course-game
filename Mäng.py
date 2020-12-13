import sys
import pygame
import random

BLACK = 0, 0, 0
WHITE = 255, 255, 255
LIME = 180, 255, 100
RED = 255, 0, 0

pygame.init()
aken = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Mäng")
taust = pygame.image.load("taust.png")
angry = pygame.image.load("angry.png")
happy = pygame.image.load("happy.png")
angry = pygame.transform.scale(angry, (50, 50))
happy = pygame.transform.scale(happy, (50, 50))
mehike_paremale = pygame.image.load("mehike.png")
mehike_paremale = pygame.transform.scale(mehike_paremale, (40, 60))
mehike_vasakule = pygame.transform.flip(mehike_paremale, True, False)
font = pygame.font.SysFont('Comic Sans MS', 30)
kasutav_pilt_mehikesest = mehike_paremale

näita_algus = True
näita_mäng = False
näita_skoori = False
näita_edetabelit = False
mehike_x = 270
mehike_kiirus = 0
vasakVajutatud = False
paremVajutatud = False
kella_korrigeerija = 0
eelnevapalli_x = 0
pallide_lisamise_tik = 0
jagaja = 0
käsnakallesi = 0
skoor = 0

pallide_kiirus = 2
kuuli_algus = -70
kuulid = []

#võtab parameetriks skooride järjendi ja kirjutab need faili igale reale 1 skoor, kahanevasse järjekorda
def kirjuta_skoorid_faili(skoorid):
    skoorid.sort(reverse=True)  # sorteerime kahanevasse järjekorda
    if len(skoorid) > 10:  # kui on rohkem kui 10 skoori, siis võtame ainult top10
        skoorid = skoorid[:10]
    with open("skoorid.txt", "w") as fail:
        for skoor in skoorid:
            fail.write(str(skoor) + "\n")

#loeb failist kõik skoorid ja tagstab kahanevasse järjekorda sorteeritud järjendi skooridest
def loe_skoorid_failist():
    skoorid = []
    with open("skoorid.txt") as fail:
        for rida in fail:
            skoorid.append(int(rida.strip()))
    skoorid.sort(reverse=True)  # sorteerime kahanevasse järjekorda
    return skoorid

#võtab parameetriks skoori ja lisab selle skooride faili
def uuenda_skoori_faili(lisatav_skoor):
    vanad = loe_skoorid_failist()
    vanad.append(lisatav_skoor)
    kirjuta_skoorid_faili(vanad)


import pygame.camera

pygame.camera.init()
isCameraFound = len(pygame.camera.list_cameras()) != 0 #Camera detected or not
print(f"Leidsin kaamera: {isCameraFound}")
if isCameraFound:
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    pygame.image.save(cam.get_image(),"test.jpg")


while True:
    hiir_x, hiir_y = pygame.mouse.get_pos()  # hiirepositsioon nuppude vajutamiseks
    aken.blit(taust, [0, 0])  # taustapildi joonistame kõige esimesena igal frameil



    # igal frameil joonistame uue pildi paremale ülesse nurka
    if isCameraFound:
        img = cam.get_image()
        img = pygame.transform.scale(img, (150, 100))
        aken.blit(img, (600-150, 0))



    # Alguse menüü------------------------------------------------------------------------------------------------------
    if näita_algus:
        tekst_start = font.render('Start', False, (0, 0, 0))
        pygame.draw.rect(aken, BLACK, (220, 345, 160, 60))
        pygame.draw.rect(aken, LIME, (225, 350, 150, 50))
        aken.blit(tekst_start, (260, 350))

        tekst_edetabelid = font.render('Edetabel', False, (0, 0, 0))
        pygame.draw.rect(aken, BLACK, (220, 415, 160, 60))
        pygame.draw.rect(aken, LIME, (225, 420, 150, 50))
        aken.blit(tekst_edetabelid, (240, 420))

        # Jäglime sündmusi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and 225 <= hiir_x <= 375 and 420 <= hiir_y <= 470:  # kui vajutati edetabelit
                näita_algus = False
                näita_edetabelit = True

            if event.type == pygame.MOUSEBUTTONDOWN and 225 <= hiir_x <= 375 and 350 <= hiir_y <= 400:  # kui vajutati starti
                # algseadistame kõik näitajad mänguks ära
                näita_mäng = True
                näita_algus = False
                kuulid.clear()
                mehike_x = 270
                pallide_lisamise_tik = 0
                käsnakallesi = 0
                jagaja = 60  # mida väiksemaks läheb, seda raskemaks muutub mäng
                kella_korrigeerija = pygame.time.get_ticks()  # jätame meelde aja, millal mängu alustati, et saaks aega õigesti arvutada

    # Mängu stseen -----------------------------------------------------------------------------------------------------
    if näita_mäng:
        if mehike_x + mehike_kiirus >= -3 and mehike_x + mehike_kiirus <= 565:  # Ei lase mehikesel aknast välja joosta
            mehike_x += mehike_kiirus
        aken.blit(kasutav_pilt_mehikesest, (mehike_x, 660))

        # kuvame kõik pallid ekraanile ja muudame nende y koordinaati järgmise framei jaoks
        for i in range(len(kuulid)):
            kuul_pilt = kuulid[i][0]
            kuul_x = kuulid[i][1]
            kuul_y = kuulid[i][2]
            aken.blit(kuul_pilt, (kuul_x, kuul_y))
            kuulid[i] = [kuul_pilt, kuul_x, kuul_y + pallide_kiirus]

        # kustutame need pallid järjendist
        eemaldusele = []
        for pall in kuulid:
            if pall[2] > 670:  # Kui jõuab maani, siis lisame eemaldusele
                eemaldusele.append(pall)
            if abs((pall[1] + 25) - (mehike_x + 20)) < 40 and abs(
                    (pall[2] + 25) - 680) < 37:  # kui põrkab mehikesega kokku
                if pall[0] == angry:
                    kuulid.clear()
                    skoor = minutid * 60 + sekundid + käsnakallesi * 15  # arvutatakse skoor
                    uuenda_skoori_faili(skoor)
                    paremVajutatud = False
                    vasakVajutatud = False
                    näita_mäng = False
                    näita_skoori = True
                if pall[0] == happy:
                    käsnakallesi = käsnakallesi + 1
                    eemaldusele.append(pall)

        # eemaldame teises tsüklis, et üle ei jookseks kogemata osadest pallidest
        for pall in eemaldusele:
            # Suurte pallide koguste korral võib errorisse joosta, try except hoiab kokkujooksmise ära
            try:
                kuulid.remove(pall)
            except:
                pass

        # Jälgime sündmusi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    paremVajutatud = True
                if event.key == pygame.K_LEFT:
                    vasakVajutatud = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    paremVajutatud = False
                if event.key == pygame.K_LEFT:
                    vasakVajutatud = False

        # Kui hoitakse nuppu all siis liigutame
        mehike_kiirus = 0
        if paremVajutatud:
            mehike_kiirus = 3
            kasutav_pilt_mehikesest = mehike_paremale
        if vasakVajutatud:
            mehike_kiirus = -3
            kasutav_pilt_mehikesest = mehike_vasakule

        # Kella kuvamine
        sekundid = int((pygame.time.get_ticks() - kella_korrigeerija) / 1000 % 60)
        minutid = int((pygame.time.get_ticks() - kella_korrigeerija) / 60000 % 24)
        kell = font.render("Aeg: " + str(minutid) + ":" + str(sekundid), False, (0, 0, 0))
        aken.blit(kell, (5, 20))

        # Käsnakallede koguse kuvamine
        tekst_kallesi = font.render("Käsna Kallesi " + str(käsnakallesi), False, (0, 0, 0))
        aken.blit(tekst_kallesi, (5, 50))

        # Pallide lisamine
        if pallide_lisamise_tik % 1000 == 0 and jagaja > 20:  # iga 1000 ühiku tagant teeme raskemaks
            jagaja = jagaja - 10
            print("Jagaja väärtus: " + str(jagaja))
        pallide_lisamise_tik = pallide_lisamise_tik + 1
        if pallide_lisamise_tik % jagaja == 0:
            for i in range(2):  # igakord lisatakse nii palju palle korraga kui on range
                arv = random.randint(0, 10)
                x_koordinaad = random.randint(5, 545)
                while abs(
                        eelnevapalli_x - x_koordinaad) < 100:  # otsib uuele pallile koha nii, et ei kattuks väga eelmisega
                    x_koordinaad = random.randint(5, 545)
                eelnevapalli_x = x_koordinaad
                if arv == 4:  # 1 kümnest on spongebob
                    kuulid.append([happy, x_koordinaad, -60])
                else:
                    kuulid.append([angry, x_koordinaad, -60])
    # Kuva skoor peale mängu---------------------------------------------------------------------------------------------
    if näita_skoori:
        tekst1 = font.render('Sinu skoor', False, (0, 0, 0))
        tekst2 = font.render(str(skoor), False, (0, 0, 0))
        tekst3 = font.render("Jätkamiseks vajuta enterit", False, (0, 0, 0))

        aken.blit(tekst1, (300 - tekst1.get_width() / 2, 300))
        aken.blit(tekst2, (300 - tekst2.get_width() / 2, 350))
        aken.blit(tekst3, (300 - tekst3.get_width() / 2, 400))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    näita_algus = True
                    näita_skoori = False
    # Edetabeli vaatamine-----------------------------------------------------------------------------------------------
    if näita_edetabelit:
        tekst_tagasi = font.render('Tagasi', False, (0, 0, 0))
        pygame.draw.rect(aken, BLACK, (5, 5, 160, 60))
        pygame.draw.rect(aken, LIME, (10, 10, 150, 50))
        aken.blit(tekst_tagasi, (35, 10))

        tekst1 = font.render("TOP 10", False, (0, 0, 0))
        aken.blit(tekst1, (300 - tekst1.get_width()/2, 100))

        skoorid = loe_skoorid_failist()
        for i in range(len(skoorid)):
            taane = 5 - len(str(i+1))
            t = font.render(str(i+1) + "." + taane*" " + str(skoorid[i]), False, (0, 0, 0))
            aken.blit(t, (70, 170 + i * 45))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= hiir_x <= 160 and 10 <= hiir_y <= 60:  # kui vajutati tagasi
                näita_edetabelit = False
                näita_algus = True
    #-------------------------------------------------------------------------------------------------------------------
    pygame.display.flip()
    pygame.time.delay(17)