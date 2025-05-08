# 1.Introduction

The goal of my coursework is to learn abaut game development and to create a game demo of a rpg where the main magic
system is word based. The main controles for spells are space bar, right-cliking and left-cliking, and for the movement
it uses wasd controles.

# 2. Body/Analysis

## 2.1. Polymorphism

### Definition:

The word "polymorphism" means "many forms", and in programming it refers to methods/functions/operators with the
same name that can be executed on many objects or classes.

### How it works:

Polymorphism in Python works via dynamic method resolution.

### In code:

The classes Spells and Player both have an update method. 

## 2.2. Anstraction

### Definition:

Abstraction hides the complex internal details and shows only the necessary features of an object.

### How it works:

Abstraction works by forcing structure onto child classes while hiding the parent class's internal details.

### In code example:

pygame.sprite.Sprite has an abstract method height, width 

## 2.3. Inheritance

### Definition:

Inheritance allows a class to inherit attributes and methods from another class.

### How it works:
Inheritance works by reusing and extending functionality from parent classes.

### In code example:
`class Player (pygame.sprite.Sprite):
    def __init__(self): ...` <-the player class inherits atributes and methods from pygame.sprite.Sprite
`def update(self):
    self.player_input()
    self.animation_state()
    self.collision()` <- update() is one of those methods

## 2.4. Encapsulation

### Definition:

Encapsulation restricts direct access to some of an object’s components, which is a way of preventing
unintended interference and misuse.

### How it works:

Encapsulation hides internal state and requires controlled access through methods.

### In code example:

I haven't used Encapsulation in the code

## 2.5. Design pattern

I have used the facade design pattern, becouse it the most similar to my work flow. The Facade design pattern is a structural design pattern that provides a simplified interface to a library, a framework, or any
other complex set of classes.

## 2.6. Composition/Aggregation

`class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spreadsheet = SpriteSheet('Graphics/Player/player_sprite_sheet.png')
        self.spell_cooldown_timer= Timer(self.time)
        self.spell_cooldown_timer.deactivate()
        self.spell=Spells(self.player_dest_camera, self.player_rect)
        camera_group = CameraGroup()` <- all composition in the Payer class

# 3. Results and Summary

## 3.1. Results

- One of the challanges were making the screen resizable, becouse I wanted to make the home screen dynamic
- Another challange was trying to make the spells move, becouse I had to use trigonometry in a few areas and went through a few intirations of how I save the data of each spell
- Some of the proudest things that I somehow manage to make work is the camera and the map.

## 3.2. Conclusion

The work helped me understand how most game development works and what work goes into it, esspecially if you work 
with a framework and not a game engine. Honestly I'm really proud with the result of the program, no matter what grade 
I would get, becouse of how much work went into it. And in the future I hope to work further into updating it. 