import math
import numpy as np
def flow_rate(flow_rate0, diameter1, diameter2, density1, dinsity2, G_air_consumption_ = 0):
    square1 = (math.pi*diameter1**2)/4
    square2 = (math.pi*diameter2**2)/4
    flow_rate_new = (flow_rate0*density1*square1+G_air_consumption_)/(dinsity2*square2)
    return flow_rate_new
def coef_friction_work(flow_rate_, delta_x, diam, Energy, roughness, kin_viscosity):
    Re1 = 2.3*10**3
    Re2 = 10**4
    lambda_T1 = 64/Re1
    lambda_T2 = 64/Re2
    roughness_e = roughness/diam
    Re = (flow_rate_*diam)/kin_viscosity
    if Re <= Re1:
        lambda_T = 64/Re
    elif Re1 < Re <= Re2:
        lambda_T = lambda_T1 + ((lambda_T2-lambda_T1)/(Re2-Re1))*(Re-Re1)
    elif Re2 < Re <= 500/roughness_e:
        lambda_T = 0.067*(158/Re + 2*roughness_e)**0.2
    elif Re > 500/roughness_e:
        lambda_T = 0.067*(2.136 * roughness_e)**0.2
    lambda_friction = 1.05*lambda_T/(Energy**2)
    return lambda_friction*((delta_x*flow_rate_**2)/(diam*2))

def pressure(pressure0, flow_rate_, flow_rate_2, coord_z1, coord_z2, L_friction, density, alfa = 2):
    return pressure0 + density*(alfa*((flow_rate_**2 - flow_rate_2**2)/2) + 9.81*(coord_z2 - coord_z1) - L_friction)

def temperature_under(temperature_ambient,temperature0, G_air_consumption, coef_Cp, coef_alpha1, coef_lambda, coef_alpha2, diam1, diam2, step):
    k = 1 / (1 / (coef_alpha1) + (diam2 - diam1) / (coef_lambda) + 1 / (coef_alpha2))
    f = math.pi * step * (diam2 - diam1)
    a = 2 * G_air_consumption * coef_Cp + k * f
    b = 2 * G_air_consumption * coef_Cp - k * f
    return ((b*temperature0+2*k*f*temperature_ambient)/a)
def tempeature_up(temperature_ambient,temperature0, G_air_consumption, coef_Cp, coef_alpha1, coef_lambda, coef_alpha2, diam1, diam2, step):
    k = 1 / (1 / (coef_alpha1) + (diam2 - diam1) / (coef_lambda) + 1 / (coef_alpha2))
    f = math.pi * step * (diam2 - diam1)
    a = 2 * G_air_consumption * coef_Cp + k * f
    b = 2 * G_air_consumption * coef_Cp - k * f
    return ((b*temperature0+2*k*f*temperature_ambient)/a)

def underground(N, length, pressure0, density0, flow_rate0, coef_alpha1, coef_alpha2, coef_lambda, coef_Cp, diam1, diam2, Energy, temperature_ambient, roughness, kin_viscosity):
    print("_____")
    print("Значения для подземного участка")
    temperature0=temperature_ambient+length*0.03
    mas_temperature = [] #температура в начале участка
    mas_density = [] #плотность нефти
    mas_pressure = [] #давление
    mas_pressure_MPa = [] #давление в МПа
    mas_flow_rate = [] #скорость
    mas_temperature.append(temperature0)
    mas_density.append(density0)
    mas_pressure.append(pressure0)
    mas_flow_rate.append(flow_rate0)
    step = length/N
    for i in range(N):
        mas_flow_rate.append(flow_rate(mas_flow_rate[i], diam1, diam1, density0, density0, 0))
        L_friction_ = coef_friction_work(mas_flow_rate[i], step, diam1, Energy, roughness, kin_viscosity)
        mas_pressure.append(pressure(mas_pressure[i], mas_flow_rate[i], mas_flow_rate[i+1], step*i, step*(i+1), L_friction_, density0))
        mas_pressure_MPa.append(pressure(mas_pressure[i], mas_flow_rate[i], mas_flow_rate[i+1], step*i, step*(i+1), L_friction_, density0)//10**4/100)
        G_air_consumption = density0*mas_flow_rate[i]*math.pi*(diam1/2)**2
        mas_temperature.append(temperature_under(mas_temperature[i], temperature0 - (step*(i)*0.03), G_air_consumption, coef_Cp, coef_alpha1, coef_lambda, coef_alpha2, diam1, diam2, step))
    print("Скорость потока (mps) ", np.round(mas_flow_rate, decimals=2))
    print("Температура (C) ", np.round(mas_temperature, decimals=2))
    print("Давление (MPa) ", np.round(mas_pressure_MPa, decimals=2))

# def upground(N, length, pressure0, density0, flow_rate0, coef_alpha1, coef_alpha2, coef_lambda, coef_Cp, diam1, diam2, Energy, temperature_ambient, roughness, kin_viscosity):
#     mas_temperature = [] #температура в начале участка
#     mas_density = [] #плотность нефти
#     mas_pressure = [] #давление
#     mas_pressure_MPa = [] #давление в МПа
#     mas_flow_rate = [] #скорость
#     mas_density.append(density0)
#     mas_pressure.append(pressure0)
#     mas_flow_rate.append(flow_rate0)
#     step = length/N
#     temperature0=temperature_ambient+length*0.03
#     for i in range(N):
#         G_air_consumption = density0*mas_flow_rate[i]*math.pi*(diam1/2)**2
#         mas_temperature.append(temperature_under(mas_temperature[i], temperature0 - (step * (i) * 0.03), G_air_consumption, coef_Cp,coef_alpha1, coef_lambda, coef_alpha2, diam1, diam2, step))
#     print("_____")
#     print("Значения для надземного участка")
#     temperature0 = mas_temperature[::-1]
#     mas_temperature = []  # температура в начале участка
#     mas_density = []  # плотность нефти
#     mas_pressure = []  # давление
#     mas_pressure_MPa = []  # давление в МПа
#     mas_flow_rate = []  # скорость
#     mas_temperature.append(temperature0)
#     mas_density.append(density0)
#     mas_pressure.append(pressure0)
#     mas_flow_rate.append(flow_rate0)
#     step = length / N
#     for i in range(N):
#         mas_flow_rate.append(flow_rate(mas_flow_rate[i], diam1, diam1, density0, density0, 0))
#         L_friction_ = coef_friction_work(mas_flow_rate[i], step, diam1, Energy, roughness, kin_viscosity)
#         mas_pressure.append(pressure(mas_pressure[i], mas_flow_rate[i], mas_flow_rate[i+1], step*i, step*(i+1), L_friction_, density0))
#         mas_pressure_MPa.append(pressure(mas_pressure[i], mas_flow_rate[i], mas_flow_rate[i+1], step*i, step*(i+1), L_friction_, density0)//10**4/100)
#         G_air_consumption = density0*mas_flow_rate[i]*math.pi*(diam1/2)**2
#         mas_temperature.append(temperature_under(mas_temperature[i], temperature0 - (step*(i)*0.03), G_air_consumption, coef_Cp, coef_alpha1, coef_lambda, coef_alpha2, diam1, diam2, step))
#     print("Скорость потока ", np.round(mas_flow_rate, decimals=2))
#     print("Температура ", np.round(mas_temperature, decimals=2))
#     print("Давление ", np.round(mas_pressure_MPa, decimals=2))


def main():
    while True:
        print("Для расчета нажмите 1")
        print("Для выхода нажмите 2")
        print()
        a=int(input("Выберите пункт меню: "))
        if a==1:
            N=int(input("Введите количество участков: "))
            lenght=float(input("Введите длину трубопровода: "))
            pressure0=eval(input("Введите начальное давление: "))
            density0=eval(input("Введите плотность нефти: "))
            flow_rate0=eval(input("Введите начальную скорость потока: "))
            coef_alpha1=eval(input("Введите коэффициент теплообмена (нефть-трубопровод): "))
            coef_alpha2=eval(input("Введите коэффициент теплообмена (трубопровод-окружение): "))
            coef_lambda=eval(input("Введите коэффициент теплопроводности трубы: "))
            coef_Cp=eval(input("Введите удельную теплоемкость нефти: "))
            diam1=eval(input("Введите внутренний диаметр трубопровода: "))
            diam2=eval(input("Введите внешний диаметр трубопровода: "))
            Energy=eval(input("Введите энергию: "))
            temperature_ambient=eval(input("Введите температуру грунта на поверхности: "))
            roughness=eval(input("Введите шероховатость внутренней поверхности трубы: "))
            kin_viscosity=eval(input("Введите кинематическую вязкость нефти: "))
            underground(N, lenght, pressure0, density0, flow_rate0, coef_alpha1, coef_alpha2, coef_lambda, coef_Cp, diam1, diam2, Energy, temperature_ambient, roughness, kin_viscosity)
        # if a==2:
        #     N=int(input("Введите количество участков: "))
        #     lenght=float(input("Введите длину трубопровода: "))
        #     pressure0=eval(input("Введите начальное давление: "))
        #     density0=eval(input("Введите плотность нефти: "))
        #     flow_rate0=eval(input("Введите начальную скорость потока: "))
        #     coef_alpha1=eval(input("Введите коэффициент теплообмена (нефть-трубопровод): "))
        #     coef_alpha2=eval(input("Введите коэффициент теплообмена (трубопровод-окружение): "))
        #     coef_lambda=eval(input("Введите коэффициент теплопроводности трубы: "))
        #     coef_Cp=eval(input("Введите удельную теплоемкость нефти: "))
        #     diam1=eval(input("Введите внутренний диаметр трубопровода: "))
        #     diam2=eval(input("Введите внешний диаметр трубопровода: "))
        #     Energy=eval(input("Введите энергию: "))
        #     temperature_ambient=eval(input("Введите температуру окружающей среды: "))
        #     roughness=eval(input("Введите шероховатость поверхности: "))
        #     kin_viscosity=eval(input("Введите кинематическую вязкость нефти: "))
        #     upground(N, lenght, pressure0, density0, flow_rate0, coef_alpha1, coef_alpha2, coef_lambda, coef_Cp, diam1, diam2, Energy, temperature_ambient, roughness, kin_viscosity)
        elif a==3: break
        else: print("Неверный ввод")
underground(100, 2000, 3*10**6, 890, 1, 45, 2, 46, 2100, 0.089, 0.116, 2000, 5, 0.5, 0.0005)
#upground(100, 2000, 3*10**6, 890, 1, 45, 2, 46, 2100, 0.089, 0.116, 2000, 5, 0.5, 0.0005)