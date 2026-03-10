import pygame
import os
import math

# Initialize pygame
pygame.init()

ANIMALS = ["CAT", "DOG", "FISH", "BIRD", "FROG", "BEAR", "LION", "DUCK", 
           "PIG", "COW", "FOX", "WOLF", "DEER", "ANT", "BEE"]

ASSET_DIR = "assets/animals"
if not os.path.exists(ASSET_DIR):
    os.makedirs(ASSET_DIR)

def generate_animal_png(word, size=256):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    r = size // 2 - 20
    
    # Face Base (Pale Cream)
    pygame.draw.circle(surf, (245, 235, 215), (cx, cy), r)
    pygame.draw.circle(surf, (40, 40, 40), (cx, cy), r, 4)

    if word == "LION":
        # Mane
        pygame.draw.circle(surf, (220, 110, 30), (cx, cy), r + 8, 15)
        pygame.draw.circle(surf, (40, 40, 40), (cx - 40, cy - 20), 12)
        pygame.draw.circle(surf, (40, 40, 40), (cx + 40, cy - 20), 12)
        pygame.draw.polygon(surf, (40, 40, 40), [(cx, cy+15), (cx-15, cy-5), (cx+15, cy-5)])
    elif word == "CAT":
        # Ears
        pygame.draw.polygon(surf, (245, 235, 215), [(cx-60, cy-50), (cx-90, cy-110), (cx-30, cy-70)])
        pygame.draw.polygon(surf, (245, 235, 215), [(cx+60, cy-50), (cx+90, cy-110), (cx+30, cy-70)])
        pygame.draw.circle(surf, (40, 40, 40), (cx - 40, cy - 10), 10)
        pygame.draw.circle(surf, (40, 40, 40), (cx + 40, cy - 10), 10)
        pygame.draw.line(surf, (40, 40, 40), (cx-20, cy+20), (cx-60, cy+15), 3)
        pygame.draw.line(surf, (40, 40, 40), (cx+20, cy+20), (cx+60, cy+15), 3)
    elif word == "DOG":
        # Ears
        pygame.draw.ellipse(surf, (140, 90, 50), (cx-r-5, cy-20, 50, 100))
        pygame.draw.ellipse(surf, (140, 90, 50), (cx+r-45, cy-20, 50, 100))
        pygame.draw.circle(surf, (40, 40, 40), (cx - 35, cy - 15), 12)
        pygame.draw.circle(surf, (40, 40, 40), (cx + 35, cy - 15), 12)
        pygame.draw.circle(surf, (40, 40, 40), (cx, cy + 25), 15)
    elif word == "FISH":
        surf.fill((0,0,0,0))
        pygame.draw.circle(surf, (80, 150, 240), (cx, cy), r-10)
        pygame.draw.polygon(surf, (80, 150, 240), [(cx-r+10, cy), (cx-r-10, cy-40), (cx-r-10, cy+40)])
        pygame.draw.circle(surf, (255, 255, 255), (cx + 40, cy - 15), 12)
        pygame.draw.circle(surf, (40, 40, 40), (cx + 45, cy - 15), 5)
    elif word == "BIRD":
        pygame.draw.circle(surf, (255, 210, 60), (cx, cy), r-10)
        pygame.draw.polygon(surf, (255, 80, 40), [(cx+r-10, cy), (cx+r+10, cy-15), (cx+r+10, cy+15)])
        pygame.draw.circle(surf, (40, 40, 40), (cx + 20, cy - 20), 10)
    elif word == "FROG":
        pygame.draw.circle(surf, (100, 200, 80), (cx, cy), r-10)
        pygame.draw.circle(surf, (100, 200, 80), (cx-40, cy-r+15), 30)
        pygame.draw.circle(surf, (100, 200, 80), (cx+40, cy-r+15), 30)
        pygame.draw.circle(surf, (40, 40, 40), (cx-40, cy-r+15), 10)
        pygame.draw.circle(surf, (40, 40, 40), (cx+40, cy-r+15), 10)
        pygame.draw.arc(surf, (40, 40, 40), (cx-30, cy+10, 60, 40), 3.14, 0, 4)
    elif word == "PIG":
        pygame.draw.circle(surf, (255, 180, 200), (cx, cy), r)
        pygame.draw.ellipse(surf, (255, 140, 170), (cx-30, cy+5, 60, 40))
        pygame.draw.circle(surf, (255, 100, 140), (cx-10, cy+25), 5)
        pygame.draw.circle(surf, (255, 100, 140), (cx+10, cy+25), 5)
        pygame.draw.circle(surf, (40, 40, 40), (cx-40, cy-10), 8)
        pygame.draw.circle(surf, (40, 40, 40), (cx+40, cy-10), 8)
    elif word == "BEAR":
        pygame.draw.circle(surf, (130, 80, 40), (cx, cy), r)
        pygame.draw.circle(surf, (130, 80, 40), (cx-r+20, cy-r+20), 40)
        pygame.draw.circle(surf, (130, 80, 40), (cx+r-20, cy-r+20), 40)
        pygame.draw.circle(surf, (40, 40, 40), (cx-35, cy-15), 10)
        pygame.draw.circle(surf, (40, 40, 40), (cx+35, cy-15), 10)
        pygame.draw.circle(surf, (100, 60, 30), (cx, cy+30), 35)
        pygame.draw.circle(surf, (40, 40, 40), (cx, cy+20), 12)
    else:
        # Default cute creature for others
        pygame.draw.circle(surf, (40, 40, 40), (cx-40, cy-10), 10)
        pygame.draw.circle(surf, (40, 40, 40), (cx+40, cy-10), 10)
        pygame.draw.arc(surf, (40, 40, 40), (cx-30, cy+10, 60, 40), 3.4, 6.0, 4)

    filename = os.path.join(ASSET_DIR, f"{word.lower()}.png")
    pygame.image.save(surf, filename)
    print(f"Generated: {filename}")

for animal in ANIMALS:
    generate_animal_png(animal)

pygame.quit()
