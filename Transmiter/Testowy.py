from gpiozero import Energenie

lamp = Energenie(1)
lamp.on()
lamp.off()