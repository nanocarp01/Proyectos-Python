import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics import barcode
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.graphics.barcode import code128
from barcode import Code128
from barcode.writer import ImageWriter

def enviar_correo(destinatario, asunto, cuerpo):
    """Recibe como parametros correo del destinatario, el asunto y el cuerpo del mensaje a ser enviado

    Args:
        destinatario (_type_): _description_
        asunto (_type_): _description_
        cuerpo (_type_): _description_
    """
    # Configura el servidor SMTP
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 465
    usuario_smtp = "mail"
    contrasena_smtp = "contraseña"

    # Configura el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = usuario_smtp
    mensaje['To'] = 'mail destino'
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Inicia la conexión con el servidor SMTP
    try:
            # Establecer conexión segura SSL
            with smtplib.SMTP_SSL(servidor_smtp, puerto_smtp) as server:
                # Autenticarse en el servidor SMTP
                server.login(usuario_smtp, contrasena_smtp)

                # Enviar correo electrónico
                server.sendmail(usuario_smtp, 'mail destino', mensaje.as_string())
    except smtplib.SMTPServerDisconnected as e:
            print(f"Error de conexión SMTP: {e}")
    except Exception as e:
            print(f"Error inesperado: {e}")

        # Envía el correo electrónico
        #server.send_message(mensaje)


def generar_codigo_barra(value, x, y):
    """_summary_

    Args:
        value (_type_): _description_
        x (_type_): _description_
        y (_type_): _description_
    """
    barcode = code128.Code128(value, barWidth=0.5, barHeight=20)
    drawing = Drawing(40, 10)
    drawing.add(barcode)
    drawing.drawOn(c, x, y)


def generar_pdf(nombre, apellido, total_deuda, cantidad_meses_deuda, detalles_deuda):
    # Crear un archivo PDF
    pdf_filename = f"{nombre}_{apellido}_deuda.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Configurar posición y estilo del texto
    y_position = 750
    styles = c.beginText()
    styles.setFont("Helvetica", 12)

    # Agregar información al PDF
    c.drawString(100, y_position, f"Cliente: {nombre} {apellido}")
    y_position -= 20
    c.drawString(100, y_position, f"Total de Deuda: ${total_deuda:.2f}")
    y_position -= 20
    c.drawString(100, y_position, f"Cantidad de Meses de Deuda: {cantidad_meses_deuda}")

    # Agregar detalles de deuda y códigos de barras
    y_position -= 40
    for detalle in str(detalles_deuda).split(','):
        if ' $' in detalle:
            mes, monto = detalle.split(' $')
            c.drawString(100, y_position, f"{mes}: ${monto}")

            # Generar código de barras y agregar al PDF
            barcode_value = f"{nombre}_{apellido}_{mes}"
            generar_codigo_barra(barcode_value, 100, y_position - 40)

            y_position -= 60  # Adjust the vertical position


    # Guardar y cerrar el PDF
    c.save()

def calcular_deuda_y_enviar_correo():
    # Configura la conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="user",
        password="passbasededatos",
        database="gestionClientes"
    )

    # Crea un cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Consulta SQL para calcular la deuda
    query = """
    SELECT cl.idCliente,
           cl.nombre,
           cl.apellido,
           cl.correo,
           ROUND(SUM(CASE WHEN cc.cargo IS NOT NULL THEN cc.cargo ELSE 0 END), 2) AS total_cargos,
           ROUND(SUM(CASE WHEN cc.pago IS NOT NULL THEN cc.pago ELSE 0 END), 2) AS total_pagos,
           ROUND(ROUND(SUM(CASE WHEN cc.cargo IS NOT NULL THEN cc.cargo ELSE 0 END), 2) -
           ROUND(SUM(CASE WHEN cc.pago IS NOT NULL THEN cc.pago ELSE 0 END), 2),2) AS Total_deuda,
           COUNT(DISTINCT CONCAT(cc.mes, '/', cc.anio)) AS cantidad_meses_deuda,
           GROUP_CONCAT(DISTINCT CONCAT(CONCAT(cc.mes, '/', cc.anio), ' $', ROUND(ROUND(cc.cargo, 2)-ROUND(cc.pago, 2),2)) ORDER BY cc.anio, cc.mes) AS detalles_deuda
    FROM clientes cl
    LEFT JOIN cuentaCorriente cc ON cl.idCliente = cc.idCliente
    GROUP BY cl.idCliente, cl.nombre, cl.correo;
    """

    # Ejecuta la consulta
    cursor.execute(query)

    # Recorre los resultados e imprime la deuda por cliente
    for (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, total_cargos, total_pagos,Total_deuda, detalles_deuda, cantidad_meses_deuda) in cursor:
        deuda = total_cargos - total_pagos
        if deuda > 0:
            mensaje_correo = f"Señor {nombre_cliente} {apellido_cliente}, tiene ${deuda:.2f} de deuda. Debe en {cantidad_meses_deuda}, cantidad de meses de deuda: {detalles_deuda}. Por favor, regularice su deuda."
            print(mensaje_correo)

            # Llama a la función para generar el PDF
            generar_pdf(nombre_cliente, apellido_cliente, deuda, cantidad_meses_deuda, detalles_deuda)

            # Envía el correo al cliente
            enviar_correo(correo_cliente, "Notificación de Deuda", mensaje_correo)

    # Cierra el cursor y la conexión
    cursor.close()
    conexion.close()

# Llama a la función para calcular la deuda y enviar correos
calcular_deuda_y_enviar_correo()
