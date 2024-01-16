import psutil
import smtplib
from email.mime.text import MIMEText

def check_system_status():
    # Obtener información del sistema
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/')
    
    # Definir umbrales para notificaciones
    cpu_threshold = 85
    ram_threshold = 80
    disk_threshold = 80

    # Verificar el estado de la CPU
    if cpu_percent > cpu_threshold:
        send_notification(f"¡Alerta! Uso de CPU al {cpu_percent}%")
        print(f"¡Alerta! Uso de CPU al {cpu_percent}%")

    # Verificar el estado de la RAM
    if ram_percent > ram_threshold:
        send_notification(f"¡Alerta! Uso de RAM al {ram_percent}%")
        print(f"¡Alerta! Uso de RAM al {ram_percent}%")
    # Verificar el estado del disco
    if disk_usage.percent > disk_threshold:
        send_notification(f"¡Alerta! Uso de disco al {disk_usage.percent}%")
        print(f"¡Alerta! Uso de disco al {disk_usage.percent}%")

def send_notification(message):
    # Configurar el servidor de correo
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'tu_correo@gmail.com'
    smtp_password = 'tu_contraseña'

    # Configurar el mensaje
    subject = 'Alerta del Microservicio de Monitoreo'
    body = message
    sender_email = 'tu_correo@gmail.com'
    receiver_email = 'correo_destino@example.com'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Enviar el correo
    try:
            # Establecer conexión segura SSL
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                # Autenticarse en el servidor SMTP
                server.login(smtp_username, smtp_password)

                # Enviar correo electrónico
                server.sendmail(sender_email, [receiver_email], msg.as_string())
    except smtplib.SMTPServerDisconnected as e:
            print(f"Error de conexión SMTP: {e}")
    except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == '__main__':
    check_system_status()
    time.sleep(3600) 
