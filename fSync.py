# Standard Library Imports
import os
import json
import numpy as np

# Third-Party Library Imports
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

# Maya-Specific Imports
from maya import cmds
import maya.OpenMayaUI as omui

# Import QApplication from PySide6
from PySide6.QtWidgets import QApplication

def get_maya_main_window():
    """Get the main Maya window as a QMainWindow instance."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr is not None:
        return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)
    else:
        return None


def show_dockable_window():
    """Show the dockable window in Maya, resetting it if it already exists with a custom name."""
    custom_workspace_control_name = "fSyncWindow"  # Custom workspace control name

    # Delete the workspace control if it already exists
    if cmds.workspaceControl(custom_workspace_control_name, query=True, exists=True):
        cmds.deleteUI(custom_workspace_control_name, control=True)

    # Create the dockable widget
    maya_main_window = get_maya_main_window()
    dockable_widget = FSyncUI(parent=maya_main_window)

    # Create a new workspace control for the window
    cmds.workspaceControl(
        custom_workspace_control_name,  # Use the custom name
        label="fSync",  # Label for the window
        floating=True,
        retain=False  # Do not retain size or position
    )

    # Get the Qt object of the workspace control and set the widget
    workspace_control_ptr = omui.MQtUtil.findControl(custom_workspace_control_name)
    if workspace_control_ptr:
        workspace_control_widget = wrapInstance(int(workspace_control_ptr), QtWidgets.QWidget)
        layout = workspace_control_widget.layout()
        layout.addWidget(dockable_widget)


class FSyncUI(QtWidgets.QWidget):
    """The main UI class for the fSync tool."""

    def __init__(self, parent=get_maya_main_window()):
        """
        Initialize the fSync UI.
        """
        super(FSyncUI, self).__init__(parent)
        self.func_instance = FSyncFunc(self)  # Replace with your actual functionality

        # UI Constants
        self.window_title = 'fSync'
        self.label_width = 150
        self.label_height = 30
        self.file_fields_empty = True

        # Enable DPI scaling for the UI
        self.dpi_scale = self.get_dpi_scale()

        # Set up window
        self.setWindowTitle(self.window_title)
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Build UI components
        self.build_ui()

        # Connect signals to slots
        self.connect_signals()

        # Add tooltips
        self.add_tooltips()

    def get_dpi_scale(self):
        """Get the DPI scaling factor based on the screen's DPI."""
        app = QApplication.instance()  # Ensure QApplication is properly imported
        dpi = app.primaryScreen().logicalDotsPerInch()
        default_dpi = 140  # Default DPI (standard for most screens)
        return dpi / default_dpi  # Calculate DPI scaling factor

    def scale_value(self, value):
        """Scale the given value by the DPI scaling factor."""
        return value * self.dpi_scale

    def scale_font(self, font):
        """Scale the font size by the DPI scaling factor."""
        font.setPointSizeF(font.pointSizeF() * self.dpi_scale)
        return font

    def build_ui(self):
        """Builds the UI layout and components."""

        self.add_launch_fspy_button()
        self.add_divider()

        # File fields
        self.json_file_field = self.add_file_field('Json File Location: ', 'Browse Files', 'json')
        self.image_file_field = self.add_file_field('Image File Location: ', 'Browse Files', 'image')

        # Checkbox for image sequence and frame offset
        self.image_sequence_checkbox, self.frame_offset_textbox = self.add_checkbox_with_label_and_textbox(
            'Image Sequence', 'Start Frame:  ', False
        )

        self.add_divider()

        # Camera and shader fields
        self.camera_name_field = self.add_text_field('Camera Name: ', 'Projection_Camera')
        self.shader_name_field = self.add_text_field('Shader Name: ', 'Projection_Shader')

        self.add_divider()

        # Create Scene button
        self.add_create_scene_button()

        self.add_divider()

        # Bottom buttons
        self.add_bottom_buttons()

        # Add stretch to push content upwards.
        self.main_layout.addStretch()

    def connect_signals(self):
        """Connects signals to corresponding methods."""
        self.launch_fspy.clicked.connect(self.func_instance.launch_fspy_action)
        self.json_file_field.textChanged.connect(self.update_button_state)
        self.image_file_field.textChanged.connect(self.update_button_state)
        self.create_scene_button.clicked.connect(self.func_instance.create_scene)
        self.update_scene_button.clicked.connect(self.func_instance.update_scene)
        self.apply_shader_selected_button.clicked.connect(self.func_instance.apply_projection_shader_to_selected)

    def add_tooltips(self):
        """Adds tooltips to key UI elements."""
        tooltips = {
            self.launch_fspy: "Click to launch the fSpy tool for camera projection setup.",
            self.json_file_field: "Specify the path to the JSON file from fSpy.",
            self.image_file_field: "Specify the path to the image file for the projection.",
            self.image_sequence_checkbox: "Check this box if you are using an image sequence.",
            self.frame_offset_textbox: "Enter the frame start number for the image sequence.",
            self.camera_name_field: "Enter the name for the projection camera.",
            self.shader_name_field: "Enter the name for the projection shader.",
            self.create_scene_button: "Click to create the projection camera and shader based on the provided inputs.",
            self.update_scene_button: "Click to update the scene with new data.",
            self.apply_shader_selected_button: "Click to apply the projection shader to all selected objects."
        }
        for widget, tooltip in tooltips.items():
            widget.setToolTip(tooltip)

    # UI Component Methods (Add components to layout)
    def add_launch_fspy_button(self):
        """Adds the 'Launch fSpy' button and layout."""
        self.launch_fspy_button_layout = QtWidgets.QHBoxLayout()
        self.launch_fspy = self.add_button('Launch fSpy', self.launch_fspy_button_layout)
        self.main_layout.addLayout(self.launch_fspy_button_layout)

    def add_create_scene_button(self):
        """Adds the 'Create Scene' button and layout."""
        self.create_scene_button_layout = QtWidgets.QHBoxLayout()
        self.create_scene_button = self.add_button('Create Scene', self.create_scene_button_layout,
                                                   self.file_fields_empty)
        self.main_layout.addLayout(self.create_scene_button_layout)

    def add_bottom_buttons(self):
        """Adds the bottom buttons layout."""
        self.bottom_button_layout = QtWidgets.QHBoxLayout()
        self.update_scene_button = self.add_button('Update Scene', self.bottom_button_layout, self.file_fields_empty)
        self.apply_shader_selected_button = self.add_button('Apply Shader to Selected', self.bottom_button_layout)
        self.main_layout.addLayout(self.bottom_button_layout)

    def add_divider(self):
        """Adds a horizontal line divider to the main layout."""
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setStyleSheet("color: lightgray; max-height: 1px;")
        self.main_layout.addWidget(line)

    def add_file_field(self, label: str, button_label: str, field_name: str):
        """Adds a file input field with a label and browse button."""
        text_field_label = QtWidgets.QLabel(label)
        text_field_label.setFixedSize(self.label_width, self.scale_value(self.label_height))

        text_field_box = QtWidgets.QLineEdit()
        text_field_box.setMinimumWidth(self.label_width)

        text_field_button = QtWidgets.QPushButton(button_label)
        text_field_button.setFixedSize(self.label_width, self.scale_value(self.label_height))

        setattr(self, f"{field_name}_field", text_field_box)
        setattr(self, f"{field_name}_button", text_field_button)

        text_field_button.clicked.connect(lambda: self.select_file(field_name))

        local_layout = QtWidgets.QHBoxLayout()
        local_layout.addWidget(text_field_label)
        local_layout.addWidget(text_field_box)
        local_layout.addWidget(text_field_button)

        self.main_layout.addLayout(local_layout)

        return text_field_box

    def add_text_field(self, label: str, placeholder_text: str):
        """Adds a labeled text field with a placeholder."""
        text_field_label = QtWidgets.QLabel(label)
        text_field_label.setFixedSize(self.label_width, self.scale_value(self.label_height))

        text_field_box = QtWidgets.QLineEdit()
        text_field_box.setPlaceholderText(placeholder_text)

        local_layout = QtWidgets.QHBoxLayout()
        local_layout.addWidget(text_field_label)
        local_layout.addWidget(text_field_box)

        self.main_layout.addLayout(local_layout)
        return text_field_box

    def add_checkbox_with_label_and_textbox(self, label: str, label2: str, is_checked: bool):
        """
        Adds a checkbox, label, textbox, and separator. The textbox visibility is controlled by the checkbox state.
        """
        checkbox = QtWidgets.QCheckBox(label)
        checkbox.setChecked(is_checked)
        checkbox.setFixedSize(self.label_width, self.scale_value(self.label_height))
        checkbox.setStyleSheet("QCheckBox { padding-top: -2px; }")  # Adjust checkbox text position

        label_widget = QtWidgets.QLabel(label2)
        label_widget.setAlignment(QtCore.Qt.AlignRight)
        label_widget.setFixedSize(self.label_width -8, self.scale_value(self.label_height))
        label_widget.setContentsMargins(0, 2, 0, 0)  # Offset label down by 2 pixels

        frame_offset_textbox = QtWidgets.QLineEdit()
        frame_offset_textbox.setEnabled(is_checked)

        # Style label based on checkbox state
        self.update_label_style(label_widget, is_checked)

        # Vertical separator line
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Horizontal layout for checkbox, separator, label, and textbox
        local_layout = QtWidgets.QHBoxLayout()
        local_layout.addWidget(checkbox)
        local_layout.addWidget(separator)
        local_layout.addWidget(label_widget)
        local_layout.addWidget(frame_offset_textbox)
        local_layout.setAlignment(QtCore.Qt.AlignLeft)

        # Add the layout to the main layout
        self.main_layout.addLayout(local_layout)

        # Update textbox and label state based on checkbox
        checkbox.toggled.connect(lambda checked: (
            frame_offset_textbox.setEnabled(checked),
            self.update_label_style(label_widget, checked)
        ))

        return checkbox, frame_offset_textbox

    def add_button(self, label: str, parent_layout: QtWidgets.QHBoxLayout, empty_field=None):
        """
        Adds a button to the given layout. Disables the button if `empty_field` is True.
        """
        button = QtWidgets.QPushButton(label)
        button.setFixedHeight(self.scale_value(self.label_height))
        button.setEnabled(not empty_field)
        parent_layout.addWidget(button)
        return button

    def update_button_state(self):
        """Enables or disables buttons based on file field contents."""
        self.file_fields_empty = not (self.json_file_field.text() and self.image_file_field.text())
        self.create_scene_button.setEnabled(not self.file_fields_empty)
        self.update_scene_button.setEnabled(not self.file_fields_empty)

    def select_file(self, field_name: str):
        """
        Opens a file dialog to select a file, and updates the text field with the file path.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            text_field = getattr(self, f"{field_name}_field")
            text_field.setText(file_path)

    def update_label_style(self, label_widget, is_checked):
        """Updates the color of the label based on the checkbox state."""
        label_widget.setStyleSheet(f"QLabel {{ color: {'lightgray' if is_checked else 'gray'}; }}")

    def get_field_value(self, text_field: QtWidgets.QLineEdit, place_holder_text: str):
        """
        Returns the text from the text field, or the placeholder if the field is empty.
        """
        return text_field.text() or place_holder_text

    def get_text_field_value(self, field_name: str):
        """
        Returns the current value of the text field.
        """
        text_field = getattr(self, f"{field_name}_field")
        return text_field.text()

# The following line would typically be used to connect the UI to Maya's main window.
def get_maya_main_window():
    """Gets the Maya main window to parent the widget to."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class FSyncFunc:
    """
    Class to handle fSync functionality, including launching fSpy, creating and updating Maya scenes, and handling shaders.
    """

    def __init__(self, ui):
        """
        Initializes the FSyncFunc instance with UI references and sets default values for the scene parameters.

        :param ui: The instance of the UI class.
        """
        self.ui_instance = ui

        # File paths for the JSON and image data
        self.json_file_path = None
        self.image_file_path = None

        # Names for camera and shader
        self.camera_name = None
        self.shader_name = None
        self.projection_shader = None

        # Camera transformation parameters
        self.aspect_ratio = self.angle_of_view = self.focal_length = None
        self.pos_x = self.pos_y = self.pos_z = None
        self.euler_angles = None

    def launch_fspy_action(self):
        """
        Launches the fSpy application if the executable exists.
        """
        fspy_path = os.path.join(os.environ.get('USERPROFILE', ''), "AppData", "Local", "Programs", "fspy", "fSpy.exe")
        if os.path.exists(fspy_path):
            os.startfile(fspy_path)
        else:
            cmds.warning("fSpy application not found.")

    def _get_ui_input(self):
        """
        Retrieves the user input values from the UI for JSON file, image file, camera name, and shader name.
        """
        self.json_file_path = self.ui_instance.get_text_field_value("json")
        self.image_file_path = self.ui_instance.get_text_field_value("image")
        self.camera_name = self.ui_instance.get_field_value(self.ui_instance.camera_name_field, "Projection_Camera")
        self.shader_name = self.ui_instance.get_field_value(self.ui_instance.shader_name_field, "Projection_Shader")

    def create_scene(self):
        """
        Creates a new scene based on the user input. This includes creating a camera and shader.
        """
        self._get_ui_input()
        self.create_camera()
        if cmds.objExists(self.camera_name):
            self.create_projection_shader()

    def update_scene(self):
        """
        Updates the scene based on the user input. This includes updating the camera and shader.
        """
        self._get_ui_input()
        self.update_camera()
        self.update_projection_shader()

    def _load_json_data(self):
        """
        Loads the JSON data from the specified file path.

        :return: A dictionary of the parsed JSON data.
        :raises: Error if the file doesn't exist.
        """
        if not os.path.exists(self.json_file_path):
            cmds.error(f"JSON file does not exist: {self.json_file_path}")
            return {}
        with open(self.json_file_path, 'r') as file:
            return json.load(file)

    def create_camera(self):
        """
        Creates a new camera in the scene based on the JSON data.
        """
        if cmds.objExists(self.camera_name):
            print("Camera already exists.")
            return
        data = self._load_json_data()
        self.extract_data(data)
        self.cam_item = cmds.camera(n='place_holder', hfv=self.angle_of_view, ar=self.aspect_ratio,
                                    p=[self.pos_x, self.pos_y, self.pos_z], rot=self.euler_angles, lt=False)[0]
        self.cam_item = cmds.rename(self.cam_item, self.camera_name)

    def update_camera(self):
        """
        Updates the position, rotation, and focal length of an existing camera in the scene.
        """
        data = self._load_json_data()
        self.extract_data(data)
        if cmds.objExists(self.camera_name):
            cmds.setAttr(f"{self.camera_name}.translateX", self.pos_x)
            cmds.setAttr(f"{self.camera_name}.translateY", self.pos_y)
            cmds.setAttr(f"{self.camera_name}.translateZ", self.pos_z)
            cmds.setAttr(f"{self.camera_name}.rotateX", self.euler_angles[0])
            cmds.setAttr(f"{self.camera_name}.rotateY", self.euler_angles[1])
            cmds.setAttr(f"{self.camera_name}.rotateZ", self.euler_angles[2])
            cmds.setAttr(f"{self.camera_name}.focalLength", self.focal_length)
        else:
            cmds.warning(f"Camera '{self.camera_name}' does not exist.")

    def extract_data(self, data):
        """
        Extracts relevant camera transformation data from the JSON file.

        :param data: The parsed JSON data.
        """
        self.aspect_ratio = data["imageWidth"] / data["imageHeight"]
        self.angle_of_view = np.degrees(data["horizontalFieldOfView"])
        self.focal_length = (24 * self.aspect_ratio) / (2 * np.tan(np.radians(self.angle_of_view) / 2))
        rows = data['cameraTransform']['rows']
        self.pos_x, self.pos_y, self.pos_z = rows[0][3], rows[1][3], rows[2][3]
        rot_matrix = np.array([row[:3] for row in rows[:3]])
        self.euler_angles = self.rotation_matrix_to_euler_zyx(rot_matrix)

    def rotation_matrix_to_euler_zyx(self, matrix):
        """
        Converts a rotation matrix to Euler angles (ZYX convention).

        :param matrix: The 3x3 rotation matrix.
        :return: The corresponding Euler angles in degrees.
        """
        if abs(matrix[2, 0]) != 1:
            pitch = -np.arcsin(matrix[2, 0])
            roll = np.arctan2(matrix[2, 1] / np.cos(pitch), matrix[2, 2] / np.cos(pitch))
            yaw = np.arctan2(matrix[1, 0] / np.cos(pitch), matrix[0, 0] / np.cos(pitch))
        else:
            yaw = 0
            pitch = np.pi / 2 if matrix[2, 0] == -1 else -np.pi / 2
            roll = yaw + np.arctan2(matrix[0, 1], matrix[0, 2]) if matrix[2, 0] == -1 else -yaw + np.arctan2(
                -matrix[0, 1], -matrix[0, 2])
        return np.degrees([roll, pitch, yaw])

    def create_projection_shader(self):
        """
        Creates a projection shader based on the provided camera and image file.
        """
        if self.projection_shader and cmds.objExists(self.shader_name):
            print("Shader already exists.")
            return
        if not cmds.objExists(self.camera_name):
            cmds.error(f"Camera '{self.camera_name}' does not exist.")
            return

        self.projection_shader = cmds.shadingNode("surfaceShader", asShader=True, name=self.shader_name)
        file_node = cmds.shadingNode("file", asTexture=True, isColorManaged=True, name=f"{self.shader_name}_file")
        cmds.setAttr(f"{file_node}.fileTextureName", self.image_file_path, type="string")
        self.image_sequence_func(file_node)

        expression = f"{file_node}.frameExtension = frame"
        cmds.expression(s=expression, o=file_node, ae=True, uc="all")

        cmds.setAttr(f"{file_node}.wrapU", 0)
        cmds.setAttr(f"{file_node}.wrapV", 0)

        projection_node = cmds.shadingNode("projection", asUtility=True, name=f"{self.shader_name}_projection")
        cmds.setAttr(f"{projection_node}.projType", 8)
        cmds.connectAttr(f"{file_node}.outColor", f"{projection_node}.image", force=True)
        cmds.connectAttr(f"{self.camera_name}.worldInverseMatrix[0]", f"{projection_node}.placementMatrix", force=True)
        cmds.connectAttr(f"{cmds.listRelatives(self.camera_name, shapes=True, type='camera')[0]}.message",
                         f"{projection_node}.linkedCamera", force=True)

        cmds.connectAttr(f"{projection_node}.outColor", f"{self.projection_shader}.outColor", force=True)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{self.shader_name}_SG")
        cmds.connectAttr(f"{self.projection_shader}.outColor", f"{shading_group}.surfaceShader", force=True)

        cmds.modelEditor('modelPanel4', edit=True, displayTextures=True)
        print(
            f"Projection shader '{self.shader_name}' created with image: {self.image_file_path} using camera: {self.camera_name}")

    def update_projection_shader(self):
        """
        Updates the projection shader with the new image file path and refreshes the viewport.
        """
        file_nodes = cmds.ls(f"{self.shader_name}_file", type="file")
        if not file_nodes:
            cmds.warning(f"File node '{self.shader_name}_file' does not exist.")
            return

        file_node = file_nodes[0]
        if not self.image_file_path:
            cmds.warning("Image file path is empty. Cannot update the shader.")
            return

        cmds.setAttr(f"{file_node}.fileTextureName", self.image_file_path, type="string")
        self.image_sequence_func(file_node)
        cmds.refresh()
        print("Viewport refreshed to display the updated texture.")

    def image_sequence_func(self, file_node):
        """
        Handles the image sequence behavior for the shader.

        :param file_node: The file node for the texture in the shader.
        """
        if self.ui_instance.image_sequence_checkbox.isChecked():
            cmds.setAttr(f"{file_node}.useFrameExtension", 1)
            frame_offset_text = self.ui_instance.frame_offset_textbox.text()
            try:
                frame_offset_value = float(frame_offset_text.strip()) if frame_offset_text else cmds.playbackOptions(
                    q=True, min=True)
                cmds.setAttr(f"{file_node}.frameOffset", -frame_offset_value + 1)
            except ValueError:
                cmds.warning(f"Invalid frame offset value: {frame_offset_text}")
        else:
            cmds.setAttr(f"{file_node}.useFrameExtension", 0)

    def apply_projection_shader_to_selected(self):
        """
        Applies the created projection shader to the selected objects in the scene.
        """
        selected_objects = cmds.ls(selection=True, long=True)
        if not selected_objects:
            cmds.warning("No objects selected. Please select objects to apply the shader.")
            return
        if not self.projection_shader:
            cmds.error("Projection shader not created. Please create the shader first.")
            return
        for obj in selected_objects:
            if 'mesh' in (cmds.objectType(shape) for shape in
                          cmds.listRelatives(obj, shapes=True, fullPath=True) or []):
                cmds.select(obj)
                cmds.hyperShade(assign=self.projection_shader)
                print(f"Applied projection shader to {obj}")