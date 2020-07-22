import pygame
from Model import *
from Persistence import *


model = Model()
model.add_killer_wall(30,200,400,20)
# model.add_door(400,200,50,20, 1)
model.add_passable_wall(450,200,800,20,pass_id=0)
model.add_passable_wall(450,300,800,20,pass_id=1)
model.add_portal(300,10,10,10, 0)
model.add_portal(300,450,10,10, 0)
# model.add_button(500,10,50,50, 2)

pygame.init()

win = pygame.display.set_mode((model.width, model.height))

run = True

while run:
	pygame.time.delay(10)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	buttons_pressed = pygame.key.get_pressed()
	if buttons_pressed[pygame.K_ESCAPE]:
		run = False
	if buttons_pressed[pygame.K_SPACE]:
		print(model.p0.x, model.p0.y)
		print("----------------------------")
	if buttons_pressed[pygame.K_l]:
		mtx = load_map_matrix("Helo.map")
		model.load_map(mtx)
	

	if buttons_pressed[pygame.K_UP]:
		model.move_player(0, "up")
	if buttons_pressed[pygame.K_RIGHT]:
		model.move_player(0, "right")
	if buttons_pressed[pygame.K_DOWN]:
		model.move_player(0, "down")
	if buttons_pressed[pygame.K_LEFT]:
		model.move_player(0, "left")
	
	if buttons_pressed[pygame.K_w]:
		model.move_player(1, "up")
	if buttons_pressed[pygame.K_d]:
		model.move_player(1, "right")
	if buttons_pressed[pygame.K_s]:
		model.move_player(1, "down")
	if buttons_pressed[pygame.K_a]:
		model.move_player(1, "left")
	
	win.fill((255,255,255))
	
	for o in model.get_objects():
		pygame.draw.rect(win, o.color, (o.x, o.y, o.width, o.height))
	
	
	pygame.display.update()
	
	
pygame.quit()




























