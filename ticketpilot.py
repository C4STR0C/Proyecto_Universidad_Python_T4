# TicketPilot - Castro
# clasifica tickets de soporte con gemini

from google import genai
import time

# tickets que llegaron
tickets = [
    "No puedo iniciar sesión en mi cuenta y tengo una presentación en una hora.",
    "Me cobraron dos veces la mensualidad de este mes.",
    "Quisiera saber si hay descuento si compro 50 licencias.",
    "La aplicación se cierra sola cuando subo una foto.",
    "Necesito una copia de mi factura de octubre.",
    "El sistema está caído y nadie en la empresa puede trabajar.",
]

ventas = []
soporte = []
facturacion = []
sin_clasificar = []

clave = input("API key de Gemini: ")
cliente = genai.Client(api_key=clave)

for ticket in tickets:
    print("\nTicket:", ticket)
    pregunta = "Clasifica este ticket de soporte. Responde solo URGENCIA;DEPARTAMENTO. Urgencia puede ser ALTA, MEDIA o BAJA. Departamento puede ser VENTAS, SOPORTE o FACTURACION. Ticket: " + ticket

    # a veces gemini se satura, entonces pruebo hasta 3 veces
    respuesta = ""
    intentos = 0
    while respuesta == "" and intentos < 3:
        try:
            respuesta = cliente.models.generate_content(model="gemini-3.5-flash-lite", contents=pregunta).text
        except Exception:
            print("gemini no responde, intentando de nuevo...")
            intentos = intentos + 1
            time.sleep(5)

    if ";" in respuesta:
        partes = respuesta.upper().split(";")
        urgencia = partes[0].strip()
        departamento = partes[1].strip()
        print("Urgencia:", urgencia, "| Departamento:", departamento)

        if departamento == "VENTAS":
            ventas.append(urgencia + " - " + ticket)
        elif departamento == "SOPORTE":
            soporte.append(urgencia + " - " + ticket)
        elif departamento == "FACTURACION":
            facturacion.append(urgencia + " - " + ticket)
        else:
            sin_clasificar.append(ticket)
    else:
        print("no se pudo clasificar")
        sin_clasificar.append(ticket)

# resultado final
print("\n----- VENTAS -----")
for t in ventas:
    print(t)

print("\n----- SOPORTE TECNICO -----")
for t in soporte:
    print(t)

print("\n----- FACTURACION -----")
for t in facturacion:
    print(t)

print("\n----- SIN CLASIFICAR -----")
for t in sin_clasificar:
    print(t)
