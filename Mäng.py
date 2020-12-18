import sys
import pygame
import random
import math


BLACK = 0, 0, 0
WHITE = 255, 255, 255
LIME = 180, 255, 100
RED = 255, 0, 0
BACKGROUND_BLUE = 4, 176, 216

pygame.init()
aken = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Mäng")
taust = pygame.image.load("taust.png")
kollaneViirus = pygame.image.load("kollaneViirus.png")
oranzViirus = pygame.image.load("oranzViirus.png")
lillakasViirus = pygame.image.load("lillakasViirus.png")
maskiPilt = pygame.image.load("maskiPilt.png")
hanerasv = pygame.image.load("hanerasv.png")
hanerasv = pygame.transform.scale(hanerasv, (60, 170))
kollaneViirus = pygame.transform.scale(kollaneViirus, (80, 80))
oranzViirus = pygame.transform.scale(oranzViirus, (80, 80))
lillakasViirus = pygame.transform.scale(lillakasViirus, (80, 80))
maskiPilt = pygame.transform.scale(maskiPilt, (80, 80))
mehike_paremale = pygame.image.load("mehike.png")
mehike_paremale = pygame.transform.scale(mehike_paremale, (40, 60))
mehike_vasakule = pygame.transform.flip(mehike_paremale, True, False)
font = pygame.font.SysFont('Comic Sans MS', 30)
smallerfont = pygame.font.SysFont('Comic Sans MS', 17)
kasutav_pilt_mehikesest = mehike_paremale
mehike_on_paremale = True

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
maskideArv = 0
skoor = 0
hanerasvaProtsent = 0
iteratsiooniLugeja = 0

pallide_kiirus = 2
kuuli_algus = -70
kuulid = []
süstlad = []


def kaugus(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# võtab parameetriks skooride järjendi ja kirjutab need faili igale reale 1 skoor, kahanevasse järjekorda
def kirjuta_skoorid_faili(skoorid):
    skoorid.sort(reverse=True)  # sorteerime kahanevasse järjekorda
    if len(skoorid) > 10:  # kui on rohkem kui 10 skoori, siis võtame ainult top10
        skoorid = skoorid[:10]
    with open("skoorid.txt", "w") as fail:
        for skoor in skoorid:
            fail.write(str(skoor) + "\n")


# loeb failist kõik skoorid ja tagstab kahanevasse järjekorda sorteeritud järjendi skooridest
def loe_skoorid_failist():
    skoorid = []
    with open("skoorid.txt") as fail:
        for rida in fail:
            skoorid.append(int(rida.strip()))
    skoorid.sort(reverse=True)  # sorteerime kahanevasse järjekorda
    return skoorid


# võtab parameetriks skoori ja lisab selle skooride faili
def uuenda_skoori_faili(lisatav_skoor):
    vanad = loe_skoorid_failist()
    vanad.append(lisatav_skoor)
    kirjuta_skoorid_faili(vanad)


def kasPõrkasKokku(mehikese_rec_x, mehikese_rec_y, mehikese_rec_w, mehikese_rec_h, takistus_center_x, takistus_center_y,takistus_radius):
    # kukkuva objekti kaugus viite erineva punkti kohta mehikesel
    keskeltÜlevalt = kaugus(takistus_center_x, takistus_center_y, mehikese_rec_x + mehikese_rec_w / 2, mehikese_rec_y)
    vasakultÜlevalt = kaugus(takistus_center_x, takistus_center_y, mehikese_rec_x, mehikese_rec_y)
    paremaltÜlevalt = kaugus(takistus_center_x, takistus_center_y, mehikese_rec_x + mehikese_rec_w, mehikese_rec_y)
    vasakultKeskelt = kaugus(takistus_center_x, takistus_center_y, mehikese_rec_x, mehikese_rec_y + mehikese_rec_h / 2)
    paremaltKeskelt = kaugus(takistus_center_x, takistus_center_y, mehikese_rec_x + mehikese_rec_w,mehikese_rec_y + mehikese_rec_h / 2)
    return (keskeltÜlevalt < takistus_radius or vasakultÜlevalt < takistus_radius or paremaltÜlevalt < takistus_radius or paremaltKeskelt < takistus_radius or vasakultKeskelt < takistus_radius)

import pygame.camera

pygame.camera.init()
isCameraFound = len(pygame.camera.list_cameras()) != 0  # Camera detected or not
print(f"Leidsin kaamera: {isCameraFound}")
if isCameraFound:
    cam = pygame.camera.Camera(0, (640, 480))
    cam.start()
    # pygame.image.save(cam.get_image(),"fbi_picture.jpg")


def süstladTeele():
    süstlaid = 9
    vahe = int((600 - süstlaid*60) / (süstlaid-1))
    süstlaX = 0
    for i in range(süstlaid):
        #pygame.draw.rect(aken, BLACK, (süstlaX, 600, 60, 170))
        süstlad.append([hanerasv, süstlaX, 800])
        süstlaX += 60 + vahe


while True:
    hiir_x, hiir_y = pygame.mouse.get_pos()  # hiirepositsioon nuppude vajutamiseks
    aken.blit(taust, [0, 0])  # taustapildi joonistame kõige esimesena igal frameil


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
                iteratsiooniLugeja = 0
                hanerasvaProtsent = 0
                maskideArv = 0
                jagaja = 60  # mida väiksemaks läheb, seda raskemaks muutub mäng
                kella_korrigeerija = pygame.time.get_ticks()  # jätame meelde aja, millal mängu alustati, et saaks aega õigesti arvutada

    # Mängu stseen -----------------------------------------------------------------------------------------------------
    if näita_mäng:
        if mehike_x + mehike_kiirus >= -3 and mehike_x + mehike_kiirus <= 565:  # Ei lase mehikesel aknast välja joosta
            mehike_x += mehike_kiirus

        if mehike_on_paremale:
            mehikese_rec_x = mehike_x + 7
            mehikese_rec_y = 660
            mehikese_rec_w = 40 - 10
            mehikese_rec_h = 60

        else:
            mehikese_rec_x = mehike_x + 3
            mehikese_rec_y = 660
            mehikese_rec_w = 40 - 10
            mehikese_rec_h = 60

        # pygame.draw.rect(aken, BLACK, (mehikese_rec_x + 3, mehikese_rec_y, mehikese_rec_w - 10, mehikese_rec_h))
        aken.blit(kasutav_pilt_mehikesest, (mehike_x, 660))

        # kuvame kõik pallid ekraanile ja muudame nende y koordinaati järgmise framei jaoks
        for i in range(len(kuulid)):
            kuul_pilt = kuulid[i][0]
            kuul_x = kuulid[i][1]
            kuul_y = kuulid[i][2]
            liik = kuulid[i][3]

            if liik == "kollane":
                takistus_center_x = kuul_x + 40
                takistus_center_y = kuul_y + 40
                takistus_radius = 31
            if liik == "oranz":
                takistus_center_x = kuul_x + 40
                takistus_center_y = kuul_y + 40
                takistus_radius = 27
            if liik == "lillakas":
                takistus_center_x = kuul_x + 40
                takistus_center_y = kuul_y + 40
                takistus_radius = 30
            if liik == "mask":
                takistus_center_x = kuul_x + 40
                takistus_center_y = kuul_y + 33
                takistus_radius = 33

            #pygame.draw.circle(aken, BLACK, (takistus_center_x, takistus_center_y), takistus_radius)
            aken.blit(kuul_pilt, (kuul_x, kuul_y))

            kuulid[i] = [kuul_pilt, kuul_x, kuul_y + pallide_kiirus, liik,
                         (takistus_center_x, takistus_center_y, takistus_radius)]

        for s in süstlad:
            aken.blit(s[0], (s[1], s[2]))
            s[2] = s[2] - 4
            if s[2] < -170:
                süstlad.clear()


        # kustutame need pallid järjendist
        eemaldusele = []
        for pall in kuulid:
            if len(süstlad) != 0 and pall[4][1] + pall[4][2] > süstlad[0][2] and pall[3] != "mask":
                eemaldusele.append(pall)

            if pall[2] > 670:  # Kui jõuab maani, siis lisame eemaldusele
                eemaldusele.append(pall)

            if kasPõrkasKokku(mehikese_rec_x, mehikese_rec_y, mehikese_rec_w, mehikese_rec_h, pall[4][0], pall[4][1],
                              pall[4][2]):  # kui põrkab mehikesega kokku
                if pall[0] == kollaneViirus or pall[0] == oranzViirus or pall[0] == lillakasViirus:
                    kuulid.clear()
                    skoor = minutid * 60 + sekundid + maskideArv * 15  # arvutatakse skoor
                    uuenda_skoori_faili(skoor)
                    paremVajutatud = False
                    vasakVajutatud = False
                    näita_mäng = False
                    näita_skoori = True
                if pall[0] == maskiPilt:
                    maskideArv = maskideArv + 1
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
                if hanerasvaProtsent >= 1 and event.key == pygame.K_RETURN:
                    süstladTeele()
                    hanerasvaProtsent = 0
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
            mehike_on_paremale = True
        if vasakVajutatud:
            mehike_kiirus = -3
            kasutav_pilt_mehikesest = mehike_vasakule
            mehike_on_paremale = False

        # Kella kuvamine
        sekundid = int((pygame.time.get_ticks() - kella_korrigeerija) / 1000 % 60)
        minutid = int((pygame.time.get_ticks() - kella_korrigeerija) / 60000 % 24)
        kell = font.render("Aeg: " + str(minutid) + ":" + str(sekundid), False, (0, 0, 0))
        aken.blit(kell, (5, 20))

        tekst_kallesi = font.render("Maske kogutud: " + str(maskideArv), False, (0, 0, 0))
        aken.blit(tekst_kallesi, (5, 50))

        # Pallide lisamine
        if pallide_lisamise_tik % 1000 == 0 and jagaja > 20:  # iga 1000 ühiku tagant teeme raskemaks
            jagaja = jagaja - 10
            print("Jagaja väärtus: " + str(jagaja) + "(mida väiksem, seda raskem)")
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
                    kuulid.append([maskiPilt, x_koordinaad, -60, "mask"])
                else:
                    suvaline = random.randint(0, 2)
                    if suvaline == 0:
                        kuulid.append([kollaneViirus, x_koordinaad, -60, "kollane"])
                    elif suvaline == 1:
                        kuulid.append([oranzViirus, x_koordinaad, -60, "oranz"])
                    else:
                        kuulid.append([lillakasViirus, x_koordinaad, -60, "lillakas"])

        # hanerasva power
        pygame.draw.rect(aken, BLACK, (5, 95, 200, 30))
        pygame.draw.rect(aken, BACKGROUND_BLUE, (8, 98, 194, 24))
        pygame.draw.rect(aken, LIME, (8, 98, 194 * hanerasvaProtsent, 24))
        tekst_powerile = smallerfont.render('POWER MOVE', False, (0, 0, 0))

        aken.blit(tekst_powerile, (48, 98))



        if iteratsiooniLugeja % 10 == 0:
            if hanerasvaProtsent < 1:
                hanerasvaProtsent += 0.005
        iteratsiooniLugeja += 1

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
        aken.blit(tekst1, (300 - tekst1.get_width() / 2, 100))

        skoorid = loe_skoorid_failist()
        for i in range(len(skoorid)):
            taane = 5 - len(str(i + 1))
            t = font.render(str(i + 1) + "." + taane * " " + str(skoorid[i]), False, (0, 0, 0))
            aken.blit(t, (70, 170 + i * 45))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= hiir_x <= 160 and 10 <= hiir_y <= 60:  # kui vajutati tagasi
                näita_edetabelit = False
                näita_algus = True
    # -------------------------------------------------------------------------------------------------------------------

    # igal frameil joonistame uue pildi paremale ülesse nurka
    if isCameraFound:
        img = cam.get_image()
        img = pygame.transform.scale(img, (150, 100))
        aken.blit(img, (600 - 150, 0))

    pygame.display.flip()
    pygame.time.delay(17)
