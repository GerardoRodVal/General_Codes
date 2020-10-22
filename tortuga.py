import turtle

p = turtle.Screen()                                                          # Definiendo fondo de la tortuga
p.bgcolor("gold")                                                            # Color del fondo

gerardo = turtle.Turtle()                                                    # Generando tortuga
gerardo.color("white")                                                       # Color de la tortuga
#gerardo.shape("turtle")

nohely = turtle.Turtle()
nohely.color("red")
#nohely.shape("turtle")

for i in range(4):
 gerardo.left(90)
 gerardo.forward(100)


for i in range(4):
 nohely.right(45)
 nohely.forward(100)

