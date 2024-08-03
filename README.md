-- Crear la base de datos
CREATE DATABASE tbmedicos;

-- Seleccionar la base de datos
USE tbmedicos;

-- Crear la tabla pacientes
CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico VARCHAR(50) DEFAULT '0',
    nombre VARCHAR(50) DEFAULT '0',
    fecha_nac DATE,
    enfermedades VARCHAR(50),
    alergias VARCHAR(50),
    antecedentes_medicos VARCHAR(50)
) COLLATE=latin1_spanish_ci;

-- Crear la tabla tbmedicos
CREATE TABLE medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    rfc VARCHAR(11),
    cedulaP VARCHAR(50),
    correoE VARCHAR(50),
    contraseña VARCHAR(50),
    rol VARCHAR(50)
) COLLATE=latin1_spanish_ci;
