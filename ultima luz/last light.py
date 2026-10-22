#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÚLTIMA LUZ - (Teclado + Controle iPega USB) & Tela Cheia com Pause e Música
"""

import math
import random
import sys
import pygame

# CONSTANTES E CONFIGURAÇÕES DE TELA
W, H = 1024, 720
FPS = 60

CABIN = pygame.Rect(520, 300, 160, 120)
PANEL_W = 330
HORTA = pygame.Rect(400, 455, 130, 62)
ENFERMARIA = pygame.Rect(395, 295, 84, 56)
OFICINA = pygame.Rect(715, 440, 92, 62)
TORRE = pygame.Rect(722, 262, 38, 38)

GOLD = (255, 214, 120)
WHITE = (235, 235, 240)
GREY = (150, 150, 160)
DGREY = (80, 80, 90)
RED = (205, 60, 60)
GREEN = (90, 190, 100)
BLUE = (90, 160, 255)

CHAR_COL = {
    "Gabriel": (90, 160, 255),
    "Rafael": (230, 110, 60),
    "Livia": (235, 235, 245),
    "Miguel": (240, 210, 70),
    "Helena": (110, 200, 110),
    "Daniel": (150, 165, 200),
    "Caio": (170, 120, 80),
    "Elisa": (205, 130, 205),
}

HOMES = {
    "Rafael": (600, 450),
    "Livia": (545, 458),
    "Miguel": (668, 455),
    "Daniel": (705, 410),
    "Helena": (520, 425),
    "Caio": (625, 440),
    "Elisa": (700, 475),
}

MON = {
    "andarilho": dict(hp=30, speed=68, r=10, cab=4, hit=9, col=(120, 150, 110)),
    "corredor": dict(hp=48, speed=160, r=12, cab=7, hit=7, col=(195, 90, 80)),
    "brutamontes": dict(hp=240, speed=36, r=25, cab=26, hit=26, col=(115, 80, 105)),
    "gritador": dict(hp=58, speed=38, r=11, cab=0, hit=0, col=(205, 205, 120)),
    "observador": dict(hp=70, speed=120, r=11, cab=0, hit=18, col=(90, 70, 130)),
}

NIGHTS = {
    1: dict(title="NOITE 1: O MEDO", mons=[("andarilho", 20), ("corredor", 10)], gap=2.6, special=[], allies=["Rafael"]),
    2: dict(title="NOITE 2: UNIÃO", mons=[("andarilho", 22), ("corredor", 15)], gap=2.2, special=[], allies=["Rafael", "Livia", "Miguel", "Daniel", "Helena"]),
    3: dict(title="NOITE 3: A PRIMEIRA FERIDA", mons=[("andarilho", 14), ("corredor", 8)], gap=2.0, special=[("EVENTO_FERIDA", 0.5)], allies=["Rafael", "Livia", "Miguel", "Daniel", "Helena"]),
    4: dict(title="NOITE 4: O GRITO", mons=[("andarilho", 30), ("corredor", 20)], gap=2.0, special=[("gritador", 0.2)], allies=["Rafael", "Livia", "Miguel", "Daniel", "Helena"]),
    5: dict(title="NOITE 5: A PRIMEIRA PERDA", mons=[("andarilho", 30), ("corredor", 30)], gap=1.9, special=[("brutamontes", 0.45)], allies=["Rafael", "Livia", "Daniel", "Caio"]),
    6: dict(title="NOITE 6: O QUE NOS OBSERVA", mons=[("andarilho", 18), ("corredor", 40)], gap=1.8, special=[("observador", 0.12), ("gritador", 0.35), ("brutamontes", 0.55), ("brutamontes", 0.85)], allies=["Rafael", "Livia", "Miguel", "Daniel", "Helena"]),
}

BARKS = {
    "Miguel": ["Esse aí tinha cara de segunda-feira.", "Alguém avisa que eu errei de propósito.", "Se eu morrer, quero um funeral com bolo.", "Eles não têm nenhum senso de humor."],
    "Rafael": ["Ninguém passa!", "Enquanto eu estiver de pé!", "Segura a linha, Gabriel!"],
    "Daniel": ["A barricada não vai aguentar muito.", "Eu consigo consertar... por enquanto.", "Não adianta. Eles não acabam."],
    "Helena": ["A luz incomoda eles!", "Eles vão embora. Sempre vão.", "Amanhã tem sol, Gabriel."],
    "Livia": ["Se você se machucar, vem me procurar!", "Fica perto de mim se precisar!"],
    "Caio": ["Eu seguro a porta!", "Podem ir. Eu fico aqui."],
    "Elisa": ["Eu protejo a minha família!"],
}

SCENES = {
    "intro": [
        ("S", "Escuro."),
        ("S", "Uma respiração pesada, distante."),
        ("S", "Gritos."),
        ("S", "Algo está correndo do lado de fora."),
        ("N", "Gabriel se levanta, e abre a porta."),
        ("N", "Do outro lado, uma pequena cabana cercada por uma floresta. Outras pessoas estão ali."),
        ("N", "Não são soldados. Não são heróis. São apenas pessoas tentando sobreviver."),
        ("Rafael", "Ei, calma. Você está bem?"),
        ("Gabriel", "Estou."),
        ("N", "Claramente, ele não está pois seria uma mudança em sua vida ."),
        ("Rafael", "Meu nome é Rafael. Fui bombeiro. Você fica aqui com a gente."),
        ("Livia", "Eu sou a Lívia. Eu cuido dos feridos. A cabana está em ruínas, mas é tudo que temos."),
        ("Rafael", "De dia, a gente se prepara. De noite, a gente defende a cabana."),
        ("Rafael", "Toda noite eles aparecem. E a cada noite são mais."),
        ("Rafael", "Teremos que continuar, ah criançãs e idosos a salvar."),
    ],
    "pre1": [("T", "NOITE 1: O MEDO"), ("Gabriel", "Quantos são?"), ("Rafael", "Não sei"), ("Gabriel", "Como assim?"), ("Rafael", "Importa quantos de nós ainda estaremos aqui quando amanhecer.")],
    "post1": [("N", "O sol nasce. A primeira noite termina."), ("Livia", "Deixa eu ver esse braço."), ("Gabriel", "Estou bem."), ("Livia", "Feridas não desaparecem porque fingimos que elas não existem."), ("N", "Pela primeira vez, Gabriel deixa alguém cuidar dele.")],
    "pre2": [("T", "NOITE 2: UNIÃO"), ("Daniel", "A barricada aguenta mais uma noite. Talvez."), ("Rafael", "Gabriel, fica comigo na frente."), ("Gabriel", "Eu? Eu nem sei direito o que estou fazendo."), ("Rafael", "Ninguém sabia. Vem."), ("Miguel", "Eu fico atirando de longe. Se eu errar, é de propósito."), ("Helena", "Eu fico com a lanterna. Eles não gostam de luz."), ("Livia", "E eu fico perto da cabana. Se você cair, eu te levanto.")],
    "post2": [("N", "Pela primeira vez, ninguém se feriu gravemente."), ("Rafael", "Hoje eu confiei nas suas costas, Gabriel."), ("Gabriel", "Eu não consigo fazer isso sozinho."), ("Rafael", "Ninguém consegue. Por isso estamos aqui."), ("N", "Do lado de fora da cabana, Helena enterra pequenas sementes na terra."), ("Daniel", "Isso é inútil. Você sabe, né?"), ("Helena", "Se não acreditarmos no amanhã, então já perdemos hoje."), ("Miguel", "Eu voto no amanhã. Principalmente se tiver comida.")],
    "pre3": [("T", "NOITE 3: A PRIMEIRA FERIDA"), ("Rafael", "Hoje vai ser pior ."), ("Livia", "Eu estou aqui para, Gabriel."), ("Gabriel", "Estou bem.")],
    "post3": [("N", "Gabriel acorda na enfermaria improvisada. Tudo dói."), ("Gabriel", "Eu só estou atrapalhando vocês."), ("Livia", "Você não precisa ser útil o tempo inteiro para merecer ficar aqui."), ("N", "Gabriel não responde. Mas, por hoje, ele aceita ficar."), ("N", "(Ferido, Gabriel terá menos energia amanhã.)")],
    "pre4": [("T", "NOITE 4: O GRITO"), ("Daniel", "Esse silêncio lá fora não é normal."), ("Rafael", "Fiquem atentos. Todo mundo.")],
    "post4": [("N", "A cabana quase caiu. Centenas de criaturas, atraídas por um único grito."), ("N", "Gabriel entra na cabana e se senta no chão. As mãos tremem."), ("Gabriel", "Eu não consigo mais."), ("N", "Rafael senta ao lado dele."), ("Rafael", "Então não consiga sozinho.")],
    "pre5": [("T", "NOITE 5: A PRIMEIRA PERDA"), ("N", "Caio chegou há poucos dias. Quase não fala."), ("Caio", "Eu fico na entrada. Alguém precisa ficar."), ("Rafael", "Não precisa ser você."), ("Caio", "Alguém precisa ser. Pode ser eu.")],
    "post5": [("S", "Não existe música."), ("S", "Não existe discurso."), ("S", "Apenas silêncio."), ("S", "Naquela noite, uma cadeira fica vazia dentro da cabana.")],
    "familia": [("T", "DIA 6"), ("N", "Durante a exploração, o grupo encontra uma família escondida em um porão."), ("Elisa", "Por favor. Só precisamos de um lugar para passar a noite. Somos três."), ("N", "Uma mãe, um pai e uma criança. Levá-los significa gastar comida, remédios e munição."), ("Rafael", "A decisão é sua, Gabriel.")],
    "ajudou": [("Gabriel", "Venham. Tem espaço para vocês."), ("Elisa", "Obrigada. De verdade."), ("N", "A cabana fica mais cheia. Os recursos diminuem. Mas agora há mais mãos para ajudar nas tarefas.")],
    "nao_ajudou": [("Gabriel", "Sinto muito. Nós não temos o suficiente."), ("N", "Os recursos são preservados. Mas as palavras de Gabriel ficam com ele."), ("Gabriel", "Eu fiz a coisa certa. Não fiz?"), ("Rafael", "Não existe resposta certa. Só existe a que você consegue carregar.")],
    "fim": [("N", "Seis noites. Seis amanheceres."), ("N", "Entre os registros recuperados, um nome se repete: PROJETO AURORA."), ("Gabriel", "O que isso quer dizer?"), ("Daniel", "Que a gente nunca esteve tão longe do que eles são."), ("Helena", "Ou que a gente também pode amplificar o que existe de bom."), ("N", "Na cabana, a pequena lâmpada continua acesa."), ("T", "FIM DA PARTE 1")],
}

RECORDS = [
    [("N", "Documento encontrado: PROJETO AURORA (1/3)."), ("N", "MEMORANDO INTERNO: Objetivo do projeto desenvolver uma tecnologia capaz de regenerar tecidos humanos."), ("Gabriel", "Então foi isso que começou tudo...")],
    [("N", "Documento encontrado: PROJETO AURORA (2/3)."), ("N", "RELATÓRIO DE FALHA: O protocolo falhou. Uma mutação começou a se espalhar entre os voluntários. Não conseguimos contê-la."), ("Livia", "Eles sabiam. Desde o começo, eles sabiam.")],
    [("N", "Documento encontrado: PROJETO AURORA (3/3)."), ("N", "Nota final, escrita à mão: 'A infecção não cria monstros. Ela amplifica aquilo que já existe.'"), ("Gabriel", "Aquilo que já existe... Isso muda tudo.")],
]

TALK_ORDER = ["Rafael", "Livia", "Miguel", "Helena", "Daniel"]
TALKS = {
    "Rafael": [
        [("Rafael", "Eu era bombeiro. Entrava onde todo mundo saía."), ("Rafael", "Nem sempre consegui voltar com todos. Não gosto de falar disso."), ("Gabriel", "Você não precisa falar.")],
        [("Rafael", "Enquanto eu estiver de pé, ninguém passa. É só isso que eu sei fazer."), ("Gabriel", "E quando você precisar descansar?"), ("Rafael", "...Aí eu aviso.")],
        [("Rafael", "Você está diferente, Gabriel. Já não finge tanto."), ("Gabriel", "Estou aprendendo."), ("Rafael", "Então já aprendeu mais do que eu em anos.")],
    ],
    "Livia": [
        [("Livia", "Eu era enfermeira. Cuidar dos outros me impede de pensar demais."), ("Gabriel", "E quem cuida de você?"), ("Livia", "...Boa pergunta.")],
        [("Livia", "Pode se sentar. Eu só quero olhar esse curativo."), ("Gabriel", "Estou bem."), ("Livia", "Você sempre diz isso. Eu sempre confiro.")],
        [("Livia", "Cuidar dos outros é a maneira mais honesta que eu conheço de ter esperança."), ("Gabriel", "Obrigado, Lívia.")],
    ],
    "Miguel": [
        [("Miguel", "Sabe qual é a diferença entre um zumbi e a minha ex? O zumbi pelo menos aparece."), ("Gabriel", "Isso foi horrível."), ("Miguel", "Eu sei. Estou treinando.")],
        [("Miguel", "Eu sempre faço piada. Perguntam por quê."), ("Gabriel", "Por quê?"), ("Miguel", "Porque se eu parar de rir, aí eu tenho que pensar. Esquece. Outra piada!")],
        [("Miguel", "Se alguma coisa acontecer comigo, você ri por mim, tá?"), ("Gabriel", "Não vai acontecer nada."), ("Miguel", "Claro que não. Eu sou o mais bonito do grupo.")],
    ],
    "Helena": [
        [("Helena", "Eu era professora. Eu ensinava crianças a imaginarem o futuro."), ("Helena", "Quando tudo isso acabar, o que você vai fazer, Gabriel?"), ("Gabriel", "Eu nunca pensei nisso.")],
        [("Helena", "Essas sementes demoram semanas. Mas amanhã elas ainda vão estar aqui."), ("Gabriel", "E se a gente não estiver?"), ("Helena", "Então alguém colhe por nós.")],
        [("Helena", "Se não acreditarmos no amanhã, então já perdemos hoje."), ("Gabriel", "Eu quero acreditar."), ("Helena", "Já é um começo.")],
    ],
    "Daniel": [
        [("Daniel", "Eu conserto geradores, portas, armas. Mas não conserto o final dessa história."), ("Gabriel", "Você acha que não tem final feliz?"), ("Daniel", "Eu acho que não. Mas eu continuo consertando.")],
        [("Daniel", "Não me peça para ter esperança. Peça para eu consertar a porta."), ("Gabriel", "Combinado."), ("Daniel", "Esse eu consigo.")],
        [("Daniel", "Sabe o que é engraçado? Eu acordo todo dia achando que é o último."), ("Daniel", "E todo dia eu continuo. Não sei por quê."), ("Gabriel", "Talvez você saiba, sim.")],
    ],
}

def clamp(v, a, b):
    return max(a, min(b, v))

def dist(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

def closest_on_rect(r, x, y):
    return clamp(x, r.left, r.right), clamp(y, r.top, r.bottom)

def wrap(text, font, maxw):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.size(t)[0] <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_text(surf, text, font, color, pos, anchor="topleft", shadow=True):
    if not text:
        return pygame.Rect(pos, (0, 0))
    img = font.render(text, True, color)
    r = img.get_rect(**{anchor: pos})
    if shadow:
        sh = font.render(text, True, (0, 0, 0))
        surf.blit(sh, (r.x + 2, r.y + 2))
    surf.blit(img, r)
    return r

def make_light(radius):
    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        a = int(235 * (1 - r / radius) ** 0.7)
        pygame.draw.circle(s, (255, 255, 255, a), (radius, radius), r)
    return s

def make_glow(radius, color, amax):
    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        a = int(amax * (1 - r / radius) ** 2)
        pygame.draw.circle(s, (*color, a), (radius, radius), r)
    return s

def draw_bar(surf, font, x, y, w, h, frac, col, label):
    pygame.draw.rect(surf, (20, 20, 26), (x, y, w, h), border_radius=4)
    pygame.draw.rect(surf, col, (x, y, int(w * clamp(frac, 0, 1)), h), border_radius=4)
    pygame.draw.rect(surf, (200, 200, 210), (x, y, w, h), 1, border_radius=4)
    draw_text(surf, label, font, WHITE, (x + 6, y + h // 2), "midleft")

SPR = {}
BODY = [
    "..HHHH....",
    ".HHHHHH...",
    "..HHHHHHHH..",
    "..HSSSSSSH..",
    "..SSESSESS..",
    "..SSSSSSSS..",
    "...SSMMSS...",
    "....SSSS....",
    "..CCCCCCCC..",
    ".CCCCCCCCCC.",
    ".SCCCCCCCCS.",
    ".SCCCCCCCCS.",
    "..CCCCCCCC..",
    "..PPPPPPPP..",
    "..PP....PP..",
    "..BB....BB..",
]
BASEPAL = dict(H=(80, 55, 35), S=(225, 180, 145), E=(30, 25, 30), M=(150, 70, 70), C=(100, 100, 120), P=(60, 60, 80), B=(35, 28, 28), X=(255, 255, 255))
HUMANS = {
    "Gabriel": (dict(H=(80, 55, 35), C=(70, 120, 200), P=(60, 60, 85)), []),
    "Rafael": (dict(H=(200, 50, 40), S=(210, 165, 130), C=(185, 95, 45), P=(55, 55, 65), X=(255, 210, 70)), [(x, 2, "X") for x in range(2, 10)]),
    "Livia": (dict(H=(120, 80, 60), C=(235, 235, 240), P=(90, 120, 150), X=(210, 40, 40)), [(5, 9, " "), (6, 9, "X"), (4, 10, "X"), (5, 10, " "), (6, 10, "X"), (7, 10, "X"), (5, 11, " "), (6, 11, "X")]),
    "Miguel": (dict(H=(50, 35, 25), C=(240, 200, 60), P=(50, 70, 120), S=(235, 190, 155)), [(4, 6, "M"), (7, 6, "M")]),
    "Helena": (dict(H=(95, 55, 32), C=(90, 170, 100), P=(75, 62, 52), X=(50, 35, 30)), [(1, 4, "H"), (10, 4, "H"), (1, 5, "H"), (10, 5, "H"), (1, 6, "H"), (10, 6, "H"), (3, 4, "X"), (5, 4, "X"), (6, 4, "X"), (8, 4, " ")]),
    "Daniel": (dict(H=(90, 95, 110), S=(200, 160, 130), C=(90, 105, 140), P=(60, 70, 100), X=(60, 60, 70)), [(2, 3, "X"), (9, 3, " ")]),
    "Caio": (dict(H=(60, 40, 25), C=(150, 105, 70), P=(70, 60, 50)), []),
    "Elisa": (dict(H=(70, 40, 70), C=(190, 120, 190), P=(70, 70, 100)), []),
}

MONSPR = {
    "andarilho": ([
        "..GGGG....", "...GGGGGG...", "...GEGGEG...", "...GGMMGG...",
        "GG.CCCCCC.GG", "GG.CCCCCC.GG", ".G.CCCCCC.G.", "...CCCCCC...",
        "...PP..PP...", "...PP..PP...", "...BB..BB...", "...GGGG....",
    ], dict(G=(120, 150, 110), E=(255, 60, 60), M=(50, 20, 20), C=(95, 80, 70), P=(60, 60, 70), B=(30, 28, 30)), 2),
    "corredor": ([
        "..GGG.....", "....GGGGG...", "....GEGEG...", "....GGMGG...",
        "..CCCCCC..", ".CCCCCCCC.GG", "GG.CCCC..GG.", "...GGG......",
        "..PP..PP..", ".PP....PP...", "..BB..BB....", "...CCCC.....",
    ], dict(G=(195, 100, 90), E=(255, 230, 80), M=(60, 15, 15), C=(110, 60, 55), P=(55, 50, 60), B=(30, 28, 30)), 2),
    "brutamontes": ([
        "..GGGG....", "..GGGGGG....", "..GEGGEG....", "..GGMMGG....",
        "..GGGG....", ".GGGCCCCCCGGG.", ".GGGGCCCCCCGGGG.", ".GGGGCCCCCCGGGG.",
        "GGGGGCCCCCCGGGGG", "GGGGGCCCCCCGGGGG", "..GG.CCCCCC.GG..", "GGGGGCCCCCCGGGGG",
        ".PPPPPP...", "....PP..PP..", ".PP..PP...", "..BB..BB....",
    ], dict(G=(125, 85, 115), E=(255, 90, 60), M=(40, 15, 25), C=(80, 60, 80), P=(55, 45, 60), B=(30, 28, 30)), 3),
    "gritador": ([
        "...GGGG....", "...GGGGGG...", "..GGEGGEGG..", "...GGMMGG...",
        "..GGMMMMGG..", ".G.CCCCCC.G.", "...CCCCcc...", "..cccccccc..",
        ".GCCCCCCCCG.", "...PP..PP...", "..GGMMMMGG..", "...BB..BB...",
    ], dict(G=(205, 205, 150), E=(255, 60, 60), M=(40, 10, 10), C=(120, 110, 90), P=(70, 65, 70), B=(30, 28, 30)), 2),
    "observador": ([
        "..DDDD....", "...DDDDDD...", "..DDDDDDDD..", "..DEEDDEED..",
        "..DEEDDEED..", "..DDDDDDDD..", "..DDDMMDDD..", "...DDDDDD...",
        "..DDDDDDDD..", ".DD.DDDD.DD.", ".D..DDDD..D.", "...D..D.....",
    ], dict(D=(60, 45, 95), E=(255, 220, 90), M=(20, 10, 30)), 2),
}

def build_pixel(grid, pal, scale, overrides=None):
    g = [list(r) for r in grid]
    for x, y, ch in overrides or []:
        if y < len(g) and 0 <= x < len(g[0]):
            g[y][x] = ch
    h, w = len(g), len(g[0])
    s = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
    for y in range(h):
        for x in range(w):
            c = pal.get(g[y][x])
            if c:
                s.set_at((x + 1, y + 1), c)
    base = s.copy()
    for y in range(h + 2):
        for x in range(w + 2):
            if base.get_at((x, y))[3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w + 2 and 0 <= ny < h + 2 and base.get_at((nx, ny))[3] > 0:
                        s.set_at((x, y), (14, 10, 18))
                        break
    return pygame.transform.scale(s, ((w + 2) * scale, (h + 2) * scale))

def build_sprites():
    SPR.clear()
    for name, (over_pal, over) in HUMANS.items():
        pal = dict(BASEPAL)
        pal.update(over_pal)
        body = build_pixel(BODY, pal, 2, over)
        SPR[name] = dict(
            body=body,
            flip=pygame.transform.flip(body, True, False),
            med=build_pixel(BODY, pal, 3, over),
            portrait=build_pixel(BODY[0:12], pal, 9, over)
        )
    for kind, (grid, pal, scale) in MONSPR.items():
        body = build_pixel(grid, pal, scale)
        SPR[kind] = dict(body=body, flip=pygame.transform.flip(body, True, False))

def draw_person(surf, font, name, x, y, r=11, t=0.0):
    sp = SPR.get(name)
    if sp:
        pygame.draw.ellipse(surf, (0, 0, 0), (int(x) - 10, int(y) + 10, 20, 7))
        img = sp["body"]
        surf.blit(img, img.get_rect(midbottom=(int(x), int(y) + 16)))
        return
    col = CHAR_COL.get(name, (200, 200, 200))
    pygame.draw.circle(surf, col, (int(x), int(y)), r)
    draw_text(surf, name[0], font, (20, 20, 20), (int(x), int(y)), "center", shadow=False)

class Story:
    def __init__(self, lines, on_done):
        self.lines = lines
        self.on_done = on_done
        self.i = 0
        self.t = 0.0

    def cur(self):
        return self.lines[self.i]

    def cps(self):
        return 20 if self.cur()[0] == "S" else 55

    def typed_all(self):
        k, text = self.cur()
        return k == "T" or int(self.t * self.cps()) >= len(text)

    def advance(self):
        if not self.typed_all():
            self.t = 999
            return
        self.next()

    def next(self):
        self.i += 1
        self.t = 0.0
        if self.i >= len(self.lines):
            cb = self.on_done
            self.on_done = None
            if cb:
                cb()

    def skip_all(self):
        cb = self.on_done
        self.on_done = None
        self.i = len(self.lines) - 1
        if cb:
            cb()

    def update(self, dt):
        self.t += dt
        if self.cur()[0] == "T" and self.t > 3.0:
            self.next()

class Night:
    def __init__(self, g, n, aftermath=False):
        self.g = g
        self.n = n
        self.aftermath = aftermath
        cfg = NIGHTS[n]
        self.cfg = cfg
        self.px, self.py = 600.0, 485.0
        
        # Jogador 2 (Rafael - Co-op Controle USB / iPega)
        self.p2_x, self.p2_y = 560.0, 485.0
        self.p2_aim = 0.0
        self.p2_shoot_cd = 0.0
        self.p2_melee_cd = 0.0
        self.p2_melee_t = 0.0

        self.hp = float(g.hp)
        if g.hungry and not aftermath:
            self.hp = max(20.0, self.hp - 15)
        self.ammo = g.res["municao"]
        self.cabin_max = float(g.cabin_max)
        self.cabin_hp = float(g.cabin_max)
        self.dmg_mult = (1 + 0.25 * g.weapon) * (1 + g.morale / 400.0)
        self.speed = 190.0
        self.wounded = False
        self.shoot_cd = 0.0
        self.melee_cd = 0.0
        self.melee_t = 0.0
        self.iframes = 0.0
        self.aim = 0.0
        self.monsters = []
        self.bullets = []
        self.parts = []
        self.pickups = []
        self.barks = []
        self.banner = None
        self.shake = 0.0
        self.red = 0.0
        self.white = 0.0
        self.muzzle = 0.0
        self.p2_muzzle = 0.0
        self.time = 0.0
        self.state = "play"
        self.end_t = 0.0
        self.paused = False
        self.no_ammo_msg = 0.0
        self.lamp_flick = 0
        self.tower = "torre" in g.built
        self.allies = []
        self.queue = []
        self.spawn_t = 2.0
        self.extra_alert = False

        if aftermath:
            return

        names = list(cfg["allies"])
        if n == 6 and g.helped_family:
            names.append("Elisa")
        if "Rafael" in names:
            names.remove("Rafael")

        for name in names:
            hx, hy = HOMES[name]
            self.allies.append(dict(name=name, x=float(hx), y=float(hy), hx=hx, hy=hy, cd=random.random(), bark=random.uniform(6, 14)))

        base = []
        for kind, cnt in cfg["mons"]:
            base += [kind] * cnt
        random.shuffle(base)
        for kind, frac in cfg["special"]:
            base.insert(int(frac * len(base)), kind)

        self.queue = base
        self.total = len([k for k in base if not k.startswith("EVENTO")])

        if g.hungry:
            self.say("Narrador", "Todos dormiram com fome. Gabriel começa a noite mais fraco.")
        if n == 1:
            self.banner = ("J1: WASD+Mouse | J2: Controle ", 9.0)

    def say(self, who, text, t=4.5):
        self.barks.append([who, text, t])
        self.barks = self.barks[-3:]

    def edge_pos(self):
        side = random.randint(0, 3)
        if side == 0:
            return random.uniform(0, W), -30
        if side == 1:
            return random.uniform(0, W), H + 30
        if side == 2:
            return -30, random.uniform(0, H)
        return W + 30, random.uniform(0, H)

    def spawn(self, kind, x=None, y=None):
        if x is None:
            x, y = self.edge_pos()
        d = MON[kind]
        boost = self.n - 1
        hp = d["hp"] * (1 + 0.06 * boost)
        m = dict(kind=kind, x=float(x), y=float(y), hp=hp, maxhp=hp,
                 speed=d["speed"] * (1 + 0.04 * boost), r=d["r"], cab=d["cab"] * (1 + 0.05 * boost),
                 hit=d["hit"], cd=random.random(), kx=0.0, ky=0.0, flash=0.0,
                 state="normal", timer=random.uniform(5, 8), scream=6.0,
                 dash=0.0, dx=0.0, dy=0.0, face=0.0)
        if kind == "gritador":
            m["state"] = "observe"
        self.monsters.append(m)
        return m

    def blood(self, x, y, n=6, col=(120, 20, 20), spd=140):
        for _ in range(n):
            a = random.uniform(0, 6.283)
            s = random.uniform(30, spd)
            self.parts.append([x, y, math.cos(a) * s, math.sin(a) * s, random.uniform(0.25, 0.6), col, random.randint(2, 4)])

    def nearest(self, x, y, rng, only_visible=False):
        best, bd = None, rng
        for m in self.monsters:
            d = dist(x, y, m["x"], m["y"]) - m["r"]
            if d < bd:
                best, bd = m, d
        return best

    def read_input(self):
        k = pygame.key.get_pressed()
        
        # Jogador 1 (Gabriel) - Teclado e Mouse
        dx_p1 = (1 if k[pygame.K_d] else 0) - (1 if k[pygame.K_a] else 0)
        dy_p1 = (1 if k[pygame.K_s] else 0) - (1 if k[pygame.K_w] else 0)
        mx, my = self.g.get_virtual_mouse_pos()
        mb = pygame.mouse.get_pressed()
        shoot_p1 = bool(mb[0])
        melee_p1 = bool(k[pygame.K_SPACE] or mb[2])

        # Jogador 2 (Rafael) - Controle USB Focado (iPega)
        dx_p2, dy_p2 = 0.0, 0.0
        aim_p2_x, aim_p2_y = 1.0, 0.0
        shoot_p2 = False
        melee_p2 = False

        if self.g.joystick:
            # Analógico Esquerdo (Movimento)
            dx_p2 = self.g.joystick.get_axis(0)
            dy_p2 = self.g.joystick.get_axis(1)
            if abs(dx_p2) < 0.15: dx_p2 = 0.0
            if abs(dy_p2) < 0.15: dy_p2 = 0.0

            # Analógico Direito (Mira)
            if self.g.joystick.get_numaxes() > 3:
                aim_p2_x = self.g.joystick.get_axis(2)
                aim_p2_y = self.g.joystick.get_axis(3)
                if abs(aim_p2_x) < 0.2 and abs(aim_p2_y) < 0.2:
                    aim_p2_x, aim_p2_y = 1.0, 0.0
            
            # Botões do Gamepad USB
            if self.g.joystick.get_numbuttons() > 0:
                shoot_p2 = self.g.joystick.get_button(5) or self.g.joystick.get_button(7)
                melee_p2 = self.g.joystick.get_button(0) or self.g.joystick.get_button(2)
        # Se o comando NÃO estiver conectado, o Rafael age como um NPC autónomo
        else:
            # Tenta encontrar o monstro mais próximo utilizando a posição atual do Rafael (self.p2_x, self.p2_y)
            # Nota: Podes usar as variáveis de posição do Jogador 2 para centrar a busca
            alvo = self.nearest(self.p2_x, self.p2_y, 300, only_visible=False)
            
            if alvo:
                # Calcula a direção (vetor) em direção ao monstro
                import math
                diff_x = alvo["x"] - self.p2_x
                diff_y = alvo["y"] - self.p2_y
                dist = math.hypot(diff_x, diff_y)
                
                if dist > 5: # Evita trepidação se estiver muito perto
                    dx_p2 = diff_x / dist
                    dy_p2 = diff_y / dist
                else:
                    dx_p2, dy_p2 = 0.0, 0.0
                
                # Aponta a mira para o monstro
                aim_p2_x = dx_p2 if dx_p2 != 0 else 1.0
                aim_p2_y = dy_p2
                
                # Dispara automaticamente se estiver perto o suficiente
                shoot_p2 = dist < 200
                melee_p2 = False
            else:
                # Se não houver monstros por perto, fica parado ou faz uma patrulha calma
                dx_p2, dy_p2 = 0.0, 0.0
                aim_p2_x, aim_p2_y = 1.0, 0.0
                shoot_p2 = False
                melee_p2 = False

        return (dx_p1, dy_p1, mx, my, shoot_p1, melee_p1), (dx_p2, dy_p2, aim_p2_x, aim_p2_y, shoot_p2, melee_p2)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_ESCAPE, pygame.K_P) if hasattr(pygame, 'K_P') else e.key in (pygame.K_ESCAPE, pygame.K_p):
                if self.state == "play":
                    self.paused = not self.paused
            
            if self.paused:
                if e.key == pygame.K_c or e.key == pygame.K_RETURN:
                    self.paused = False
                elif e.key == pygame.K_s or e.key == pygame.K_ESCAPE:
                    self.g.state = "title"

            if e.type == pygame.K_e and self.aftermath:
                if dist(self.px, self.py, 600, 458) < 60:
                    self.g.after_aftermath()

    def hurt_player(self, dmg):
        if self.iframes > 0 or self.state != "play":
            return
        self.hp -= dmg
        self.iframes = 0.5
        self.red = 0.35
        self.shake = max(self.shake, 0.3)
        self.blood(self.px, self.py, 8, (150, 20, 20))
        if self.hp <= 0:
            self.hp = 0
            self.state = "lose"
            self.lose_reason = "Gabriel caiu."

    def fire(self, is_p2=False):
        cd = self.p2_shoot_cd if is_p2 else self.shoot_cd
        if cd > 0:
            return
        if self.ammo <= 0:
            if self.no_ammo_msg <= 0:
                self.say("Gabriel" if not is_p2 else "Rafael", "Sem munição!", 2.5)
                self.no_ammo_msg = 2.5
            return

        self.ammo -= 1
        if is_p2:
            self.p2_shoot_cd = 0.28
            self.p2_muzzle = 0.08
            px, py, aim = self.p2_x, self.p2_y, self.p2_aim
        else:
            self.shoot_cd = 0.28
            self.muzzle = 0.08
            px, py, aim = self.px, self.py, self.aim

        a = aim + random.uniform(-0.04, 0.04)
        self.bullets.append(dict(x=px + math.cos(a) * 16, y=py + math.sin(a) * 16,
                                 vx=math.cos(a) * 760, vy=math.sin(a) * 760,
                                 dmg=16 * self.dmg_mult, life=1.0, col=(255, 235, 150)))
        self.shake = max(self.shake, 0.08)

    def melee(self, is_p2=False):
        cd = self.p2_melee_cd if is_p2 else self.melee_cd
        if cd > 0:
            return

        if is_p2:
            self.p2_melee_cd = 0.45
            self.p2_melee_t = 0.16
            px, py, aim = self.p2_x, self.p2_y, self.p2_aim
        else:
            self.melee_cd = 0.45
            self.melee_t = 0.16
            px, py, aim = self.px, self.py, self.aim

        for m in list(self.monsters):
            d = dist(px, py, m["x"], m["y"])
            if d < 66 + m["r"] * 0.4:
                ang = math.atan2(m["y"] - py, m["x"] - px)
                diff = abs((ang - aim + math.pi) % (2 * math.pi) - math.pi)
                if diff < 1.25:
                    self.damage(m, 17 * self.dmg_mult, math.cos(ang), math.sin(ang), 320)

    def damage(self, m, dmg, dx, dy, kb=120):
        if m not in self.monsters:
            return
        m["hp"] -= dmg
        m["flash"] = 0.1
        f = 0.12 if m["kind"] == "brutamontes" else 1.0
        m["kx"] += dx * kb * f
        m["ky"] += dy * kb * f
        self.blood(m["x"], m["y"], 4)
        if m["hp"] <= 0:
            self.monsters.remove(m)
            self.blood(m["x"], m["y"], 14, (110, 15, 15), 190)
            if random.random() < 0.10 or m["kind"] in ("brutamontes", "gritador"):
                self.pickups.append([m["x"], m["y"]])

    def update(self, dt):
        if self.paused:
            return
        self.time += dt
        self.shake = max(0, self.shake - dt)
        self.red = max(0, self.red - dt)
        self.white = max(0, self.white - dt)
        self.muzzle = max(0, self.muzzle - dt)
        self.p2_muzzle = max(0, self.p2_muzzle - dt)

        self.shoot_cd = max(0, self.shoot_cd - dt)
        self.melee_cd = max(0, self.melee_cd - dt)
        self.melee_t = max(0, self.melee_t - dt)

        self.p2_shoot_cd = max(0, self.p2_shoot_cd - dt)
        self.p2_melee_cd = max(0, self.p2_melee_cd - dt)
        self.p2_melee_t = max(0, self.p2_melee_t - dt)

        self.iframes = max(0, self.iframes - dt)
        self.no_ammo_msg = max(0, self.no_ammo_msg - dt)

        for b in self.barks:
            b[2] -= dt
        self.barks = [b for b in self.barks if b[2] > 0]

        if self.banner:
            self.banner = (self.banner[0], self.banner[1] - dt)
            if self.banner[1] <= 0:
                self.banner = None

        for p in self.parts:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[2] *= 0.9
            p[3] *= 0.9
            p[4] -= dt
        self.parts = [p for p in self.parts if p[4] > 0]

        self.lamp_flick = random.randint(0, 2)

        if self.state == "lose":
            self.end_t += dt
            return

        if self.state == "win":
            self.end_t += dt
            if self.end_t > 3.2 and not self.aftermath:
                self.g.night_won(self.hp, self.ammo)
            return

        p1_in, p2_in = self.read_input()
        self.update_player(dt, p1_in, p2_in)

        if self.aftermath:
            return

        self.update_spawns(dt)
        self.update_allies(dt)
        self.update_monsters(dt)
        self.update_bullets(dt)

        for p in list(self.pickups):
            if dist(self.px, self.py, p[0], p[1]) < 24 or dist(self.p2_x, self.p2_y, p[0], p[1]) < 24:
                self.ammo += 4
                self.pickups.remove(p)
                self.say("Gabriel", "+4 munição", 1.5)

        if self.cabin_hp <= 0:
            self.cabin_hp = 0
            self.state = "lose"
            self.lose_reason = "A cabana caiu."
        elif not self.queue and not self.monsters and self.state == "play":
            self.state = "win"
            self.end_t = 0.0

    def update_player(self, dt, p1_in, p2_in):
        dx, dy, mx, my, shoot, melee = p1_in
        sp = self.speed * (0.62 if self.wounded else 1.0)
        if dx or dy:
            l = math.hypot(dx, dy)
            self.px += dx / l * sp * dt
            self.py += dy / l * sp * dt
            self.px = clamp(self.px, 14, W - 14)
            self.py = clamp(self.py, 14, H - 14)

        cx, cy = closest_on_rect(CABIN.inflate(10, 10), self.px, self.py)
        d = dist(self.px, self.py, cx, cy)
        if d < 13:
            if d == 0:
                self.py = CABIN.bottom + 18
            else:
                self.px = cx + (self.px - cx) / d * 13
                self.py = cy + (self.py - cy) / d * 13

        self.aim = math.atan2(my - self.py, mx - self.px)

        if shoot: self.fire(is_p2=False)
        if melee: self.melee(is_p2=False)

        dx2, dy2, ax2, ay2, shoot2, melee2 = p2_in
        if dx2 or dy2:
            l2 = math.hypot(dx2, dy2)
            self.p2_x += dx2 / l2 * sp * dt
            self.p2_y += dy2 / l2 * sp * dt
            self.p2_x = clamp(self.p2_x, 14, W - 14)
            self.p2_y = clamp(self.p2_y, 14, H - 14)

        cx2, cy2 = closest_on_rect(CABIN.inflate(10, 10), self.p2_x, self.p2_y)
        d2 = dist(self.p2_x, self.p2_y, cx2, cy2)
        if d2 < 13:
            if d2 == 0:
                self.p2_y = CABIN.bottom + 18
            else:
                self.p2_x = cx2 + (self.p2_x - cx2) / d2 * 13
                self.p2_y = cy2 + (self.p2_y - cy2) / d2 * 13

        if abs(ax2) > 0.01 or abs(ay2) > 0.01:
            self.p2_aim = math.atan2(ay2, ax2)

        if shoot2: self.fire(is_p2=True)
        if melee2: self.melee(is_p2=True)

    def update_spawns(self, dt):
        if not self.queue:
            return
        self.spawn_t -= dt
        if self.spawn_t > 0:
            return
        item = self.queue.pop(0)
        self.spawn_t = self.cfg["gap"] * random.uniform(0.7, 1.3)
        if item == "EVENTO_FERIDA":
            self.trigger_wound()
            return
        m = self.spawn(item)
        if item == "gritador":
            self.banner = ("Um Gritador! Elimine-o antes que ele grite!", 5.0)
            self.say("Miguel", "Tem uma coisa parada ali. Só olhando pra gente...")
        elif item == "brutamontes":
            self.say("Daniel", "Aquilo ali é grande demais!")
        elif item == "observador":
            self.say("Daniel", "Algo nos vigia desde o entardecer.")

    def trigger_wound(self):
        self.wounded = True
        self.hp = min(self.hp, 28.0)
        self.red = 1.0
        self.shake = 0.8
        self.banner = ("Gabriel foi gravemente ferido!", 4.0)
        self.say("Livia", "GABRIEL!")
        self.say("Rafael", "Aguenta! Fica perto da Lívia!")
        for _ in range(3):
            self.spawn("corredor")

    def update_allies(self, dt):
        for a in self.allies:
            a["cd"] = max(0, a["cd"] - dt)
            a["bark"] -= dt
            name = a["name"]
            rng_mult = 1.4 if self.tower else 1.0
            if a["bark"] <= 0:
                a["bark"] = random.uniform(11, 20)
                self.say(name, random.choice(BARKS[name]), 3.5)

            if name == "Caio":
                tgt = None
                best = 175
                for m in self.monsters:
                    d = dist(a["hx"], a["hy"], m["x"], m["y"])
                    if d < best:
                        best, tgt = d, m
                if tgt:
                    self.move_to(a, tgt["x"], tgt["y"], 165, dt, stop=tgt["r"] + 14)
                    if dist(a["x"], a["y"], tgt["x"], tgt["y"]) < tgt["r"] + 26 and a["cd"] <= 0:
                        a["cd"] = 0.6
                        ang = math.atan2(tgt["y"] - a["y"], tgt["x"] - a["x"])
                        self.damage(tgt, 16, math.cos(ang), math.sin(ang), 220)
                else:
                    self.move_to(a, a["hx"], a["hy"], 120, dt)
            elif name in ("Miguel", "Elisa"):
                tgt = self.nearest(a["x"], a["y"], 300 * rng_mult)
                if tgt and a["cd"] <= 0:
                    a["cd"] = 0.8 if name == "Miguel" else 1.1
                    ang = math.atan2(tgt["y"] - a["y"], tgt["x"] - a["x"]) + random.uniform(-0.06, 0.06)
                    self.bullets.append(dict(x=a["x"], y=a["y"], vx=math.cos(ang) * 620,
                                             vy=math.sin(ang) * 620,
                                             dmg=11 if name == "Miguel" else 8, life=0.9,
                                             col=(255, 180, 120)))
            elif name == "Daniel":
                if self.cabin_hp < self.cabin_max:
                    rate = 3.5 * (1.6 if "oficina" in self.g.built else 1.0)
                    self.cabin_hp = min(self.cabin_max, self.cabin_hp + rate * dt)
                    if random.random() < 0.04:
                        self.parts.append([a["x"], a["y"], random.uniform(-20, 20), -40, 0.5, (200, 200, 120), 2])
            elif name == "Livia":
                d = dist(a["x"], a["y"], self.px, self.py)
                if self.hp < 65 and d > 380:
                    self.move_to(a, self.px, self.py, 130, dt, stop=34)
                else:
                    self.move_to(a, a["hx"], a["hy"], 100, dt)
                if d < 110 and self.hp < 100 and self.state == "play":
                    heal = 5.0 * (1.6 if "enfermaria" in self.g.built else 1.0)
                    self.hp = min(100.0, self.hp + heal * dt)
                    if random.random() < 0.08:
                        self.parts.append([self.px, self.py, random.uniform(-15, 15), -40, 0.6, (120, 255, 150), 3])
            elif name == "Helena":
                d = dist(a["x"], a["y"], self.px, self.py)
                if d > 75:
                    self.move_to(a, self.px - 40, self.py - 40, 150, dt)

    def move_to(self, a, tx, ty, speed, dt, stop=2):
        d = dist(a["x"], a["y"], tx, ty)
        if d > stop:
            step = min(speed * dt, d - stop)
            a["x"] += (tx - a["x"]) / d * step
            a["y"] += (ty - a["y"]) / d * step
        cx, cy = closest_on_rect(CABIN.inflate(6, 6), a["x"], a["y"])
        dd = dist(a["x"], a["y"], cx, cy)
        if dd < 11:
            if dd == 0:
                a["y"] = CABIN.bottom + 15
            else:
                a["x"] = cx + (a["x"] - cx) / dd * 11
                a["y"] = cy + (a["y"] - cy) / dd * 11

    def update_monsters(self, dt):
        helenas = [a for a in self.allies if a["name"] == "Helena"]
        for m in list(self.monsters):
            m["cd"] = max(0, m["cd"] - dt)
            m["flash"] = max(0, m["flash"] - dt)
            m["x"] += m["kx"] * dt
            m["y"] += m["ky"] * dt
            fr = 0.85 ** (dt * 60)
            m["kx"] *= fr
            m["ky"] *= fr
            spd = m["speed"]
            for h in helenas:
                if dist(h["x"], h["y"], m["x"], m["y"]) < 125:
                    spd *= 0.6
                    break
            
            dp1 = dist(m["x"], m["y"], self.px, self.py)
            dp2 = dist(m["x"], m["y"], self.p2_x, self.p2_y)
            dp = min(dp1, dp2)

            k = m["kind"]
            if k == "gritador" and m["state"] == "observe":
                self.upd_gritador(m, dt, spd)
            elif k == "observador":
                self.upd_observador(m, dt, spd, dp)
            else:
                self.chase(m, dt, spd, dp1, dp2)

        ms = self.monsters
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                a, b = ms[i], ms[j]
                d = dist(a["x"], a["y"], b["x"], b["y"])
                lim = (a["r"] + b["r"]) * 0.85
                if d < lim and d > 0:
                    push = (lim - d) * 0.5
                    nx, ny = (a["x"] - b["x"]) / d, (a["y"] - b["y"]) / d
                    a["x"] += nx * push
                    a["y"] += ny * push
                    b["x"] -= nx * push
                    b["y"] -= ny * push

    def step_toward(self, m, tx, ty, spd, dt):
        d = dist(m["x"], m["y"], tx, ty)
        if d > 0.1:
            m["x"] += (tx - m["x"]) / d * spd * dt
            m["y"] += (ty - m["y"]) / d * spd * dt
            m["face"] = math.atan2(ty - m["y"], tx - m["x"])

    def chase(self, m, dt, spd, dp1, dp2):
        k = m["kind"]
        agro = 90 if k == "brutamontes" else 170
        dp = min(dp1, dp2)
        target_x = self.px if dp1 <= dp2 else self.p2_x
        target_y = self.py if dp1 <= dp2 else self.p2_y

        if dp < agro and self.state == "play":
            self.step_toward(m, target_x, target_y, spd, dt)
            if dp < m["r"] + 14 and m["cd"] <= 0:
                m["cd"] = 0.9
                self.hurt_player(m["hit"])
            return

        cx, cy = closest_on_rect(CABIN.inflate(16, 16), m["x"], m["y"])
        d = dist(m["x"], m["y"], cx, cy)
        if d <= m["r"] + 2:
            self.cabin_hp -= m["cab"] * dt
            m["face"] = math.atan2(cy - m["y"], cx - m["x"])
            if random.random() < 0.05:
                self.parts.append([cx, cy, random.uniform(-40, 40), random.uniform(-40, 40), 0.4, (130, 90, 50), 2])
        else:
            self.step_toward(m, cx, cy, spd, dt)

    def upd_gritador(self, m, dt, spd):
        cd = dist(m["x"], m["y"], CABIN.centerx, CABIN.centery)
        if cd > 310:
            self.step_toward(m, CABIN.centerx, CABIN.centery, spd, dt)
        m["scream"] -= dt
        if m["scream"] <= 0:
            self.scream(m)
            m["state"] = "normal"

    def scream(self, m):
        self.shake = 1.0
        self.white = 0.5
        self.banner = ("O GRITO!", 3.5)
        self.say("Rafael", "Ele chamou os outros! Segurem a porta!")
        for i in range(14):
            self.spawn("andarilho" if i < 9 else "corredor")

    def upd_observador(self, m, dt, spd, dp):
        alone = (not self.queue) and len(self.monsters) == 1
        if m["state"] == "dash":
            m["dash"] -= dt
            m["x"] += m["dx"] * 340 * dt
            m["y"] += m["dy"] * 340 * dt
            m["face"] = math.atan2(m["dy"], m["dx"])
            if dp < m["r"] + 13 and m["cd"] <= 0:
                m["cd"] = 1.0
                self.hurt_player(m["hit"])
            if m["dash"] <= 0:
                m["state"] = "stalk"
                m["timer"] = 3.0 if alone else random.uniform(6, 8)
            return

        m["state"] = "warn" if m["timer"] <= 1.0 else "stalk"
        m["timer"] -= dt
        if m["state"] == "stalk":
            ang = math.atan2(m["y"] - self.py, m["x"] - self.px)
            if dp > 270:
                self.step_toward(m, self.px, self.py, spd, dt)
            elif dp < 210:
                self.step_toward(m, m["x"] + math.cos(ang) * 50, m["y"] + math.sin(ang) * 50, spd, dt)
            else:
                perp = ang + math.pi / 2
                m["x"] += math.cos(perp) * spd * 0.6 * dt
                m["y"] += math.sin(perp) * spd * 0.6 * dt
            m["x"] = clamp(m["x"], -40, W + 40)
            m["y"] = clamp(m["y"], -40, H + 40)

        if m["timer"] <= 0:
            d = max(1, dp)
            m["dx"] = (self.px - m["x"]) / d
            m["dy"] = (self.py - m["y"]) / d
            m["state"] = "dash"
            m["dash"] = 0.9

    def update_bullets(self, dt):
        for b in list(self.bullets):
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            b["life"] -= dt
            hit = False
            for m in self.monsters:
                if dist(b["x"], b["y"], m["x"], m["y"]) < m["r"] + 3:
                    l = math.hypot(b["vx"], b["vy"])
                    self.damage(m, b["dmg"], b["vx"] / l, b["vy"] / l, 130)
                    hit = True
                    break
            if hit or b["life"] <= 0 or not (-20 < b["x"] < W + 20 and -20 < b["y"] < H + 20):
                self.bullets.remove(b)

    def draw(self, g, surf, screen):
        g.draw_world(surf, night=True)
        self.draw_entities(g, surf)
        self.draw_darkness(g, surf)

        if self.tower:
            for m in self.monsters:
                if m["kind"] == "observador":
                    pygame.draw.circle(surf, (255, 40, 40), (int(m["x"]) - 4, int(m["y"]) - 2), 2)
                    pygame.draw.circle(surf, (255, 40, 40), (int(m["x"]) + 4, int(m["y"]) - 2), 2)

        ox, oy = 0, 0
        if self.shake > 0:
            amp = min(10, self.shake * 14)
            ox, oy = random.uniform(-amp, amp), random.uniform(-amp, amp)

        g.render_scaled(surf, (ox, oy))
        self.draw_hud(g, screen)

    def draw_entities(self, g, surf):
        fs = g.f_s
        if self.aftermath:
            pygame.draw.ellipse(surf, (25, 20, 20), (582, 450, 50, 22))
            pygame.draw.circle(surf, CHAR_COL["Caio"], (578, 460), 8)
            if dist(self.px, self.py, 600, 458) < 60:
                draw_text(surf, "Pressione E", g.f_m, WHITE, (600, 500), "center")

        for p in self.pickups:
            pygame.draw.rect(surf, GOLD, (p[0] - 5, p[1] - 4, 10, 8), border_radius=2)
            pygame.draw.rect(surf, (90, 70, 20), (p[0] - 5, p[1] - 4, 10, 8), 1, border_radius=2)

        for p in self.parts:
            pygame.draw.circle(surf, p[5], (int(p[0]), int(p[1])), p[6])

        for a in self.allies:
            draw_person(surf, fs, a["name"], a["x"], a["y"])
            if a["name"] == "Helena":
                pygame.draw.circle(surf, (255, 240, 170), (int(a["x"]) + 12, int(a["y"]) + 4), 4)

        for m in self.monsters:
            self.draw_monster(g, surf, m)

        for b in self.bullets:
            pygame.draw.line(surf, b["col"], (b["x"], b["y"]), (b["x"] - b["vx"] * 0.02, b["y"] - b["vy"] * 0.02), 3)

        # Gabriel (P1)
        px, py = int(self.px), int(self.py)
        blink = self.iframes > 0 and int(self.time * 30) % 2 == 0
        if not blink:
            pygame.draw.ellipse(surf, (0, 0, 0), (px - 10, py + 10, 20, 7))
            img = SPR["Gabriel"]["flip" if math.cos(self.aim) < 0 else "body"]
            surf.blit(img, img.get_rect(midbottom=(px, py + 16)))
            ex, ey = px + math.cos(self.aim) * 22, py + math.sin(self.aim) * 22
            pygame.draw.line(surf, (60, 60, 70), (px, py + 2), (ex, ey), 4)
            if self.muzzle > 0:
                pygame.draw.circle(surf, (255, 240, 160), (int(ex), int(ey)), 7)
            if self.melee_t > 0 and not self.aftermath:
                r = pygame.Rect(0, 0, 150, 150)
                r.center = (px, py)
                pygame.draw.arc(surf, (255, 255, 255), r, self.aim - 1.1, self.aim + 1.1, 4)

        # Rafael (P2 - Controle USB / iPega)
        p2x, p2y = int(self.p2_x), int(self.p2_y)
        pygame.draw.ellipse(surf, (0, 0, 0), (p2x - 10, p2y + 10, 20, 7))
        img2 = SPR["Rafael"]["flip" if math.cos(self.p2_aim) < 0 else "body"]
        surf.blit(img2, img2.get_rect(midbottom=(p2x, p2y + 16)))
        ex2, ey2 = p2x + math.cos(self.p2_aim) * 22, p2y + math.sin(self.p2_aim) * 22
        pygame.draw.line(surf, (180, 80, 40), (p2x, p2y + 2), (ex2, ey2), 4)
        if self.p2_muzzle > 0:
            pygame.draw.circle(surf, (255, 240, 160), (int(ex2), int(ey2)), 7)
        if self.p2_melee_t > 0:
            r2 = pygame.Rect(0, 0, 150, 150)
            r2.center = (p2x, p2y)
            pygame.draw.arc(surf, (255, 210, 70), r2, self.p2_aim - 1.1, self.p2_aim + 1.1, 4)

    def draw_monster(self, g, surf, m):
        x, y, r = int(m["x"]), int(m["y"]), m["r"]
        k = m["kind"]
        spr = SPR[k]["flip" if math.cos(m["face"]) < 0 else "body"]
        vis, tint = 255, False
        if k == "observador":
            dp = dist(m["x"], m["y"], self.px, self.py)
            vis = 255 if (dp < 230 or m["flash"] > 0) else 70
            tint = m["state"] in ("warn", "dash")

        if m["flash"] > 0 or tint:
            spr = spr.copy()
            spr.fill((150, 150, 150, 0) if m["flash"] > 0 else (120, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)

        if vis < 255:
            spr = spr.copy()
            spr.set_alpha(vis)

        pygame.draw.ellipse(surf, (0, 0, 0), (x - r, y + r - 5, r * 2, 8))
        rect = spr.get_rect(midbottom=(x, y + r))
        surf.blit(spr, rect)

        if k == "gritador":
            charge = 1 - clamp(m["scream"] / 6.0, 0, 1) if m["state"] == "observe" else 0
            pygame.draw.circle(surf, (255, 255, 255), (x, y), r + int(8 + 30 * charge), 1)

        if m["hp"] < m["maxhp"]:
            w = max(18, r * 2)
            by = rect.top - 6
            pygame.draw.rect(surf, (40, 0, 0), (x - w // 2, by, w, 4))
            pygame.draw.rect(surf, (210, 50, 50), (x - w // 2, by, int(w * m["hp"] / m["maxhp"]), 4))

    def draw_darkness(self, g, surf):
        if self.state == "win":
            f = clamp(1 - self.end_t / 3.0, 0, 1)
        else:
            f = 1.0
        if f <= 0:
            return

        dark = g.dark
        dark.fill((3, 5, 16, int(232 * f)))

        low = self.cabin_hp < self.cabin_max * 0.3
        if low and random.random() < 0.15:
            lamp = g.lights[190]
        else:
            lamp = g.lights[(230, 265, 290)[self.lamp_flick]]

        r = lamp.get_width() // 2
        dark.blit(lamp, (CABIN.centerx - r, CABIN.centery - r), special_flags=pygame.BLEND_RGBA_SUB)

        pl = g.lights[190]
        dark.blit(pl, (self.px - 190, self.py - 190), special_flags=pygame.BLEND_RGBA_SUB)

        p2l = g.lights[190]
        dark.blit(p2l, (self.p2_x - 190, self.p2_y - 190), special_flags=pygame.BLEND_RGBA_SUB)

        if self.muzzle > 0:
            ml = g.lights[140]
            dark.blit(ml, (self.px - 140, self.py - 140), special_flags=pygame.BLEND_RGBA_SUB)

        for a in self.allies:
            if a["name"] == "Helena":
                hl = g.lights[140]
                dark.blit(hl, (a["x"] - 140, a["y"] - 140), special_flags=pygame.BLEND_RGBA_SUB)

        surf.blit(dark, (0, 0))

    def draw_hud(self, g, s):
        if self.aftermath:
            draw_text(s, "Silêncio.", g.f_m, GREY, (g.screen_w // 2, 40), "center")
            return

        fs, fm = g.f_s, g.f_m
        draw_text(s, self.cfg["title"], fm, GOLD, (20, 12))
        draw_bar(s, fs, 20, 44, 230, 20, self.hp / 100.0, (200, 60, 60), "Gabriel (P1)")
        draw_bar(s, fs, 20, 70, 230, 20, self.cabin_hp / self.cabin_max, (210, 160, 60), "Cabana")

        draw_text(s, f"Munição: {self.ammo}", fs, WHITE, (20, 98))
        draw_text(s, f"Arma nv.{g.weapon + 1}", fs, GREY, (130, 98))

        left = len([k for k in self.queue if not k.startswith("EVENTO")]) + len(self.monsters)
        draw_text(s, f"Criaturas restantes: {left}", fm, WHITE, (g.screen_w - 20, 14), "topright")

        y = g.screen_h - 30
        for who, text, t in reversed(self.barks):
            col = CHAR_COL.get(who, GREY)
            line = f"{who}: {text}"
            img = fs.render(line, True, col)
            r = img.get_rect(midbottom=(g.screen_w // 2, y))
            bg = pygame.Surface((r.w + 16, r.h + 6), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 150))
            s.blit(bg, (r.x - 8, r.y - 3))
            s.blit(img, r)
            y -= 28

        if self.banner:
            text = self.banner[0]
            big = text.isupper() or "!" in text
            draw_text(s, text, g.f_l if big else fm, (255, 225, 140) if big else WHITE, (g.screen_w // 2, 140), "center")

        if self.red > 0:
            ov = pygame.Surface((g.screen_w, g.screen_h), pygame.SRCALPHA)
            ov.fill((200, 0, 0, int(110 * self.red / 0.35 if self.red < 0.35 else 110)))
            s.blit(ov, (0, 0))

        if self.white > 0:
            ov = pygame.Surface((g.screen_w, g.screen_h), pygame.SRCALPHA)
            ov.fill((255, 255, 255, int(160 * self.white / 0.5)))
            s.blit(ov, (0, 0))

        if self.state == "win":
            a = int(clamp(self.end_t / 1.5, 0, 1) * 255)
            img = g.f_xl.render("AMANHECEU", True, GOLD)
            img.set_alpha(a)
            s.blit(img, img.get_rect(center=(g.screen_w // 2, g.screen_h // 2)))

        if self.state == "lose":
            ov = pygame.Surface((g.screen_w, g.screen_h), pygame.SRCALPHA)
            ov.fill((0, 0, 0, int(clamp(self.end_t / 1.0, 0, 1) * 200)))
            s.blit(ov, (0, 0))
            if self.end_t > 0.8:
                draw_text(s, getattr(self, "lose_reason", ""), g.f_xl, RED, (g.screen_w // 2, g.screen_h // 2 - 40), "center")
                draw_text(s, "R: Tentar novamente a noite | ESC: Menu", fm, WHITE, (g.screen_w // 2, g.screen_h // 2 + 30), "center")

        if self.paused:
            ov = pygame.Surface((g.screen_w, g.screen_h), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 200))
            s.blit(ov, (0, 0))
            
            draw_text(s, "JOGO PAUSADO", g.f_xl, GOLD, (g.screen_w // 2, g.screen_h // 2 - 90), "center")
            
            box = pygame.Surface((440, 140), pygame.SRCALPHA)
            box.fill((20, 20, 30, 220))
            b_rect = box.get_rect(center=(g.screen_w // 2, g.screen_h // 2 + 20))
            s.blit(box, b_rect)
            pygame.draw.rect(s, GOLD, b_rect, 2, border_radius=8)

            draw_text(s, "[ C ] ou [ ENTER ] : CONTINUAR", fm, WHITE, (g.screen_w // 2, g.screen_h // 2 - 10), "center")
            draw_text(s, "[ S ] ou [ ESC ]   : SAIR PARA O MENU", fm, RED, (g.screen_w // 2, g.screen_h // 2 + 35), "center")

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Inicialização da música midia.mp3
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("ultima luz/midia.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"Não foi possível carregar a música: {e}")

        pygame.display.set_caption("ÚLTIMA LUZ")
        
        info = pygame.display.Info()
        self.screen_w = info.current_w
        self.screen_h = info.current_h
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.FULLSCREEN | pygame.DOUBLEBUF)

        self.clock = pygame.time.Clock()
        self.f_s = pygame.font.Font(None, 22)
        self.f_m = pygame.font.Font(None, 30)
        self.f_l = pygame.font.Font(None, 52)
        self.f_xl = pygame.font.Font(None, 100)

        self.scene = pygame.Surface((W, H))
        self.dark = pygame.Surface((W, H), pygame.SRCALPHA)
        self.lights = {r: make_light(r) for r in (140, 190, 230, 265, 290)}
        self.lamp_glow = make_glow(170, (255, 200, 110), 170)

        build_sprites()
        self.bg = self.make_bg()
        self.time = 0.0
        self.state = "title"
        self.story = None
        self.night = None

        self.hover = -1
        self.msg = ""
        self.msg_t = 0.0
        self.reset_game()

    def get_virtual_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        scale_x = self.screen_w / W
        scale_y = self.screen_h / H
        scale = min(scale_x, scale_y)
        ox = (self.screen_w - W * scale) / 2
        oy = (self.screen_h - H * scale) / 2
        vx = (mx - ox) / scale
        vy = (my - oy) / scale
        return vx, vy

    def render_scaled(self, surf, offset=(0, 0)):
        scale_x = self.screen_w / W
        scale_y = self.screen_h / H
        scale = min(scale_x, scale_y)
        nw, nh = int(W * scale), int(H * scale)
        scaled = pygame.transform.smoothscale(surf, (nw, nh))
        ox = (self.screen_w - nw) // 2 + offset[0]
        oy = (self.screen_h - nh) // 2 + offset[1]
        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled, (ox, oy))

    def reset_game(self):
        self.day = 1
        self.res = dict(comida=10, municao=30, sucata=6, remedio=2)
        self.hp = 100
        self.morale = 40
        self.weapon = 0
        self.barr = 0
        self.cabin_max = 300
        self.built = set()
        self.max_energy = 3
        self.energy = 3
        self.injured_days = 0
        self.hungry = False
        self.helped_family = None
        self.records = 0
        self.talks = 0
        self.talk_idx = {n: 0 for n in TALK_ORDER}
        self.snap = None
        self.night = None

    def snapshot(self):
        return dict(res=dict(self.res), hp=self.hp, morale=self.morale, weapon=self.weapon,
                    barr=self.barr, cabin_max=self.cabin_max, built=set(self.built),
                    hungry=self.hungry, max_energy=self.max_energy)

    def restore(self, s):
        self.res = dict(s["res"])
        self.hp = s["hp"]
        self.morale = s["morale"]
        self.weapon = s["weapon"]
        self.barr = s["barr"]
        self.cabin_max = s["cabin_max"]
        self.built = set(s["built"])
        self.hungry = s["hungry"]
        self.max_energy = s["max_energy"]

    def set_msg(self, text, t=6.0):
        self.msg = text
        self.msg_t = t

    def play(self, lines, on_done):
        self.story = Story(lines, on_done)
        self.state = "story"

    def start_new(self):
        self.reset_game()
        self.play(SCENES["intro"], self.begin_day)

    def begin_day(self):
        if self.day == 6 and self.helped_family is None:
            self.play(SCENES["familia"], self.open_choice)
            return
        self.enter_day()

    def enter_day(self):
        self.state = "day"
        self.energy = self.max_energy - (1 if self.injured_days > 0 else 0)
        if self.injured_days > 0:
            self.injured_days -= 1
            self.set_msg("Gabriel ainda está ferido: hoje há menos energia.")
        else:
            self.set_msg(f"Amanheceu. Dia {self.day}. Prepare a cabana antes que a noite chegue.")

    def open_choice(self):
        self.state = "choice"

    def resolve_choice(self, helped):
        self.helped_family = helped
        if helped:
            self.res["comida"] = max(0, self.res["comida"] - 4)
            self.res["remedio"] = max(0, self.res["remedio"] - 1)
            self.res["municao"] = max(0, self.res["municao"] - 8)
            self.max_energy += 1
            self.morale = min(100, self.morale + 10)
            self.play(SCENES["ajudou"], self.enter_day)
        else:
            self.morale = max(0, self.morale - 10)
            self.play(SCENES["nao_ajudou"], self.enter_day)

    def next_day(self):
        self.day += 1
        if "horta" in self.built:
            self.res["comida"] += 3
        self.begin_day()

    def end_day(self):
        need = 3 + (2 if self.helped_family else 0)
        if self.res["comida"] >= need:
            self.res["comida"] -= need
            self.hungry = False
        else:
            self.res["comida"] = 0
            self.hungry = True

        self.snap = self.snapshot()
        lines = list(SCENES["pre%d" % self.day])
        if self.day == 6:
            lines += [("Daniel", "Alguma coisa nos vigia desde o entardecer."), ("Rafael", "Fiquem juntos.")]
            if self.helped_family:
                lines.append(("Elisa", "Eu sei atirar. Deixem eu ajudar."))
            else:
                lines.append(("N", "Gabriel ainda pensa na família que ficou para trás."))
        self.play(lines, self.start_night)

    def start_night(self):
        self.night = Night(self, self.day)
        self.state = "night"

    def retry_night(self):
        if self.snap:
            self.restore(self.snap)
            self.start_night()

    def night_won(self, hp, ammo):
        self.hp = int(round(hp))
        self.res["municao"] = ammo
        n = self.day
        if n == 3:
            self.hp = min(self.hp, 30)
            self.injured_days = 1
            self.night = None
        if n == 5:
            self.night = Night(self, 5, aftermath=True)
            self.state = "night"
            return
        if n == 6:
            lines = SCENES["fim"]
            done = self.end_game
        else:
            lines = list(SCENES["post%d" % n])
            done = self.next_day
        self.play(lines, done)

    def after_aftermath(self):
        self.night = None
        self.play(SCENES["post5"], self.next_day)

    def end_game(self):
        self.state = "end"

    def spend(self, **kw):
        for k, v in kw.items():
            self.res[k] -= v

    def a_explore(self):
        g = random.randint
        gain = dict(comida=g(1, 3), municao=g(3, 8), sucata=g(2, 5), remedio=g(0, 1) + (1 if random.random() < 0.25 else 0))
        for k, v in gain.items():
            self.res[k] += v
        self.energy -= 1
        txt = f"Exploração: +{gain['comida']} comida, +{gain['municao']} munição, +{gain['sucata']} sucata, +{gain['remedio']} remédio."
        if random.random() < 0.3:
            dmg = random.randint(8, 18)
            self.hp = max(15, self.hp - dmg)
            txt += f" Você foi surpreendido por um infectado (-{dmg} vida)."
        self.set_msg(txt, 8)
        if self.day >= 3 and self.records < min(len(RECORDS), self.day - 2):
            rec = RECORDS[self.records]
            self.records += 1
            self.play(rec, self.enter_day_keep)

    def enter_day_keep(self):
        self.state = "day"

    def a_rest(self):
        heal = 60
        if "enfermaria" in self.built:
            heal = 100
        elif self.res["remedio"] >= 1:
            self.res["remedio"] -= 1
            heal = 100
        self.hp = min(100, self.hp + heal)
        self.morale = min(100, self.morale + 5)
        self.energy -= 1
        self.set_msg("Lívia cuida de Gabriel. Vida recuperada." + ("" if "enfermaria" in self.built else " (Gastou 1 remédio, se havia)"))

    def a_talk(self):
        name = TALK_ORDER[self.talks % len(TALK_ORDER)]
        i = self.talk_idx[name] % len(TALKS[name])
        self.talk_idx[name] += 1
        self.talks += 1
        self.energy -= 1
        self.morale = min(100, self.morale + 10)
        self.set_msg("Conversar fortalece o grupo. Moral +10.")
        self.play(TALKS[name][i], self.enter_day_keep)

    def a_reinforce(self):
        self.spend(sucata=4)
        self.barr += 1
        self.cabin_max += 60
        self.energy -= 1
        self.set_msg(f"Barricadas reforçadas (nível {self.barr}). Cabana resiste mais.")

    def weapon_cost(self):
        return 5 - (1 if "oficina" in self.built else 0)

    def a_weapon(self):
        self.spend(sucata=self.weapon_cost())
        self.weapon += 1
        self.energy -= 1
        self.set_msg(f"Daniel melhora a arma. Dano +25% (nível {self.weapon + 1}).")

    def a_build(self, what, cost, text):
        self.spend(sucata=cost)
        self.built.add(what)
        self.energy -= 1
        self.set_msg(text, 8)

    def a_wait(self):
        self.end_day()

    def day_actions(self):
        r, e = self.res, self.energy > 0
        A = []
        A.append(dict(label="Explorar a região", cost="1 energia", ok=e, fn=self.a_explore, desc="Procura comida, munição, sucata e remédios. Há riscos lá fora. A partir do dia 3 você pode achar registros do Projeto Aurora."))
        A.append(dict(label="Descansar e se tratar", cost="1 energia", ok=e, fn=self.a_rest, desc="Recupera vida. Com remédio (ou enfermaria), Lívia cura tudo."))
        A.append(dict(label="Conversar com o grupo", cost="1 energia", ok=e, fn=self.a_talk, desc="Fortalece a moral: aumenta o dano de Gabriel. Descubra o que cada um carrega."))
        
        ok = e and self.barr < 5 and r["sucata"] >= 4
        A.append(dict(label="Reforçar barricadas" + (" (máx)" if self.barr >= 5 else ""), cost="4 sucata", ok=ok, fn=self.a_reinforce, desc="+60 de resistência da cabana por nível (máx. 5)."))
        
        wc = self.weapon_cost()
        ok = e and self.weapon < 5 and r["sucata"] >= wc
        A.append(dict(label="Melhorar a arma" + (" (máx)" if self.weapon >= 5 else ""), cost=f"{wc} sucata", ok=ok, fn=self.a_weapon, desc="+25% de dano em tiros e golpes (máx. 5 níveis)."))

        builds = [
            ("enfermaria", "Enfermaria", 6, "Descansar sempre cura tudo; Lívia cura mais rápido à noite."),
            ("oficina", "Oficina", 6, "Melhorias de arma mais baratas; Daniel conserta a cabana mais rápido."),
            ("horta", "Horta", 5, "Helena planta: +3 de comida a cada amanhecer."),
            ("torre", "Torre de observação", 8, "Aliados atiram mais longe e você enxerga o Observador."),
        ]
        for key, name, cost, desc in builds:
            if key in self.built:
                A.append(dict(label=f"{name} (construída)", cost="", ok=False, fn=None, desc=desc))
            else:
                A.append(dict(label=f"Construir: {name}", cost=f"{cost} sucata", ok=e and r["sucata"] >= cost, fn=(lambda k=key, c=cost, n=name: self.a_build(k, c, f"{n} construída!")), desc=desc))

        A.append(dict(label="ESPERAR A NOITE", cost="", ok=True, fn=self.a_wait, desc="Termina o dia. Todos comem (3 comida; 5 se a família está aqui)."))
        return A

    def day_button_rects(self, n):
        return [pygame.Rect(16, 262 + i * 39, PANEL_W - 32, 34) for i in range(n)]

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.time += dt
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(e)
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def handle_event(self, e):
        st = self.state
        if st == "title":
            if (e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE)) or (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1):
                self.start_new()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif st == "story":
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.story.advance()
                elif e.key == pygame.K_TAB:
                    self.story.skip_all()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.story.advance()
        elif st == "day":
            acts = self.day_actions()
            rects = self.day_button_rects(len(acts))
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                vx, vy = self.get_virtual_mouse_pos()
                for a, r in zip(acts, rects):
                    if r.collidepoint(vx, vy):
                        if a["ok"] and a["fn"]:
                            a["fn"]()
                        elif a["fn"] and self.energy <= 0:
                            self.set_msg("Sem energia hoje. Termine o dia quando quiser.")
                        elif a["fn"]:
                            self.set_msg("Recursos insuficientes.")
                        break
        elif st == "choice":
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_1, pygame.K_2):
                self.resolve_choice(e.key == pygame.K_1)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                vx, vy = self.get_virtual_mouse_pos()
                for i, r in enumerate(self.choice_rects()):
                    if r.collidepoint(vx, vy):
                        self.resolve_choice(i == 0)
        elif st == "night":
            if self.night:
                self.night.handle_event(e)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r and self.night.state == "lose":
                    self.retry_night()
                elif e.key == pygame.K_ESCAPE and self.night.state == "lose":
                    self.state = "title"
        elif st == "end":
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = "title"

    def update(self, dt):
        if self.msg_t > 0:
            self.msg_t -= dt
        if self.state == "story" and self.story:
            self.story.update(dt)
        elif self.state == "night" and self.night:
            self.night.update(dt)
        elif self.state == "day":
            vx, vy = self.get_virtual_mouse_pos()
            acts = self.day_actions()
            self.hover = -1
            for i, r in enumerate(self.day_button_rects(len(acts))):
                if r.collidepoint(vx, vy):
                    self.hover = i

    def make_bg(self):
        rnd = random.Random(7)
        s = pygame.Surface((W, H))
        s.fill((36, 56, 38))
        for _ in range(1400):
            x, y = rnd.randint(0, W), rnd.randint(0, H)
            c = rnd.choice([(30, 48, 32), (42, 64, 44), (34, 52, 34)])
            pygame.draw.circle(s, c, (x, y), rnd.randint(2, 5))

        pygame.draw.ellipse(s, (82, 66, 46), (330, 190, 640, 400))
        pygame.draw.ellipse(s, (92, 75, 52), (370, 220, 560, 340))

        for _ in range(200):
            x, y = rnd.randint(360, 900), rnd.randint(200, 580)
            if ((x - 650) / 290) ** 2 + ((y - 390) / 175) ** 2 < 1:
                pygame.draw.circle(s, (74, 60, 42), (x, y), rnd.randint(1, 3))

        trees = []
        while len(trees) < 60:
            x, y = rnd.randint(0, W), rnd.randint(0, H)
            if 300 < x < 960 and 180 < y < 600:
                continue
            trees.append((x, y, rnd.randint(18, 34)))

        for x, y, r in trees:
            pygame.draw.circle(s, (12, 28, 16), (x + 4, y + 5), r)
            pygame.draw.circle(s, (22, 52, 28), (x, y), r)
            pygame.draw.circle(s, (30, 68, 36), (x - r // 4, y - r // 4), r // 2)
        return s

    def draw_world(self, surf, night=False, day=False):
        surf.blit(self.bg, (0, 0))
        b = self.built

        if day:
            for key, rect in (("enfermaria", ENFERMARIA), ("oficina", OFICINA), ("horta", HORTA), ("torre", TORRE)):
                if key not in b:
                    pygame.draw.rect(surf, (110, 92, 66), rect, 1)

        if "horta" in b:
            pygame.draw.rect(surf, (70, 50, 34), HORTA, border_radius=4)
            for i in range(5):
                x = HORTA.x + 12 + i * 25
                pygame.draw.line(surf, (50, 140, 60), (x, HORTA.y + 8), (x, HORTA.bottom - 8), 6)
                for j in range(3):
                    pygame.draw.circle(surf, (120, 220, 110), (x, HORTA.y + 14 + j * 16), 3)

        if "enfermaria" in b:
            pygame.draw.rect(surf, (225, 225, 230), ENFERMARIA, border_radius=6)
            pygame.draw.rect(surf, (90, 90, 100), ENFERMARIA, 2, border_radius=6)
            cx, cy = ENFERMARIA.center
            pygame.draw.rect(surf, (200, 40, 40), (cx - 4, cy - 14, 8, 28))
            pygame.draw.rect(surf, (200, 40, 40), (cx - 14, cy - 4, 28, 8))

        if "oficina" in b:
            pygame.draw.rect(surf, (90, 92, 105), OFICINA, border_radius=4)
            pygame.draw.rect(surf, (45, 45, 55), OFICINA, 2, border_radius=4)
            for i in range(4):
                pygame.draw.circle(surf, (170, 170, 120), (OFICINA.x + 14 + i * 20, OFICINA.centery), 6, 2)

        if "torre" in b:
            pygame.draw.rect(surf, (96, 70, 44), TORRE)
            pygame.draw.line(surf, (60, 42, 26), TORRE.topleft, TORRE.bottomright, 2)
            pygame.draw.line(surf, (60, 42, 26), TORRE.topright, TORRE.bottomleft, 2)
            pygame.draw.rect(surf, (60, 42, 26), TORRE, 3)

        for i in range(self.barr):
            pygame.draw.rect(surf, (88, 60, 34), CABIN.inflate(14 + i * 4, 14 + i * 4), 2, border_radius=4)

        pygame.draw.rect(surf, (104, 72, 46), CABIN, border_radius=6)
        pygame.draw.rect(surf, (74, 50, 30), (CABIN.x, CABIN.y, CABIN.w, 34), border_radius=6)
        pygame.draw.rect(surf, (36, 24, 16), CABIN, 3, border_radius=6)

        for i in range(1, 5):
            x = CABIN.x + i * 32
            pygame.draw.line(surf, (88, 60, 38), (x, CABIN.y + 38), (x, CABIN.bottom - 4), 1)

        pygame.draw.rect(surf, (40, 26, 16), (CABIN.centerx - 15, CABIN.bottom - 34, 30, 34))

        lx, ly = CABIN.centerx, CABIN.centery - 10
        glow = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 220, 120, 90), (35, 35), 34)
        pygame.draw.circle(glow, (255, 235, 160, 170), (35, 35), 18)
        surf.blit(glow, (lx - 35, ly - 35))
        pygame.draw.circle(surf, (255, 245, 190), (lx, ly), 7)

    def draw_day(self):
        s = self.scene
        self.draw_world(s, day=True)
        t = self.time

        idle = {"Gabriel": (600, 505), "Rafael": (600, 450), "Livia": (440, 375), "Helena": (465, 435), "Miguel": (668, 455), "Daniel": (760, 420)}
        if self.day >= 4:
            idle["Caio"] = (570, 462)
        if self.helped_family:
            idle["Elisa"] = (720, 530)

        for name, (x, y) in idle.items():
            draw_person(s, self.f_s, name, x + math.sin(t + len(name)) * 3, y + math.cos(t * 0.8 + len(name)) * 2)

        p = pygame.Surface((PANEL_W, H), pygame.SRCALPHA)
        p.fill((10, 10, 16, 232))
        s.blit(p, (0, 0))

        draw_text(s, f"DIA {self.day}", self.f_l, GOLD, (16, 10))
        draw_text(s, NIGHTS[self.day]["title"], self.f_s, GREY, (16, 52))

        r = self.res
        items = [("Comida", r["comida"]), ("Sucata", r["sucata"]), ("Munição", r["municao"]), ("Remédio", r["remedio"])]
        for i, (n, v) in enumerate(items):
            x = 16 + (i % 2) * 150
            y = 80 + (i // 2) * 22
            draw_text(s, f"{n}: {v}", self.f_m, WHITE, (x, y))

        draw_bar(s, self.f_s, 16, 128, PANEL_W - 32, 18, self.hp / 100.0, (200, 60, 60), f"Vida: {self.hp}/100")
        draw_bar(s, self.f_s, 16, 150, PANEL_W - 32, 18, self.morale / 100.0, (90, 160, 255), f"Moral: {self.morale}")

        draw_text(s, "Energia:", self.f_m, WHITE, (16, 176))
        for i in range(self.max_energy):
            col = GOLD if i < self.energy else DGREY
            pygame.draw.circle(s, col, (110 + i * 24, 186), 9)

        draw_text(s, f"Arma nv.{self.weapon + 1} | Barricadas nv.{self.barr} | Cabana {self.cabin_max}", self.f_s, GREY, (16, 204))
        draw_text(s, f"Registros Aurora: {self.records}/3", self.f_s, GREY, (16, 224))
        draw_text(s, "AÇÕES", self.f_s, GOLD, (16, 244))

        acts = self.day_actions()
        rects = self.day_button_rects(len(acts))

        for i, (a, rc) in enumerate(zip(acts, rects)):
            wait = a["label"].startswith("ESPERAR")
            if a["ok"]:
                col = (90, 70, 30) if wait else (40, 44, 60)
                if i == self.hover:
                    col = (140, 105, 40) if wait else (70, 76, 105)
                tc = WHITE
            else:
                col, tc = (24, 24, 30), DGREY

            pygame.draw.rect(s, col, rc, border_radius=6)
            pygame.draw.rect(s, (110, 110, 130) if a["ok"] else (45, 45, 55), rc, 1, border_radius=6)
            draw_text(s, a["label"], self.f_s, tc, (rc.x + 10, rc.centery), "midleft", shadow=False)
            if a["cost"]:
                draw_text(s, a["cost"], self.f_s, tc if a["ok"] else DGREY, (rc.right - 8, rc.centery), "midright", shadow=False)

        if self.msg and self.msg_t > 0:
            y = 16
            for ln in wrap(self.msg, self.f_m, W - PANEL_W - 60):
                draw_text(s, ln, self.f_m, WHITE, (PANEL_W + 24, y))
                y += 28

        if 0 <= self.hover < len(acts):
            box = pygame.Surface((W - PANEL_W - 40, 60), pygame.SRCALPHA)
            box.fill((0, 0, 0, 190))
            s.blit(box, (PANEL_W + 20, H - 80))
            y = H - 74
            for ln in wrap(acts[self.hover]["desc"], self.f_s, W - PANEL_W - 70):
                draw_text(s, ln, self.f_s, WHITE, (PANEL_W + 32, y))
                y += 20

        self.render_scaled(s)

    def choice_rects(self):
        return [pygame.Rect(140, 380, 340, 120), pygame.Rect(540, 380, 340, 120)]

    def draw_choice(self):
        s = self.scene
        self.draw_world(s, day=True)
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 200))
        s.blit(ov, (0, 0))

        draw_text(s, "A PRIMEIRA GRANDE ESCOLHA", self.f_l, GOLD, (W // 2, 150), "center")
        draw_text(s, "Uma família de três pessoas pede abrigo.", self.f_m, WHITE, (W // 2, 220), "center")
        draw_text(s, "Não existe uma resposta simplesmente certa.", self.f_m, GREY, (W // 2, 255), "center")
        draw_text(s, "Sobreviver também significa tomar decisões difíceis.", self.f_m, GREY, (W // 2, 285), "center")

        opts = [("1: AJUDAR", "-4 comida, 1 remédio, 8 munição.", "+1 energia por dia, mais bocas para alimentar."),
                ("2: NÃO AJUDAR", "Os recursos são preservados.", "Mas Gabriel vai carregar essa decisão.")]

        vx, vy = self.get_virtual_mouse_pos()
        for r, (a, b, c) in zip(self.choice_rects(), opts):
            col = (70, 76, 105) if r.collidepoint(vx, vy) else (40, 44, 60)
            pygame.draw.rect(s, col, r, border_radius=10)
            pygame.draw.rect(s, (130, 130, 150), r, 2, border_radius=10)
            draw_text(s, a, self.f_m, GOLD, (r.centerx, r.y + 24), "center")
            draw_text(s, b, self.f_s, WHITE, (r.centerx, r.y + 62), "center")
            draw_text(s, c, self.f_s, GREY, (r.centerx, r.y + 88), "center")

        self.render_scaled(s)

    def draw_story(self):
        s = self.scene
        s.fill((7, 7, 12))
        st = self.story
        kind, text = st.cur()

        flick = 0.88 + 0.12 * math.sin(self.time * 7) + random.uniform(-0.03, 0.03)
        self.lamp_glow.set_alpha(int(255 * clamp(flick, 0, 1)))
        s.blit(self.lamp_glow, (W // 2 - 170, 40 - 170 + 90))
        pygame.draw.circle(s, (255, 245, 190), (W // 2, 130), 7)

        if kind == "T":
            a = clamp(st.t / 0.8, 0, 1) * clamp((3.0 - st.t) / 0.6, 0, 1)
            img = self.f_l.render(text, True, GOLD)
            img.set_alpha(int(255 * a))
            s.blit(img, img.get_rect(center=(W // 2, H // 2 + 20)))
        else:
            n = int(st.t * st.cps())
            lines = wrap(text, self.f_m, 760 if kind in ("N", "S") else W - 280)
            if kind in ("N", "S"):
                col = WHITE if kind == "N" else (150, 150, 165)
                y = 330
                rem = n
                for ln in lines:
                    part = ln[:max(0, rem)]
                    rem -= len(ln) + 1
                    draw_text(s, part, self.f_l if kind == "S" else self.f_m, col, (W // 2, y), "midtop")
                    y += 52 if kind == "S" else 38
            else:
                col = CHAR_COL.get(kind, WHITE)
                frame = pygame.Rect(24, 520, 138, 150)
                pygame.draw.rect(s, (16, 16, 24), frame, border_radius=8)
                pygame.draw.rect(s, col, frame, 3, border_radius=8)

                sp = SPR.get(kind)
                if sp:
                    bob = int(math.sin(self.time * 18) * 2) if not st.typed_all() else 0
                    port = sp["portrait"]
                    s.blit(port, port.get_rect(midbottom=(frame.centerx, frame.bottom - 4 + bob)))
                else:
                    pygame.draw.circle(s, col, frame.center, 42)

                box = pygame.Surface((W - 200, 190), pygame.SRCALPHA)
                box.fill((20, 20, 30, 220))
                s.blit(box, (170, 500))

                draw_text(s, kind, self.f_m, col, (190, 512))
                y = 548
                rem = n
                for ln in lines:
                    part = ln[:max(0, rem)]
                    rem -= len(ln) + 1
                    draw_text(s, part, self.f_m, WHITE, (190, y))
                    y += 34

        draw_text(s, "ESPAÇO: Continua | TAB: Pula", self.f_s, DGREY, (W - 16, H - 14), "bottomright", shadow=False)
        self.render_scaled(s)

    def draw_lineup(self, y, names):
        n = len(names)
        for i, nm in enumerate(names):
            spr = SPR[nm]["med"]
            x = W // 2 + (i - (n - 1) / 2) * 90
            bob = int(math.sin(self.time * 2 + i) * 2)
            self.scene.blit(spr, spr.get_rect(midbottom=(x, y + bob)))

    def draw_title(self):
        s = self.scene
        s.fill((6, 6, 11))

        flick = 0.85 + 0.15 * math.sin(self.time * 6) + random.uniform(-0.04, 0.04)
        self.lamp_glow.set_alpha(int(255 * clamp(flick, 0, 1)))
        s.blit(self.lamp_glow, (W // 2 - 170, 200 - 170))
        pygame.draw.circle(s, (255, 245, 190), (W // 2, 200), 9)

        draw_text(s, "ÚLTIMA LUZ", self.f_xl, GOLD, (W // 2, 360), "center")
        draw_text(s, "Nem sempre continuamos porque somos fortes.", self.f_m, GREY, (W // 2, 440), "center")
        draw_text(s, "Às vezes continuamos porque alguém precisa de nós.", self.f_m, GREY, (W // 2, 472), "center")

        self.draw_lineup(548, ["Gabriel", "Rafael", "Livia", "Miguel", "Helena", "Daniel"])

        if int(self.time * 1.6) % 2 == 0:
            draw_text(s, "ENTER ou Clique para começar", self.f_m, WHITE, (W // 2, 580), "center")

        draw_text(s, "Sobrevivência | Terror | Co-op Local | Ação", self.f_s, DGREY, (W // 2, 680), "center")
        self.render_scaled(s)

    def draw_end(self):
        s = self.scene
        s.fill((6, 6, 11))

        self.lamp_glow.set_alpha(255)
        s.blit(self.lamp_glow, (W // 2 - 170, 170 - 170))
        pygame.draw.circle(s, (255, 245, 190), (W // 2, 170), 9)

        crew = ["Gabriel", "Rafael", "Livia", "Helena", "Daniel"]
        if self.helped_family:
            crew.append("Elisa")

        self.draw_lineup(262, crew)

        draw_text(s, "FIM DA PARTE 1", self.f_l, GOLD, (W // 2, 320), "center")
        draw_text(s, "Você sobreviveu a seis noites.", self.f_m, WHITE, (W // 2, 390), "center")

        helped = {True: "Você ajudou a família.", False: "Você não ajudou a família.", None: ""}[self.helped_family]
        draw_text(s, helped, self.f_m, GREY, (W // 2, 430), "center")
        draw_text(s, f"Registros do Projeto Aurora: {self.records}/3", self.f_m, GREY, (W // 2, 465), "center")
        draw_text(s, "Mas enquanto houver alguém para nos levantar...", self.f_m, WHITE, (W // 2, 540), "center")
        draw_text(s, "...ainda existe um motivo para continuar.", self.f_m, GOLD, (W // 2, 575), "center")
        draw_text(s, "ENTER: Voltar ao menu", self.f_s, DGREY, (W // 2, 680), "center")

        self.render_scaled(s)

    def draw(self):
        st = self.state
        if st == "title":
            self.draw_title()
        elif st == "story":
            self.draw_story()
        elif st == "day":
            self.draw_day()
        elif st == "choice":
            self.draw_choice()
        elif st == "night" and self.night:
            self.night.draw(self, self.scene, self.screen)
        elif st == "end":
            self.draw_end()

if __name__ == "__main__":
    Game().run()