def HVOF_Calc(arr):
    #Heat capacity of Water (J/KgC)
    C_w = 4.186

    #Density of water (Kg/L)
    rho_w = 1/1000.0

    #Standard Temperature of Alicats (K)
    Ts = 298.15

    #Standard Pressure of Alicats (PSI)
    Ps = 14.696

    #Density of Oxygen from Ideal Gas Law (g/L)
    rho_O = 32/22.4

    #Density of Kerosene (kg/m^3)
    rho_kero = 814.8

    #Heat/mass of kerosene (KJ/g)
    Q_kero = 64.0

    #Stoichiometric Ratio 
    stoich = 170.0/592.0

    
    Fl_fuel, Fl_w, T_in, T_out, m_dot_O = arr
    
    #Phi Calculation: mass flow is calculated in g/min
    m_dot_fuel = Fl_fuel * rho_kero
    phi = (m_dot_fuel/m_dot_O)/stoich
    
    #Heat Calculations
    Q_w = (T_out-T_in)*C_w*Fl_w*rho_w * (1/60.0) #1min/60seconds
    
    Q_fuel = m_dot_fuel*rho_kero * (1/60.0) #1min/60seconds
    
    return [phi, Q_w, Q_fuel]
    
    
