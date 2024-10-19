USE Prestamo_universal;
GO

CREATE TABLE #temp_clientes(
	--id_cliente INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	ti_documento CHAR(2),
	nu_documento VARCHAR(15),
	nombre_cliente NVARCHAR(100),
	email_cliente NVARCHAR(100),
	telefono_cliente VARCHAR(15),
	direccion_cliente NVARCHAR(200),
	--id_ubigeo_domicilio CHAR(6) FOREIGN KEY REFERENCES Ubigeo_domicilio(id_ubigeo_domicilio) NOT NULL,
	id_pais_docu CHAR(4),
	id_ti_persona CHAR(1),
	ti_sexo CHAR(1),
	fe_nacimiento DATE,
	id_profesion INT,
	id_esta_civil INT,
	id_estado CHAR(1),
	id_cat_cliente INT,
	fe_apertura  DATE NOT NULL DEFAULT GETDATE(),
	fe_aper_prim_prest DATE NOT NULL DEFAULT GETDATE(),
	--fe_actu_reg DATE NOT NULL DEFAULT GETDATE()
);
GO

SELECT * FROM #temp_clientes;