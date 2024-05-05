import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QRadioButton,
                             QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# 示例计算函数
def calculationOf30(screen_distance, wind_strength, is_downwind):
    power_data_30 = {
        1: 14, 2: 20, 3: 25, 4: 29, 5: 32, 6: 36, 7: 39, 8: 42, 9: 45, 10: 48,
        11: 50, 12: 53, 13: 55, 14: 58, 15: 60, 16: 63, 17: 65, 18: 67, 19: 69, 20: 71
    }
    base_power = power_data_30.get(screen_distance, None)
    if base_power is None:
        return None, None  # 如果屏距不在字典中，返回None

    adjusted_power = base_power - wind_strength if is_downwind else base_power + wind_strength
    return 30, adjusted_power  # 角度固定为30度

def calculationOf50(screen_distance, wind_strength, is_downwind):
    power_data_50 = {
        1: 14, 2: 20, 3: 25, 4: 29, 5: 32, 6: 36, 7: 39, 8: 42, 9: 45, 10: 48,
        11: 50, 12: 53, 13: 55, 14: 58, 15: 60, 16: 63, 17: 65, 18: 67, 19: 69, 20: 71
    }

    base_power = power_data_50.get(screen_distance, None)
    if base_power is None:
        return None, None  # 如果屏距不在字典中，返回None

    # 计算实际风力影响的角度变化和实际角度调整值
    doubled_wind_effect = wind_strength * 2
    actual_angle_adjustment = round(doubled_wind_effect)
    angle_difference = doubled_wind_effect - actual_angle_adjustment

    # 计算力度调整
    power_adjustment = round(abs(angle_difference) / 0.2)

    # 根据顺风还是逆风调整力度
    if is_downwind:
        # 顺风情况：如果2倍风力大于实际风力调整，减少力；反之增加力
        adjusted_power = base_power - power_adjustment if doubled_wind_effect > actual_angle_adjustment else base_power + power_adjustment
        adjusted_angle = 50 + actual_angle_adjustment
    else:
        # 逆风情况：如果2倍风力大于实际风力调整，增加力；反之减少力
        adjusted_power = base_power + power_adjustment if doubled_wind_effect > actual_angle_adjustment else base_power - power_adjustment
        adjusted_angle = 50 - actual_angle_adjustment

    return adjusted_angle, adjusted_power

def calculationOf65(screen_distance, wind_strength, is_downwind):
    power_data_65 = {
        1: 13, 2: 21, 3: 27, 4: 32, 5: 37, 6: 41, 7: 45, 8: 49, 9: 53, 10: 56,
        11: 59.5, 12: 63, 13: 66, 14: 69, 15: 72, 16: 75, 17: 78, 18: 81, 19: 83.5, 20: 86.5
    }

    base_power = power_data_65.get(screen_distance, None)
    if base_power is None:
        return None, None  # 如果屏距不在字典中，返回None
    wind_strength = wind_strength * 1.15
    # 计算实际风力影响的角度变化和实际角度调整值
    doubled_wind_effect = wind_strength * 2
    actual_angle_adjustment = round(doubled_wind_effect)
    angle_difference = doubled_wind_effect - actual_angle_adjustment

    # 计算力度调整
    power_adjustment = round(abs(angle_difference) / 0.2)

    # 根据顺风还是逆风调整力度
    if is_downwind:
        # 顺风情况：如果2倍风力大于实际风力调整，减少力；反之增加力
        adjusted_power = base_power - power_adjustment if doubled_wind_effect > actual_angle_adjustment else base_power + power_adjustment
        adjusted_angle = 65 + actual_angle_adjustment
    else:
        # 逆风情况：如果2倍风力大于实际风力调整，增加力；反之减少力
        adjusted_power = base_power + power_adjustment if doubled_wind_effect > actual_angle_adjustment else base_power - power_adjustment
        adjusted_angle = 65 - actual_angle_adjustment

    return adjusted_angle, adjusted_power

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("风力计算器 by 高木同学")
        self.resize(100, 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        font = QFont("Arial", 10)
        self.central_widget.setFont(font)
        self.central_widget.setStyleSheet("background-color: #f0f0f0;")

        # 创建输入字段
        self.screen_distance_line_edit = QLineEdit("1")
        self.wind_strength_line_edit = QLineEdit("0.0")
        self.create_input_field("屏距(整数):", self.screen_distance_line_edit, 1)
        self.create_input_field("风力(小数):", self.wind_strength_line_edit, 0.1)

        # 角度选择单选按钮
        self.angle_group = QGroupBox("选择角度")
        angle_layout = QHBoxLayout()
        self.angle_30 = QRadioButton("30°")
        self.angle_50 = QRadioButton("50°")
        self.angle_65 = QRadioButton("65°")
        self.angle_30.setChecked(True)
        angle_layout.addWidget(self.angle_30)
        angle_layout.addWidget(self.angle_50)
        angle_layout.addWidget(self.angle_65)
        self.angle_group.setLayout(angle_layout)
        self.layout.addWidget(self.angle_group)

        # 风向单选按钮
        self.wind_group = QGroupBox("风向")
        self.downwind = QRadioButton("顺风")
        self.upwind = QRadioButton("逆风")
        self.downwind.setChecked(True)
        wind_layout = QVBoxLayout()
        wind_layout.addWidget(self.downwind)
        wind_layout.addWidget(self.upwind)
        self.wind_group.setLayout(wind_layout)
        self.layout.addWidget(self.wind_group)

        # 结果标签
        self.force_output = QLabel("力度: 未计算")
        self.angle_output = QLabel("角度: 未计算")
        self.layout.addWidget(self.force_output)
        self.layout.addWidget(self.angle_output)

        # 计算按钮
        self.calculate_button = QPushButton("计算")
        self.calculate_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; height: 40px;")

    def create_input_field(self, label, line_edit, step):
        layout = QHBoxLayout()
        label_widget = QLabel(label)
        line_edit.setFixedWidth(100)

        increase_button = QPushButton("+")
        increase_button.setFixedWidth(30)
        increase_button.clicked.connect(lambda: self.adjust_value(line_edit, step))

        decrease_button = QPushButton("-")
        decrease_button.setFixedWidth(30)
        decrease_button.clicked.connect(lambda: self.adjust_value(line_edit, -step))

        layout.addWidget(label_widget)
        layout.addWidget(line_edit)
        layout.addWidget(increase_button)
        layout.addWidget(decrease_button)

        self.layout.addLayout(layout)

    def adjust_value(self, line_edit, delta):
        current_value = float(line_edit.text()) + delta
        if delta == 1 or delta == -1:
            line_edit.setText(f"{int(current_value)}")
        else:
            line_edit.setText(f"{current_value:.1f}")

    def calculate(self):
        try:
            screen_distance = int(self.screen_distance_line_edit.text())
            wind_strength = float(self.wind_strength_line_edit.text())
            is_downwind = self.downwind.isChecked()

            if self.angle_30.isChecked():
                angle, power = calculationOf30(screen_distance, wind_strength, is_downwind)
            elif self.angle_50.isChecked():
                angle, power = calculationOf50(screen_distance, wind_strength, is_downwind)
            elif self.angle_65.isChecked():
                angle, power = calculationOf65(screen_distance, wind_strength, is_downwind)

            if angle is not None and power is not None:
                self.force_output.setText(f"力度: {power:.1f}")
                self.angle_output.setText(f"角度: {angle}°")
            else:
                self.force_output.setText("无效的屏距输入")
                self.angle_output.setText("角度: 未计算")
        except Exception as e:
            self.force_output.setText("输入有误")
            self.angle_output.setText("计算错误")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
