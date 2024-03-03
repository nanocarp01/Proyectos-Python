import threading
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

class BlinkDetectionApp:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Blink Detection GUI")
        self.video_source = video_source

        # Crear el lienzo para mostrar la cámara
        self.canvas_video = tk.Canvas(root)
        self.canvas_video.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Crear el lienzo para mostrar el gráfico
        self.canvas_graph = tk.Canvas(root, height= 600, width=400)
        self.canvas_graph.pack()

        # Crear el Label para mostrar blink_counter
        self.blink_counter_label = tk.Label(root, text="Blink Counter: 0", font=("Helvetica", 18))
        self.blink_counter_label.pack()

        # Crear el botón de inicio
        self.start_button = tk.Button(root, text="Iniciar",command=self.start_detection)
        self.start_button.pack(padx=10, pady=0)  # Agregar un poco de espacio entre el botón y el label

        # Crear la entrada de texto para el contador de cuenta regresiva
        self.countdown_label = tk.Label(root, text="Contador Regresivo:")
        self.countdown_label.pack()
        self.countdown_entry = tk.Entry(root)
        self.countdown_entry.pack()

        # Inicializar el hilo del contador
        self.countdown_thread = None
        self.countdown_value = 0
        self.countdown_running = False


        
        # Inicializar la captura de video
        self.cap = cv2.VideoCapture(self.video_source)
        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))

        # Agregar las dimensiones del óvalo
        self.oval_width = 200
        self.oval_height = 250
        self.oval_center = (self.width // 2, self.height // 2)

        # Inicializar la variable para detener la actualización
        self.stop_update = False

        self.aux_counter = 0
        self.blink_counter = 0

        # Create a placeholder image
        self.placeholder_image = ImageTk.PhotoImage(
            Image.fromarray(
                np.zeros((self.height, self.width, 3), dtype=np.uint8)))

        self.canvas_video.create_image(0, 0, image=self.placeholder_image, anchor=tk.NW)



        # Inicializar Mediapipe FaceMesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

        # Índices de puntos clave de los ojos
        self.index_left_eye = [33, 160, 158, 133, 153, 144]
        self.index_right_eye = [362, 385, 387, 263, 373, 380]

        # Estado de los ojos
        self.eyes_open = True

        # Crear la figura para el gráfico de Matplotlib
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_title("EAR(Eye Aspect Ratio) vs. Frames")

        # Crear un gráfico de ejemplo
        self.line1, = self.subplot.plot([], [])
        self.subplot.set_ylim(0, 0.4)
        self.subplot.set_ylim(0.1,0.4)
        self.subplot.set_ylabel("EAR")

        # Integrar el gráfico en el lienzo de Tkinter
        self.canvas_graph = FigureCanvasTkAgg(self.figure, master=self.canvas_graph)
        self.canvas_graph_widget = self.canvas_graph.get_tk_widget()
        self.canvas_graph_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Actualizar la cámara en el lienzo
        self.update_camera()

    def start_detection(self):
        # Alternar entre "Iniciar" y "Detener" al presionar el botón
        current_text = self.start_button.cget("text")
        if current_text == "Iniciar":
            # Obtener el valor ingresado en la entrada de texto y convertirlo a entero
            countdown_value = int(self.countdown_entry.get())
            
            if countdown_value > 0:
                # Iniciar el hilo del contador regresivo
                self.countdown_value = countdown_value
                self.countdown_running = True
                self.start_button.config(text="Detener")
                self.countdown_thread = threading.Thread(target=self.run_countdown)
                self.countdown_thread.start()
                
            elif countdown_value == 0:
                self.stop_detection()
            else:
                tk.messagebox.showwarning("Error", "Por favor, ingrese un tiempo mayor que cero.")
        else:
            
            # Detener la detección y el contador regresivo al presionar el botón
            self.countdown_value = 0

    def run_countdown(self):
        while self.countdown_value > 0 and self.countdown_running:
            time.sleep(1)
            self.countdown_value -= 1
            self.update_countdown_label()
        # Cuando el contador regresivo llega a cero, detener la detección
        self.stop_detection()

    def update_countdown_label(self):
        # Actualizar la etiqueta con el valor actual del contador regresivo
        self.countdown_label.config(text=f"Contador Regresivo: {self.countdown_value}")

    def stop_detection(self):
        self.start_button.config(text="Iniciar")
        self.update_countdown_label()
        self.countdown_value = 0
        self.countdown_label.config(text=f"Contador Regresivo: 0")


    def update_camera(self):
        # Verificar si la ventana principal está cerrada
        if not self.root.winfo_exists():
            return
        
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

            # Detección de puntos clave de los ojos con Mediapipe FaceMesh
            results = self.face_mesh.process(frame)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    self.draw_eyes(frame, face_landmarks)

                # Verificar si el centro de la cara está dentro del óvalo
                face_center = (int(results.multi_face_landmarks[0].landmark[0].x * self.width),
                               int(results.multi_face_landmarks[0].landmark[0].y * self.height))


                # Dibujar el óvalo en la imagen
                cv2.ellipse(frame, self.oval_center, (self.oval_width // 2, self.oval_height // 2), 0, 0, 360,
                            (0, 255, 0) if not self.stop_update else (255, 0, 0), 2)  # Green oval if not stopped, red otherwise
                
                

            # Verificar si la ventana principal está cerrada antes de intentar crear PhotoImage
            if self.root.winfo_exists():
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas_video.create_image(0, 0, image=self.photo, anchor=tk.NW)

            
        # Verificar si la ventana principal está cerrada antes de programar la próxima actualización
        if self.root.winfo_exists():
            self.root.after(10, self.update_camera)

    def is_inside_oval(self, x, y):
        # Verificar si las coordenadas (x, y) están dentro del óvalo
        a = self.oval_width // 2
        b = self.oval_height // 2
        x_center, y_center = self.oval_center

        return ((x - x_center) ** 2) / (a ** 2) + ((y - y_center) ** 2) / (b ** 2) <= 1

    def eye_aspect_ratio(self, normalized_landmarks):
        # Calcular la proporción de aspecto del ojo con coordenadas normalizadas
        d_A = np.linalg.norm(np.array(normalized_landmarks[1]) - np.array(normalized_landmarks[5]))
        d_B = np.linalg.norm(np.array(normalized_landmarks[2]) - np.array(normalized_landmarks[4]))
        d_C = np.linalg.norm(np.array(normalized_landmarks[0]) - np.array(normalized_landmarks[3]))

        return (d_A + d_B) / (2 * d_C)


    def draw_eyes(self, frame, landmarks):
        # Umbral de parpadeo
        ear_thresh = 0.26
        # Obtener las coordenadas de los puntos clave de los ojos
        left_eye_points = [(int(landmarks.landmark[i].x * self.width), int(landmarks.landmark[i].y * self.height)) for i in self.index_left_eye]
        right_eye_points = [(int(landmarks.landmark[i].x * self.width), int(landmarks.landmark[i].y * self.height)) for i in self.index_right_eye]

        # Normalizar las coordenadas en relación con el centro de los ojos
        left_eye_center = np.mean(left_eye_points, axis=0)
        right_eye_center = np.mean(right_eye_points, axis=0)

        normalized_left_eye = [(x - left_eye_center[0], y - left_eye_center[1]) for x, y in left_eye_points]
        normalized_right_eye = [(x - right_eye_center[0], y - right_eye_center[1]) for x, y in right_eye_points]

        ear_left_eye = self.eye_aspect_ratio(normalized_left_eye)
        ear_right_eye = self.eye_aspect_ratio(normalized_right_eye)
        ear = (ear_left_eye + ear_right_eye) / 2

         # Verificar si el centro de la cara está dentro del óvalo
        face_center = (int(landmarks.landmark[0].x * self.width),
                    int(landmarks.landmark[0].y * self.height))
        current_text = self.start_button.cget("text")
        if self.countdown_value > 0:
            # Determinar la actualización del gráfico
            if self.is_inside_oval(face_center[0], face_center[1]):
                self.stop_update = False
                # Actualizar el gráfico solo si self.stop_update es False
                self.plot_ear(ear)
            else:
                self.stop_update = True
        elif current_text == "Detener":
            self.stop_update = True

    def plot_ear(self, ear):
         # Umbral de parpadeo
        EAR_THRESH = 0.26
        NUM_FRAMES = 2
        #aux_counter = 0
        #blink_counter = 0

        if ear < EAR_THRESH:
            self.aux_counter += 1 
        else:
            if self.aux_counter >= NUM_FRAMES:
                self.aux_counter = 0
                self.blink_counter += 1

        # Actualizar el gráfico de Matplotlib con el nuevo valor de EAR
        self.line1.set_xdata(list(range(len(self.line1.get_xdata()) + 1)))
        self.line1.set_ydata(list(self.line1.get_ydata()) + [ear])

        # Ajustar el rango de la ventana de visualización del gráfico
        if len(self.line1.get_xdata()) > 50:
            self.subplot.set_xlim(len(self.line1.get_xdata()) - 50, len(self.line1.get_xdata()))

        # Agregar una línea horizontal en el umbral de parpadeo
        self.subplot.axhline(y=0.26, color='r', linestyle='--', label='Umbral de parpadeo')

        # Actualizar el texto del Label con el valor actual de blink_counter
        self.blink_counter_label.config(text=f"Blink Counter: {self.blink_counter}")
    

        # Redibujar la figura de Matplotlib en el lienzo de Tkinter
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def on_close(self):
        # Liberar recursos de la cámara al cerrar la aplicación
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = BlinkDetectionApp(root)
    root.attributes('-zoomed', True)  # Maximizar la ventana
    root.geometry("800x600")  # Tamaño de la ventana
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # Manejar cierre de ventana
    root.mainloop()

if __name__ == "__main__":
    main()
