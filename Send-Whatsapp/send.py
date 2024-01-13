import pywhatkit as kit
print("Antes de ingresar los datos tenga whatsappWeb desde su navegador predefinido sincronizado con su dispositivo")
print("------- \n" * 5)
numero=input("ingrese numero de telefono al que quiera mandar Whatsapp ej. 2634845516: ")
mensaje=input("Ingrese mensaje a enviar: ")
hora=int(input("ingrese hora en el q desea mandar el mensaje ej.19: "))
minu=int(input("ingrese minutos en el q desea mandar el mensaje ej.45: "))
print("El mensaje se enviara automaticamente 20seg despues de que la aplicacion se ha abierto")
kit.sendwhatmsg("+549"+numero, mensaje, hora,minu)
