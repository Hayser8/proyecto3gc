import pygame
from pygame.locals import *
from OpenGL.GL import *
from gl import Renderer
from buffer import *
from shaders import *
from model import *
import glm
import imageio
from PIL import Image

# Configuración de pantalla
screen_width = 540
screen_height = 540

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen)
selection_sound = pygame.mixer.Sound('music/selection.mp3')
pygame.mixer.music.load('music/background.mp3') 
pygame.mixer.music.play(-1)

# Texturas de la skybox
skybox_textures = [
    "skybox/right.jpg",
    "skybox/left.jpg",
    "skybox/top.jpg",
    "skybox/bottom.jpg",
    "skybox/front.jpg",
    "skybox/back.jpg"
]
models = []

renderer.CreateSkybox(skybox_textures, skybox_vertex_shader, skybox_fragment_shader)

# Modelo Floor (piso)
floor = Model("models/floor.obj")
floor.AddTexture("textures/floor.bmp")
floor.translation = glm.vec3(0, -0.6, 0)  
floor.scale = glm.vec3(1.9, 1.3, 1.9)  
floor.rotation = glm.vec3(0, 90, 0)  
floor.SetShaders(vertex_shader, fragment_shader)
renderer.scene.append(floor)


# Modelo Po
po = Model("models/Po.obj")
po.AddTexture("textures/Po.bmp")
po.translation = glm.vec3(0, 0, -5)
po.scale = glm.vec3(1.5, 1.5, 1.5)
po.SetShaders(po_shader_vertex, fragment_shader)
renderer.scene.append(po)
models.append(po)

# Modelo Tigress
tigress = Model("models/Tigress.obj")
tigress.AddTexture("textures/Tigress.bmp")
tigress.translation = glm.vec3(3, 0, -4)
tigress.scale = glm.vec3(1.2, 1.2, 1.2)
tigress.SetShaders(pulse, fragment_shader)
renderer.scene.append(tigress)
models.append(tigress)

# Modelo Monkey
monkey = Model("models/Monkey.obj")
monkey.AddTexture("textures/MonkeyDiffuse.bmp")
monkey.translation = glm.vec3(-3, 0, -4)
monkey.scale = glm.vec3(1.5, 1.5, 1.5)
monkey.SetShaders(monkey_shader_vertex, fragment_shader)
renderer.scene.append(monkey)
models.append(monkey)

# Modelo Shifu
shifu = Model("models/Shifu.obj")
shifu.AddTexture("textures/Shifu.bmp")
shifu.translation = glm.vec3(0, 0, -3)
shifu.scale = glm.vec3(1.0, 1.0, 1.0)
shifu.SetShaders(vertex_shader, shifu_shader_fragment)
renderer.scene.append(shifu)
models.append(shifu)

# Barras (split bars)
bars = Model("models/bars.obj")
bars.AddTexture("textures/bars.bmp")
bars.translation = glm.vec3(-2, 0, -6)
bars.scale = glm.vec3(0.1, 0.1, 0.1)  
bars.SetShaders(vertex_shader, bars_shader_fragment)
renderer.scene.append(bars)
models.append(bars)

# Punching Bag
punching_bag = Model("models/punching.obj")
punching_bag.AddTexture("textures/punching.bmp")
punching_bag.translation = glm.vec3(2, 0, -6)
punching_bag.scale = glm.vec3(0.1, 0.1, 0.1)  
punching_bag.SetShaders(punching_bag_shader_vertex, fragment_shader)
renderer.scene.append(punching_bag)
models.append(punching_bag)

# Bow Target
bow_target = Model("models/low.obj")
bow_target.AddTexture("textures/low.bmp")
bow_target.translation = glm.vec3(0, 0, -8)
bow_target.scale = glm.vec3(0.1, 0.1, 0.1) 
bow_target.SetShaders(vertex_shader, bow_target_shader_fragment)
renderer.scene.append(bow_target)
models.append(bow_target)


camera_distance = 10
camera_angle = 0
camera_height = 2
camera_max_distance = 20
camera_min_distance = 5
camera_max_height = 7
camera_min_height = -2
camera_speed = 0.2

# Variables de control
is_running = True
selected_model_index = None
mouse_dragging = False
last_mouse_pos = None

filter_on = False
vertex_shader_program = vertex_shader
fragment_shader_program = fragment_shader

renderer.SetShaders(vertex_shader_program, fragment_shader_program)

frames = []

# Ciclo principal
while is_running:
    delta_time = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                is_running = False
            if event.key == pygame.K_1:
                selected_model_index = 0
                selection_sound.play()
            elif event.key == pygame.K_2:
                selected_model_index = 1
                selection_sound.play()
            elif event.key == pygame.K_3:
                selected_model_index = 2
                selection_sound.play()
            elif event.key == pygame.K_4:
                selected_model_index = 3
                selection_sound.play()
            elif event.key == pygame.K_5:
                selected_model_index = 4
                selection_sound.play()
            elif event.key == pygame.K_6:
                selected_model_index = 5
                selection_sound.play()
            elif event.key == pygame.K_7:
                selected_model_index = 6
                selection_sound.play()
            elif event.key == pygame.K_8:
                selected_model_index = 7
                selection_sound.play()

            if selected_model_index is not None:
                camera_target = models[selected_model_index].translation
                camera_distance = 5  
                camera_angle = 0  
                camera_height = 2  

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 4:  # Rueda del mouse hacia adelante
                camera_distance = max(camera_min_distance, camera_distance - 1)
            elif event.button == 5:  # Rueda del mouse hacia atrás
                camera_distance = min(camera_max_distance, camera_distance + 1)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and mouse_dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            last_mouse_pos = current_mouse_pos
            camera_angle += dx * camera_speed
            camera_height += dy * 0.05
            camera_height = max(-5, min(10, camera_height))

    # Movimiento de la luz
    if keys[K_LEFT]:
        renderer.pointLight.x -= 1 * delta_time
    if keys[K_RIGHT]:
        renderer.pointLight.x += 1 * delta_time
    if keys[K_UP]:
        camera_height = min(camera_max_height, camera_height + 2 * delta_time)
    if keys[K_DOWN]:
        camera_height = max(camera_min_height, camera_height - 2 * delta_time)
    if keys[K_PAGEUP]:
        renderer.pointLight.y += 1 * delta_time
    if keys[K_PAGEDOWN]:
        renderer.pointLight.y -= 1 * delta_time
    if keys[K_a]:
        camera_angle -= 45 * delta_time
    if keys[K_d]:
        camera_angle += 45 * delta_time
    if keys[K_w]:
        camera_distance = max(camera_min_distance, camera_distance - 2 * delta_time)
    if keys[K_s]:
        camera_distance = min(camera_max_distance, camera_distance + 2 * delta_time)

    for obj in renderer.scene:
        obj.Update(delta_time)


    if selected_model_index is None:
        camera_target = glm.vec3(0, 0, 0)
        camera_distance = 15  
        camera_angle += 20 * delta_time 
    renderer.camera.LookAt(camera_target)
    renderer.camera.Orbit(camera_target, camera_distance, camera_angle, camera_height)

    # Renderizar la escena
    renderer.Render()
    pygame.display.flip()

    
pygame.quit()


