import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = None

z_near = -3
z_far = -10
dx = -0.2
dy = -0.5
P = np.array([[1, 0, dx, 0],
              [0, 1, dy, 0],
              [0, 0, -z_far / (z_far - z_near), z_near * z_far / (z_far - z_near)],
              [0, 0, 1, 0]])

cam = np.array([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0]])
k1 = 1


def update_values(event=None):
    global data, z_far, z_near, dx, dy, P, cam, k1

    znear_value.set(str(z_near))
    znear_slider.set(str(z_near))

    zfar_value.set(str(z_far))
    zfar_slider.set(str(z_far))

    dx_value.set(str(dx))
    dx_slider.set(str(dx))

    dy_value.set(str(dy))
    rotation_xy_value.set(str(P[0, 2]))
    rotation_cam_x_value.set(str(cam[0, 0]))
    rotation_cam_y_value.set(str(cam[1, 1]))
    k1_value.set(str(k1))
    if data is not None:
        if z_far == z_near:
            return
        Zrange = z_far - z_near
        P[2, 2] = -z_far / Zrange
        P[2, 3] = z_near * z_far / Zrange
        P[0, 2] = dx
        P[1, 2] = dy
        ax.clear()

        dots = []
        for i in range(data.shape[0]):
            f = cam @ P @ data[i, :]
            dots.append(f / f[2])
        dots = np.array(dots)
        dots_center = np.array([0.1, 0.1])
        K2 = 0.0
        r = (dots[:, :2] - dots_center) ** 2
        f1 = (r).sum(axis=1)
        f2 = (r ** 2).sum(axis=1)
        mask = np.expand_dims(k1 * f1 + K2 * f2, axis=-1)
        dots_new = (dots[:, :2]) + (dots[:, :2] - dots_center) * mask
        ax.plot(dots_new[:, 0], dots_new[:, 1], '-D')
        ax.set_aspect('equal')
        canvas.draw()


def apply_text_fields():
    znear_slider.set(znear_value.get())
    zfar_slider.set(zfar_value.get())
    dx_slider.set(dx_value.get())
    dy_slider.set(dy_value.get())
    rotation_xy_slider.set(rotation_xy_value.get())
    rotation_cam_x_slider.set(rotation_cam_x_value.get())
    rotation_cam_y_slider.set(rotation_cam_y_value.get())
    k1_slider.set(k1_value.get())


def on_z_near_change(value):
    global z_near
    z_near = float(value)
    update_values()


def on_z_far_change(value):
    global z_far
    z_far = float(value)
    update_values()


def on_dx_change(value):
    global dx
    dx = float(value)
    update_values()


def on_dy_change(value):
    global dy
    dy = float(value)
    update_values()


def on_xy_rotation_change(value):
    global P
    angle = np.radians(float(value))
    cos_val = np.cos(angle)
    sin_val = np.sin(angle)

    P[0, 0] = cos_val
    P[0, 1] = -sin_val
    P[1, 0] = sin_val
    P[1, 1] = cos_val
    update_values()


def on_x_cam_rotation_change(value):
    global cam
    cam[0, 0] = float(value)
    update_values()


def on_y_cam_rotation_change(value):
    global cam
    cam[1, 1] = float(value)
    update_values()


def on_k1_change(value):
    global k1
    k1 = float(value)
    update_values()


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        obj = []
        with open(file_path, 'r') as file:
            for s in file:
                s += ' 1'
                obj.append(s.split())
        global data
        data = np.array(obj).astype(float)
        update_values()


root = tk.Tk()
root.title("3D Objects Viewer")

# Labels
labels = ['znear', 'zfar', 'dx', 'dy', 'Rotation XY', 'Rotation Cam X', 'Rotation Cam Y', 'K1']
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="e")  # Align labels to the right
    label.grid_columnconfigure(2, weight=1)  # Adjusts column span for alignment

# Sliders
sliders = {}
znear_slider = tk.Scale(root, from_=-100, to=100, length=250, resolution=1, orient='horizontal',
                        command=on_z_near_change)
znear_slider.grid(row=0, column=1, padx=5, pady=5)
sliders['znear'] = znear_slider

zfar_slider = tk.Scale(root, from_=-100, to=100, length=250, resolution=1, orient='horizontal', command=on_z_far_change)
zfar_slider.grid(row=1, column=1, padx=5, pady=5)
sliders['zfar'] = zfar_slider

dx_slider = tk.Scale(root, from_=-10.0, to=10.0, length=250, resolution=1.0, orient='horizontal', command=on_dx_change)
dx_slider.grid(row=2, column=1, padx=5, pady=5)
sliders['dx'] = dx_slider
dx_slider.set(-0.2)

dy_slider = tk.Scale(root, from_=-10.0, to=10.0, resolution=1.0, length=250, orient='horizontal', command=on_dy_change)
dy_slider.grid(row=3, column=1, padx=5, pady=5)
dy_slider.set(-0.5)
sliders['dy'] = dy_slider

rotation_xy_slider = tk.Scale(root, from_=-180, to=180, resolution=1, length=250, orient='horizontal',
                              command=on_xy_rotation_change)
rotation_xy_slider.grid(row=4, column=1, padx=5, pady=5)
sliders['Rotation XY'] = rotation_xy_slider

rotation_cam_x_slider = tk.Scale(root, from_=-10, to=10, resolution=1, length=250, orient='horizontal',
                                 command=on_x_cam_rotation_change)
rotation_cam_x_slider.grid(row=5, column=1, padx=5, pady=5)
sliders['Rotation Cam X'] = rotation_cam_x_slider

rotation_cam_y_slider = tk.Scale(root, from_=-10, to=10, resolution=1, length=250, orient='horizontal',
                                 command=on_y_cam_rotation_change)
rotation_cam_y_slider.grid(row=6, column=1, padx=5, pady=5)
sliders['Rotation Cam Y'] = rotation_cam_y_slider

k1_slider = tk.Scale(root, from_=-10, to=10, length=250, resolution=1.0, orient='horizontal', command=on_k1_change)
k1_slider.grid(row=7, column=1, padx=5, pady=5)
sliders['K1'] = k1_slider

# Text Entry
entries = {}
znear_value = tk.StringVar()
znear_entry = tk.Entry(root, textvariable=znear_value)
znear_entry.grid(row=0, column=2, padx=5, pady=15, sticky="w")  # Align entry to the left
entries['znear'] = znear_entry

zfar_value = tk.StringVar()
zfar_entry = tk.Entry(root, textvariable=zfar_value)
zfar_entry.grid(row=1, column=2, padx=5, pady=5, sticky="w")
entries['zfar'] = zfar_entry

dx_value = tk.StringVar()
dx_entry = tk.Entry(root, textvariable=dx_value)
dx_entry.grid(row=2, column=2, padx=5, pady=5, sticky="w")
entries['dx'] = dx_entry

dy_value = tk.StringVar()
dy_entry = tk.Entry(root, textvariable=dy_value)
dy_entry.grid(row=3, column=2, padx=5, pady=5, sticky="w")
entries['dy'] = dy_entry

rotation_xy_value = tk.StringVar()
rotation_xy_entry = tk.Entry(root, textvariable=rotation_xy_value)
rotation_xy_entry.grid(row=4, column=2, padx=5, pady=5, sticky="w")
entries['Rotation XY'] = rotation_xy_entry

rotation_cam_x_value = tk.StringVar()
rotation_cam_x_entry = tk.Entry(root, textvariable=rotation_cam_x_value)
rotation_cam_x_entry.grid(row=5, column=2, padx=5, pady=5, sticky="w")
entries['Rotation Cam X'] = rotation_cam_x_entry

rotation_cam_y_value = tk.StringVar()
rotation_cam_y_entry = tk.Entry(root, textvariable=rotation_cam_y_value)
rotation_cam_y_entry.grid(row=6, column=2, padx=5, pady=5, sticky="w")
entries['Rotation Cam Y'] = rotation_cam_y_entry

k1_value = tk.StringVar()
k1_entry = tk.Entry(root, textvariable=k1_value)
k1_entry.grid(row=7, column=2, padx=5, pady=5, sticky="w")
entries['K1'] = k1_entry

# Buttons
browse_btn = tk.Button(root, text="Browse", width=10, command=browse_file)
browse_btn.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)

apply_btn = tk.Button(root, text="Apply Text Fields", width=10, command=apply_text_fields)
apply_btn.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)

fig, ax = plt.subplots()
fig.set_size_inches(4, 3)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=10, column=0, columnspan=3, sticky=tk.NSEW)

update_values()
root.mainloop()
